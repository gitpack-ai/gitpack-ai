# GitPack AI

#### Automate Pull Request Reviews with AI 🪄
Get Faster, Smarter Code Reviews on Any GitHub Repo!

[https://gitpack.co](https://gitpack.co)


## Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/gitpack-ai/gitpack-ai)

Deploy GitPack AI quickly and easily with Render.com. Click the button above to start the deployment process.



## Prerequisites

- Docker
- OpenAI API Key
- Github App

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/gitpack-ai.git
   cd gitpack-ai
   ```

2. Create a `gitpack/.env` file and add the following environment variables:
   ```
   GITHUBAPP_ID=<your_github_app_id>
   GITHUBAPP_KEY=<your_github_app_private_key>
   GITHUB_WEBHOOK_SECRET=<your_github_webhook_secret>
   GITPACK_OPENAI_ORGANIZATION=<your_openai_organization>
   GITPACK_OPENAI_PROJECT=<your_openai_project>
   GITPACK_OPENAI_API_KEY=<your_openai_api_key>
   ```

3. Create a `frontend/.env.local` file and add the following:
   ```
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   NEXT_PUBLIC_GITHUB_APP_HANDLE=<name-of-your-github-app>
   ```

## Running the app

1. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. The services will be available at:
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`
   - Database: `localhost:5435`

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

Remember to update your environment variables with the new GitHub App details.

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
