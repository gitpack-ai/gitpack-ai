# GitPack AI
A Github AI Bot to be the first reviewer for your pull requests

## Installation

```bash
pip install -r requirements.txt
```


## Running the app

1. Set up environment variables:
   ```bash
   export GITHUBAPP_ID=<your_github_app_id>
   export GITHUBAPP_KEY=<your_github_app_private_key>
   export GITHUB_WEBHOOK_SECRET=<your_github_webhook_secret>
   export GITPACK_OPENAI_ORGANIZATION=<your_openai_organization>
   export GITPACK_OPENAI_PROJECT=<your_openai_project>
   export GITPACK_OPENAI_API_KEY=<your_openai_api_key>
   ```

2. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

3. The app should now be running at `http://localhost:8000`



## Create a Github App
To create a GitHub App for Gitpack AI, follow these steps:

1. Go to your GitHub account settings.
2. Navigate to "Developer settings" > "GitHub Apps" > "New GitHub App".
3. Fill out the form with the following details:
   - GitHub App name: "Gitpack AI" (or your preferred name)
   - Homepage URL: Your app's homepage or repository URL
   - Webhook URL: The URL where your app will receive webhook events (e.g., `https://your-domain.com/webhook/`)
   - Webhook secret: Generate a secure random string for this
   - Permissions:
     - Repository permissions:
       - Contents: Read
       - Issues: Read & Write
       - Pull requests: Read & Write
   - Subscribe to events:
     - Pull request
     - Pull request review
     - Pull request review comment
4. Create the GitHub App.
5. After creation, you'll see your App ID. Note this down.
6. Generate a private key for your app and download it.
7. Install the app on your repositories.

### Setting up the webhook:
1. In your app settings, ensure the Webhook URL is set to where your Django app will handle incoming webhooks (e.g., `https://your-domain.com/webhook/`).
2. Generate a secure random string for the Webhook secret. You can use a command like this:
   ```bash
   openssl rand -hex 20
   ```
3. Save this secret in your app settings and in your environment variables.

Remember to update your environment variables with the new GitHub App details:

## Usage

To use the Gitpack AI bot for automatic PR reviews, follow these steps:

1. Ensure the GitHub App is installed on your repository.

2. Install the GitHub App on your repository:
   - Go to your GitHub repository
   - Click on "Settings" in the top menu
   - Select "Integrations" from the left sidebar
   - Click on "Add GitHub App" in the "Installed GitHub Apps" section
   - Find "Gitpack AI" (or the name you chose) in the list
   - Click "Install"


3. When a new pull request is opened or updated in your repository, the bot will automatically:
   - Analyze the changes in the pull request
   - Generate an overall review of the changes
   - Provide line-specific comments and suggestions

The bot automatically triggers on new PRs or updates to existing PRs. There's no need for manual intervention to initiate a review.

