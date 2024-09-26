import hmac
import hashlib
import json
from functools import wraps
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from github import Github, Auth, GithubIntegration

class GithubApp:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GithubApp, cls).__new__(cls)
            cls._instance.event_handlers = {}
            # cls._instance.github_installation = cls._instance.init_github()
        return cls._instance

    def get_github_client(self, payload):
        """
        Initialize and return a Github object using the GitHub App's private key.
        """
        if 'installation' in payload:
            installation_id = payload['installation']['id']
            auth = Auth.AppAuth(settings.GITHUBAPP_ID, settings.GITHUBAPP_KEY).get_installation_auth(installation_id)
            return Github(auth=auth)
        raise RuntimeError('Invalid payload')
        

    def on(self, event_type, actions=None):
        """
        Decorator to register event handlers for GitHub webhook events.
        """
        def decorator(func):
            if isinstance(actions, tuple):
                for action in actions:
                    key = (event_type, action)
                    self.event_handlers[key] = func
            else:
                key = (event_type, actions)
                self.event_handlers[key] = func
            return func
        return decorator

    def verify_github_signature(self, request):
        """
        Verify the GitHub webhook signature.
        """
        github_secret = settings.GITHUB_WEBHOOK_SECRET
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature:
            return False

        expected_signature = 'sha256=' + hmac.new(
            github_secret.encode(),
            request.body,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    @csrf_exempt
    def github_webhook(self, request):
        """
        Main view to handle GitHub webhook requests.
        """
        if request.method != 'POST':
            return HttpResponseForbidden('Method not allowed')

        if not self.verify_github_signature(request):
            return HttpResponseForbidden('Invalid signature')

        event_type = request.headers.get('X-GitHub-Event')
        if not event_type:
            return HttpResponseForbidden('Missing event type')

        payload = json.loads(request.body)
        action = payload.get('action')
        handler = self.event_handlers.get((event_type, action)) or self.event_handlers.get((event_type, None))
        if handler:
            return handler(request, payload)
        else:
            return JsonResponse({'status': f"Unhandled event: {event_type}.{action}"}, status=200)

