from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.shortcuts import redirect
from django.db import transaction

class CustomGitHubOAuth2Adapter(GitHubOAuth2Adapter):
    
    def get_scope(self, request, *args, **kwargs):
        return ['read:user', 'user:email']

class GitHubLogin(SocialLoginView):
    adapter_class = CustomGitHubOAuth2Adapter
    callback_url = settings.GITHUB_CALLBACK_URL
    client_class = OAuth2Client

    @transaction.atomic
    def login(self):
        # Ensure all related objects are saved within a transaction
        self.user = self.serializer.validated_data['user']
        if hasattr(self.user, 'app'):
            self.user.app.save()
        return super().login()

def github_login_redirect(request):
    github_login_url = f'https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_CALLBACK_URL}'
    return redirect(github_login_url)