import github.PullRequest
from ._github_webhook_wrapper import GithubApp
from django.http import JsonResponse
from main.lib.ai_factory import get_ai_helper
import logging
import github
import json
from main.models import Repository, Organization

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
    repository = Repository.objects.get(third_party_id=repo.id)
    if not repository.is_enabled:
        logging.info(f"Pull request opened for disabled repository: {repo_full_name} (ID: {repo.id})")
        return JsonResponse({'status': f"Handled pull_request.opened: {pr_number}"}, status=200)

    # Get the PullRequest object
    pull_request = repo.get_pull(pr_number)

    # Get the list of files changed in the pull request
    files_changed = pull_request.get_files()

    # Get all commits and select the last one (latest)
    commits = list(pull_request.get_commits())
    latest_commit = commits[-1]

    # Get the appropriate AI helper based on settings
    ai_helper = get_ai_helper()
    overall_feedback, line_comments = ai_helper.get_code_review(files_changed) 

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


@github_app.on(event_type='installation_repositories', actions=('added', 'removed'))
def handle_installation_repositories(request, payload):
    """
    Handle the 'installation_repositories' event when the GitHub App is installed on new repositories.
    """
    action = payload.get('action')
    installation = payload.get('installation')
    
    if action == 'added':
        repositories_added = payload.get('repositories_added', [])
        for repo in repositories_added:
            repo_name = repo.get('full_name')
            repo_id = repo.get('id')
            
            # Log the new installation
            logging.info(f"GitHub App installed on new repository: {repo_name} (ID: {repo_id})")

            # get or create organization
            organization, created = Organization.objects.update_or_create(
                third_party_id=installation.get('id'),
                defaults={
                    'name': installation.get('account').get('login'),
                    'url': installation.get('account').get('html_url'),
                    'avatar_url': installation.get('account').get('avatar_url')
                }
            )
            
            # Create a new repository object
            repository, created = Repository.objects.update_or_create(
                third_party_id=repo.get('id'),
                defaults={
                    'name': repo.get('name'),
                    'full_name': repo_name,
                    'description': repo.get('description', ''),
                    'url': 'https://github.com/' + repo_name,
                    'private': repo.get('private', False),
                    'organization': organization
                }
            )
            if created:
                logging.info(f"Created new repository: {repo_name}")
            else:
                logging.info(f"Updated existing repository: {repo_name}")
        
        return JsonResponse({'status': 'Handled installation_repositories event'}, status=200)
    
    if action == 'removed':
        repositories_removed = payload.get('repositories_removed', [])
        for repo in repositories_removed:
            repo_name = repo.get('full_name')
            repo_id = repo.get('id')
            logging.info(f"GitHub App removed from repository: {repo_name} (ID: {repo_id})")
            repository = Repository.objects.get(full_name=repo_name)
            repository.delete()
    
    return JsonResponse({'status': 'Unhandled action for installation_repositories event'}, status=200)


@github_app.on(event_type='installation', actions=('created', 'deleted'))
def handle_installation_created(request, payload):
    """
    Handle the 'installation' event when a new installation is created.
    """
    installation = payload.get('installation')
    installation_id = installation.get('id')
    action = payload.get('action')
    repositories = payload.get('repositories', [])
    
    if action == 'created':
        for repo in repositories:
            repo_name = repo.get('full_name')
            repo_id = repo.get('id')
            logging.info(f"GitHub App installation created: {repo_name} (ID: {repo_id})")

            # get or create organization
            organization, created = Organization.objects.update_or_create(
                third_party_id=installation.get('id'),
                defaults={
                    'name': installation.get('account').get('login'),
                    'url': installation.get('account').get('html_url'),
                    'avatar_url': installation.get('account').get('avatar_url'),
                }
            )
            # Create a new repository object
            repository, created = Repository.objects.update_or_create(
                third_party_id=repo.get('id'),
                defaults={
                    'name': repo.get('name'),
                    'full_name': repo_name,
                    'description': repo.get('description', ''),
                    'url': 'https://github.com/' + repo_name,
                    'private': repo.get('private', False),
                    'organization': organization
                }
            )
            if created:
                logging.info(f"Created new repository: {repo_name}")
            else:
                logging.info(f"Updated existing repository: {repo_name}")
        
        return JsonResponse({'status': 'Handled installation event'}, status=200)

    if action == 'deleted':
        for repo in repositories:
            repo_name = repo.get('full_name')
            repo_id = repo.get('id')
            logging.info(f"GitHub App installation deleted: {repo_name} (ID: {repo_id})")
            repository = Repository.objects.get(full_name=repo_name)
            repository.delete()
    
    return JsonResponse({'status': 'Unhandled action for installation event'}, status=200)
