from django.urls import path

from main.views import index
from main.views.github_webhook_events import github_app

urlpatterns = [
    path("", index.index, name="index"),
    path('webhook/github/', github_app.github_webhook, name='github_webhook'),
]