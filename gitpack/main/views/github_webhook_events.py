from .github_webhook import GithubApp
from django.http import JsonResponse
from main.lib.openai import OpenAIHelper

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

    query = ""

    # Loop through each changed file
    for file in files_changed:
        # Get the file content and diff
        file_content = file.raw_url
        file_patch = file.patch
        query += f"File path: {file.filename}\n\nContent:\n{file.patch}\n\n"

    # Initialize OpenAIHelper
    openai_helper = OpenAIHelper()
    feedback_json = openai_helper.get_code_review(query)

    overall_feedback = f"## Code Review for PR: {pr_title}\n\n{feedback_json['overall']['summary']}\n\n"
    if feedback_json['overall'].get('positives'):
        if type(feedback_json['overall']['positives']) is list:
            positives = ''.join(f'- {s}\n' for s in feedback_json['overall']['positives'])
        else:
            positives = feedback_json['overall']['positives']
        overall_feedback += f"### Positives:\n\n{positives}\n\n"
    if feedback_json['overall'].get('improvements'):
        #if type of feedback_json['overall']['improvements']) is list
        if type(feedback_json['overall']['improvements']) is list:
            improvements = ''.join(f'- {s}\n' for s in feedback_json['overall']['improvements'])
        else:
            improvements = feedback_json['overall']['improvements']
        overall_feedback += f"### Areas of Improvement:\n\n{improvements}\n\n"
    
    # Based on GPT feedback, add specific line comments if improvements are needed
    line_comments = []
    if feedback_json.get('inline_feedback'):
        for feedback in feedback_json['inline_feedback']:
            line_comments.append({
                'body': f"{feedback['feedback']}",
                'filename': feedback['file_path'],
                'start_line': feedback['start_line'],
                'start_side': feedback['start_side'],
                'end_line': feedback['end_line'],
                'end_side': feedback['end_side'],
                'suggested_change': feedback.get('suggested_change', None)
            })

    # Post overall review comment
    pull_request.create_issue_comment(overall_feedback)

    print('line_comments:', line_comments, 'pull_request.head.sha:', pull_request.head.sha)
    latest_commit = pull_request.get_commits()[0]
    # Post line-specific comments
    for comment in line_comments:
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

    return JsonResponse({'status': f"Handled pull_request.opened: {pr_number}"}, status=200)

# Handle issue opened
@github_app.on(event_type='issues', action='opened')
def handle_issue_opened(request, payload):
    issue_title = payload['issue']['title']
    issue_url = payload['issue']['html_url']
    print(f"Issue opened: {issue_title} ({issue_url})")
    return JsonResponse({'status': f"Handled issues.opened: {issue_title}"}, status=200)

# Additional events can be handled in a similar way
@github_app.on(event_type='pull_request', action='closed')
def handle_pull_request_closed(request, payload):
    pr_title = payload['pull_request']['title']
    pr_url = payload['pull_request']['html_url']
    print(f"Pull request closed: {pr_title} ({pr_url})")
    return JsonResponse({'status': f"Handled pull_request.closed: {pr_title}"}, status=200)
