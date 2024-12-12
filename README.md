# GitPack AI

#### Automate Pull Request Reviews with AI 🪄
Get Faster, Smarter Code Reviews on Any GitHub Repo!

[https://gitpack.co](https://gitpack.co)


## Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/gitpack-ai/gitpack-ai)

Deploy GitPack AI quickly and easily with Render.com. Click the button above to start the deployment process.


## Prerequisites

- Docker
- AI Provider API Key (OpenAI or Claude)
- Github App


# Deployment Guide

This guide explains how to deploy and test GitPack AI using Render and GitHub. Follow these steps in order to ensure proper setup and avoid common issues.

## Components

1. **Web Service/Backend**
   - Processes GitHub events and generates AI reviews
   - Required for PR review functionality
   - Requires database connection

2. **Frontend** (Optional)
   - Manages repositories at admin level
   - Not required for PR review functionality
   - Backend deployment alone is sufficient for PR reviews

3. **Database**
   - Required for backend/web service
   - Stores repository and organization data

## Deployment Order (Important!)

1. Create GitHub App (get credentials)
2. Deploy database
3. Deploy backend with proper environment variables
4. Install GitHub App on repositories
5. Deploy frontend (optional)

This order is crucial to avoid RepositoryNotFound exceptions, as the backend must be ready to handle installation webhooks.

## GitHub App Setup

1. Go to GitHub Settings > Developer Settings > GitHub Apps > New GitHub App
2. Fill in basic app information:
   - Name: (e.g., GitPack AI)
   - Homepage URL: (can be temporary, will update later)
   - Webhook URL: (can be temporary, will update later)
   - Webhook Secret: Generate with `openssl rand -hex 20`

3. Set permissions:
   - Repository permissions:
     * Contents: Read
     * Pull requests: Read & Write
   - Organization permissions:
     * Members: Read

4. Subscribe to events:
   - Pull request
   - Installation
   - Installation repositories

5. Save and collect credentials:
   - Note down App ID
   - Download private key (.pem file)
   - Generate and save webhook secret
   - Note Client ID and Secret (if using frontend)

## Environment Variables

### Backend (.env)
```bash
# Environment
ENVIRONMENT=production  # Must be 'production' on Render

# GitHub App Configuration (https://github.com/settings/apps)
GITHUBAPP_ID=            # From GitHub App settings
GITHUBAPP_KEY=           # Contents of the .pem file
GITHUB_WEBHOOK_SECRET=   # From openssl rand -hex 20

# AI Provider Selection
GITPACK_AI_PROVIDER=claude  # or 'openai'

# If using Claude
GITPACK_ANTHROPIC_API_KEY=  # Your Anthropic API key

# If using OpenAI
GITPACK_OPENAI_ORGANIZATION=
GITPACK_OPENAI_PROJECT=
GITPACK_OPENAI_API_KEY=

# GitHub OAuth (https://github.com/settings/developers)
# Only needed if deploying frontend
GITHUB_CLIENT_ID=        # From GitHub OAuth App
GITHUB_CLIENT_SECRET=    # From GitHub OAuth App
```

### Frontend (.env.local) - Optional
```bash
NEXT_PUBLIC_API_URL=backend-url
NEXT_PUBLIC_GITHUB_APP_HANDLE=your-github-app-name
```

### Switching AI Providers

You can switch between AI providers by updating environment variables:

#### OpenAI
```env
GITPACK_AI_PROVIDER=openai
GITPACK_OPENAI_ORGANIZATION=<your_openai_organization>
GITPACK_OPENAI_PROJECT=<your_openai_project>
GITPACK_OPENAI_API_KEY=<your_openai_api_key>
```

#### Claude
```env
GITPACK_AI_PROVIDER=claude
GITPACK_ANTHROPIC_API_KEY=<your_anthropic_api_key>
```

After changing providers:
1. Update environment variables in Render dashboard
2. Redeploy the service
3. Test with a new PR to verify the change


## Deploy on Render

### Quick Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/gitpack-ai/gitpack-ai)

### Testing with a Forked Repository

1. Fork and Update Deploy URL
   - Fork the repository
   - Update the repo name in the Quick Deploy URL
   - For forked repos, change `gitpack-ai/gitpack-ai` to `your-username/gitpack-ai`

2. Initial Setup
   - Click the Deploy to Render button
   - Sign up on Render if needed
   - The Blueprint will create:
     * PostgreSQL database
     * Web service (backend)

3. Configure Web Service
   - Blueprint deployment will initially fail for backend
   - Go to Render dashboard → Projects
   - Select the web service
   - Navigate to Environment in left panel
   - Add required environment variables:
     * ENVIRONMENT=production
     * GITHUBAPP_ID
     * GITHUBAPP_KEY
     * GITHUB_WEBHOOK_SECRET
     * GITPACK_AI_PROVIDER
     * GITPACK_ANTHROPIC_API_KEY (if using Claude)
     * GITHUB_CLIENT_ID (if deploying frontend)
     * GITHUB_CLIENT_SECRET (if deploying frontend)
   - Click "Manual Deploy" → "Deploy latest commit"

4. Verify Deployment
   - Wait for service to deploy completely
   - Check Events tab in Render for logs
   - Verify webhook endpoint is accessible

5. Test Integration
   - Install GitHub App on your repository
   - Create a test pull request
   - Check web service logs for review generation



## Local Development

1. Clone repository:
```bash
git clone https://github.com/your-username/gitpack-ai.git
cd gitpack-ai
```

2. Set up environment:
   - Copy `.env.example` to `gitpack/.env`
   - Copy `.env.local.example` to `frontend/.env.local`
   - Update variables with your credentials

3. Run with Docker:
```bash
docker-compose up --build
```

Services will be available at:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Database: localhost:5435

## Usage

### Installing the GitHub App

1. Go to your GitHub repository
2. Click on "Settings" in the top menu
3. Select "Integrations" from the left sidebar
4. Click on "Add GitHub App" in the "Installed GitHub Apps" section
5. Find "GitPack AI" (or your app name) in the list
6. Click "Install"

### Automatic PR Reviews

The bot automatically triggers on:
- New pull requests
- Updates to existing pull requests

For each trigger, the bot will:
1. Analyze the changes in the pull request
2. Generate an overall review of the changes
3. Provide line-specific comments and suggestions
4. Add improvement recommendations where applicable

No manual intervention is needed - the bot automatically reviews all PRs in repositories where it's installed.

### Review Features

The bot provides:
1. Overall Code Review
   - Architecture assessment
   - Code quality evaluation
   - Best practices recommendations

2. Line-Specific Comments
   - Detailed explanations of issues
   - Code improvement suggestions
   - Performance considerations

3. Automated Suggestions
   - Code fixes
   - Style improvements
   - Documentation recommendations


## Common Issues

### RepositoryNotFound Errors
This usually occurs when webhooks are processed before the backend is ready:
1. Ensure this deployment order:
   - Database fully provisioned first
   - Backend deployed with migrations complete
   - GitHub App installed last
2. If error occurs:
   - Check backend logs for migration status
   - Verify organization and repository records exist
   - Reinstall GitHub App if needed

### Webhook Issues
- Verify webhook secret matches in GitHub App and backend
- Check webhook URL is accessible
- Review webhook delivery logs in GitHub App settings
- Common webhook errors:
  * 404: Wrong webhook URL or backend not deployed
  * 401: Incorrect webhook secret
  * 500: Database not ready or migration issues

### Authentication Issues
- Verify all GitHub-related environment variables
- Ensure OAuth callback URLs are correct
- Check frontend API URL configuration
- Common auth errors:
  * Invalid redirect_uri: Callback URL mismatch
  * Invalid client_id: Wrong GitHub App credentials
  * State mismatch: Session issues



## Support

For issues and questions:
1. Check the Common Issues section above
2. Review Render logs for specific error messages
3. [Open an issue](https://github.com/gitpack-ai/gitpack-ai/issues) if needed
