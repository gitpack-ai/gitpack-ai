from django.urls import path

from main.views import index
from main.views.api import status, github
from main.views.webhooks.github_webhook_events import github_app

urlpatterns = [
    path("", index.index, name="index"),
    
    # APIs
    path("api/status/", status.StatusView.as_view(), name="api_status"),
    path("api/github/orgs", github.GitHubOrganizationsView.as_view(), name="github_orgs"),
    path("api/github/repos", github.GitHubRepositoriesView.as_view(), name="github_repos"),
    path("api/github/repo/<int:repo_id>/toggle", github.GitHubRepositoryToggleView.as_view(), name="github_repo_toggle"),

    # Webhooks
    path('webhook/github/', github_app.github_webhook, name='github_webhook'),
]