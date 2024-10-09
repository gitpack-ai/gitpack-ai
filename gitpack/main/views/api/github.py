from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Organization, Repository

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.models import SocialAccount
from github import Github, GithubIntegration
from django.conf import settings

class GitHubRepositoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def _repos_response(self, repos):
        repositories = []
        for repo in repos:
            org = repo.organization
            organization, created = Organization.objects.update_or_create(
                third_party_id=org.id,
                defaults={
                    'name': org.name,
                    'description': org.description,
                    'url': org.html_url,
                    'avatar_url': org.avatar_url
                }
            )
            repository, created = Repository.objects.update_or_create(
                third_party_id=repo.id,
                defaults={
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description,
                    'url': repo.html_url,
                    'private': repo.private,
                    'organization': organization
                }
            )
            repositories.append({
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description,
                'url': repo.html_url,
                'private': repo.private,
                'organization': {
                    'login': repo.organization.login,
                    'name': repo.organization.name,
                    'description': repo.organization.description,
                    'url': repo.organization.html_url,
                    'avatar_url': repo.organization.avatar_url,
                    'is_paid': organization.pricing.name != 'Free' if organization.pricing else False
                }
            })
        return repositories
    
    def _get_repos_with_app_installed(self, access_token):
        g = Github(access_token)
        user = g.get_user()
        
        repos_with_app = []
        github_integration = GithubIntegration(settings.GITHUBAPP_ID, settings.GITHUBAPP_KEY)
        installations = github_integration.get_installations()
        for installation in installations:
            repositories = self._repos_response(installation.get_repos()) 
            repos_with_app.extend(repositories)
        
        return repos_with_app
    
    def get(self, request):
        try:
            # Get the user's GitHub social account
            social_account = SocialAccount.objects.get(user=request.user, provider='github')
            
            # Get the access token
            access_token = social_account.socialtoken_set.first().token
            
            if bool(request.GET.get('is_app_installed', False)):
                return Response(self._get_repos_with_app_installed(access_token), status=status.HTTP_200_OK)
            # Create a GitHub instance using the access token
            g = Github(access_token)
            
            # Get the authenticated user
            user = g.get_user()
            
            # Get the repositories the user has access to
            repositories = self._repos_response(user.get_repos())
            
            return Response(repositories, status=status.HTTP_200_OK)
        
        except SocialAccount.DoesNotExist:
            return Response(
                {"error": "GitHub account not connected"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GitHubOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the user's GitHub social account
            social_account = SocialAccount.objects.get(user=request.user, provider='github')
            
            # Get the access token
            access_token = social_account.socialtoken_set.first().token
            
            # Create a GitHub instance using the access token
            g = Github(access_token)
            
            # Get the authenticated user
            user = g.get_user()
            
            # Get the organizations the user belongs to
            organizations = []
            for org in user.get_orgs():
                organization, created = Organization.objects.update_or_create(
                    third_party_id=org.id,
                    defaults={
                        'name': org.name,
                        'description': org.description,
                        'url': org.html_url,
                        'avatar_url': org.avatar_url
                    }
                )
                organizations.append({
                    'login': org.login,
                    'name': org.name,
                    'description': org.description,
                    'url': org.html_url,
                    'avatar_url': org.avatar_url,
                    'is_paid': organization.pricing.name != 'Free' if organization.pricing else False
                })
            
            return Response(organizations, status=status.HTTP_200_OK)
        
        except SocialAccount.DoesNotExist:
            return Response(
                {"error": "GitHub account not connected"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

