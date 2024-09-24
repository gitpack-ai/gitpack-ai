from .github_webhook import GithubApp
from django.http import JsonResponse
from main.lib.openai import OpenAIHelper
import logging
import github

github_app = GithubApp()

# Handle pull request opened
@github_app.on(event_type='pull_request', action='opened')
def handle_pull_request_opened(request, payload):
    # Get the repository and pull request number from the payload
    repo_full_name = payload['repository']['full_name']
    pr_number = payload['pull_request']['number']
    pr_title = payload['pull_request']['title']

    gc = github_app.get_github_client(payload)
    # Get the repository object
    repo = gc.get_repo(repo_full_name)

    # Get the PullRequest object
    pull_request = repo.get_pull(pr_number)

    # Get the list of files changed in the pull request
    files_changed = pull_request.get_files()

    latest_commit = pull_request.get_commits()[0]

    query = ""

    # Loop through each changed file
    for file in files_changed:
        # Get the file content and diff
        file_content = file.raw_url
        file_patch = file.patch
        query += f"File path: {file.filename}\n\nContent:\n{file.patch}\n\n"

    # Initialize OpenAIHelper
    openai_helper = OpenAIHelper()
    overall_feedback, line_comments = openai_helper.get_code_review(query)

    # Post line-specific comments
    for comment in line_comments:
        try:
            if comment['start_line'] == comment['end_line']:
                pull_request.create_review_comment(
                    body=comment['body'], 
                    commit=latest_commit,
                    path=comment['filename'], 
                    line=comment['start_line'], 
                    side=comment['start_side']
                )
            else:
                pull_request.create_review_comment(
                    body=comment['body'], 
                    commit=latest_commit,
                    path=comment['filename'], 
                    line=comment['end_line'], 
                    side=comment['end_side'],
                    start_line=comment['start_line'], 
                    start_side=comment['start_side']
                )
        except github.GithubException.GithubException as e:
            if e.status == 422 and 'Validation Failed' in str(e):
                # Handle validation failed exception
                logging.error(f"Validation failed when creating review comment: {e}")
                # You might want to skip this comment or try an alternative approach
                continue
            else:
                # Handle other GitHub exceptions
                logging.error(f"GitHub API error when creating review comment: {e}")
                # You might want to retry or handle the error in some way
                raise

    # Post overall review comment
    pull_request.create_issue_comment(overall_feedback)  

    return JsonResponse({'status': f"Handled pull_request.opened: {pr_number}"}, status=200)

