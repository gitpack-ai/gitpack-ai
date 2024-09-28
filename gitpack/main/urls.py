from django.urls import path

from main.views import index
from main.views.api import status
from main.views.webhooks.github_webhook_events import github_app

urlpatterns = [
    path("", index.index, name="index"),
    path("api/status/", status.StatusView.as_view(), name="api_status"),

    # Webhooks
    path('webhook/github/', github_app.github_webhook, name='github_webhook'),
]