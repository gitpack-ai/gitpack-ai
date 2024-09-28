import github.PullRequest
from ._github_webhook_wrapper import GithubApp
from django.http import JsonResponse
from main.lib.openai import OpenAIHelper
import logging
import github
import json
github_app = GithubApp()

# Handle pull request opened
@github_app.on(event_type='pull_request', actions=('opened', 'synchronize'))
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

    # Get all commits and select the last one (latest)
    commits = list(pull_request.get_commits())
    latest_commit = commits[-1]

    # Initialize OpenAIHelper
    openai_helper = OpenAIHelper()
    overall_feedback, line_comments = openai_helper.get_code_review(files_changed) 

    logging.debug(f"Overall feedback: {overall_feedback}")
    logging.debug(f"Line comments: {json.dumps(line_comments, indent=4, default=str)}")

    comments = []

    # Add line-specific comments to the review
    for comment in line_comments:
        try:
            comment_body = comment['body']
            if comment['suggested_code_changes']:
                if isinstance(comment['suggested_code_changes'], list):
                    suggested_code_changes = "\n".join(comment['suggested_code_changes'])
                else:
                    suggested_code_changes = comment['suggested_code_changes']
                comment_body += f"\n\n```suggestion\n{suggested_code_changes}\n```"
            
            if comment['start_line'] == comment['end_line']:
                comments.append(github.PullRequest.ReviewComment(
                    body=comment_body, 
                    path=comment['filename'], 
                    line=comment['start_line'], 
                    side=comment['start_side']
                ))
            else:
                comments.append(github.PullRequest.ReviewComment(
                    body=comment_body, 
                    path=comment['filename'], 
                    line=comment['end_line'], 
                    side=comment['end_side'],
                    start_line=comment['start_line'], 
                    start_side=comment['start_side']
                ))
        except Exception as e:
            logging.error(f"Error when creating review comment: {e}")
            logging.debug(f"Comment: {json.dumps(comment, indent=4, default=str)}")
            # Continue with other comments instead of raising an exception
            continue

    # Submit the review with the overall feedback as the body
    review = pull_request.create_review(commit=latest_commit, body=overall_feedback, comments=comments)

    return JsonResponse({'status': f"Handled pull_request.opened: {pr_number}"}, status=200)

