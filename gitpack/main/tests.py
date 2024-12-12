 from django.test import TestCase, override_settings
from .lib.ai_factory import get_ai_helper
import json

class FilesChangedTest:
    def __init__(self, filename, patch):
        self.filename = filename
        self.patch = patch


class TestAIHelper(TestCase):
    
    @override_settings(AI_PROVIDER='openai')
    def test_openai_code_review(self):
        ai_helper = get_ai_helper()

        # Load test data from a fixture json file
        with open('gitpack/main/fixtures/test_code_review.json', 'r') as file:
            test_content = file.read()
            test_json = json.loads(test_content)
            files_changed = [FilesChangedTest(filename, patch) for filename, patch in test_json.items()]

        overall_feedback, line_comments = ai_helper.get_code_review(files_changed)

        self.assertIsNotNone(overall_feedback)
        self.assertIsNotNone(line_comments)

    @override_settings(AI_PROVIDER='claude')
    def test_claude_code_review(self):
        ai_helper = get_ai_helper()

        # Load test data from a fixture json file
        with open('gitpack/main/fixtures/test_code_review.json', 'r') as file:
            test_content = file.read()
            test_json = json.loads(test_content)
            files_changed = [FilesChangedTest(filename, patch) for filename, patch in test_json.items()]

        overall_feedback, line_comments = ai_helper.get_code_review(files_changed)

        self.assertIsNotNone(overall_feedback)
        self.assertIsNotNone(line_comments)


class TestExtractLineNumbers(TestCase):
    """Test line number extraction logic that's shared between AI providers"""

    def setUp(self):
        self.ai_helper = get_ai_helper()

    def test_extract_line_numbers_simple(self):
        file_patch = """@@ -100,6 +100,47 @@\n     },\n ]\n \n+# Loggers\n+# Logging configuration that logs to console if DEBUG is True\n+if DEBUG:\n+    LOGGING = {\n+        'version': 1,\n+        'disable_existing_loggers': False,\n+        'formatters': {\n+            'colored': {\n+                '()': 'colorlog.ColoredFormatter',\n+                'format': '%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s',\n+                'log_colors': {\n+                    'DEBUG': 'cyan',\n+                    'INFO': 'green',\n+                    'WARNING': 'yellow',\n+                    'ERROR': 'red',\n+                    'CRITICAL': 'red,bg_white',\n+                },\n+            },\n+        },\n+        'handlers': {\n+            'console': {\n+                'class': 'colorlog.StreamHandler',\n+                'formatter': 'colored',\n+                'level': 'DEBUG',\n+            },\n+        },\n+        'loggers': {\n+            '': {  # Root logger\n+                'handlers': ['console'],\n+                'level': 'DEBUG',\n+            },\n+            'django': {\n+                'handlers': ['console'],\n+                'level': 'INFO',\n+                'propagate': False,\n+            },\n+        },\n+    }\n+\n+\n+\n \n # Internationalization\n # https://docs.djangoproject.com/en/5.1/topics/i18n/"""
        code_lines =  [
            "if DEBUG:",
            "    LOGGING = {"
        ]

        result = self.ai_helper._extract_line_numbers(file_patch=file_patch, code_lines=code_lines)
        print('result: ', result)

        self.assertEqual(result, (105, 'RIGHT', 106, 'RIGHT'))

    def test_extract_line_numbers_complex(self):
        file_patch = """@@ -1,11 +1,13 @@\n-from .github_webhook import GithubApp\n+from ._github_webhook_wrapper import GithubApp\n from django.http import JsonResponse\n from main.lib.openai import OpenAIHelper\n+import logging\n+import github\n \n github_app = GithubApp()\n \n # Handle pull request opened\n-@github_app.on(event_type='pull_request', action='opened')\n+@github_app.on(event_type='pull_request', actions=('opened', 'synchronize'))\n def handle_pull_request_opened(request, payload):\n     # Get the repository and pull request number from the payload\n     repo_full_name = payload['repository']['full_name']\n@@ -22,6 +24,8 @@ def handle_pull_request_opened(request, payload):\n     # Get the list of files changed in the pull request\n     files_changed = pull_request.get_files()\n \n+    latest_commit = pull_request.get_commits()[0]\n+\n     query = \"\"\n \n     # Loop through each changed file\n@@ -31,79 +35,47 @@ def handle_pull_request_opened(request, payload):\n         file_patch = file.patch\n         query += f\"File path: {file.filename}\\n\\nContent:\\n{file.patch}\\n\\n\"\n \n+    logging.debug(f\"Query: {query}\")\n+\n     # Initialize OpenAIHelper\n     openai_helper = OpenAIHelper()\n-    feedback_json = openai_helper.get_code_review(query)\n-\n-    overall_feedback = f\"## Code Review for PR: {pr_title}\\n\\n{feedback_json['overall']['summary']}\\n\\n\"\n-    if feedback_json['overall'].get('positives'):\n-        if type(feedback_json['overall']['positives']) is list:\n-            positives = ''.join(f'- {s}\\n' for s in feedback_json['overall']['positives'])\n-        else:\n-            positives = feedback_json['overall']['positives']\n-        overall_feedback += f\"### Positives:\\n\\n{positives}\\n\\n\"\n-    if feedback_json['overall'].get('improvements'):\n-        #if type of feedback_json['overall']['improvements']) is list\n-        if type(feedback_json['overall']['improvements']) is list:\n-            improvements = ''.join(f'- {s}\\n' for s in feedback_json['overall']['improvements'])\n-        else:\n-            improvements = feedback_json['overall']['improvements']\n-        overall_feedback += f\"### Areas of Improvement:\\n\\n{improvements}\\n\\n\"\n-    \n-    # Based on GPT feedback, add specific line comments if improvements are needed\n-    line_comments = []\n-    if feedback_json.get('inline_feedback'):\n-        for feedback in feedback_json['inline_feedback']:\n-            line_comments.append({\n-                'body': f\"{feedback['feedback']}\",\n-                'filename': feedback['file_path'],\n-                'start_line': feedback['start_line'],\n-                'start_side': feedback['start_side'],\n-                'end_line': feedback['end_line'],\n-                'end_side': feedback['end_side'],\n-                'suggested_change': feedback.get('suggested_change', None)\n-            })\n-\n-    # Post overall review comment\n-    pull_request.create_issue_comment(overall_feedback)\n+    overall_feedback, line_comments = openai_helper.get_code_review(query)\n \n-    print('line_comments:', line_comments, 'pull_request.head.sha:', pull_request.head.sha)\n-    latest_commit = pull_request.get_commits()[0]\n     # Post line-specific comments\n     for comment in line_comments:\n-        if comment['start_line'] == comment['end_line']:\n-            pull_request.create_review_comment(\n-                body=comment['body'], \n-                commit=latest_commit,\n-                path=comment['filename'], \n-                line=comment['start_line'], \n-                side=comment['start_side']\n-            )\n-        else:\n-            pull_request.create_review_comment(\n-                body=comment['body'], \n-                commit=latest_commit,\n-                path=comment['filename'], \n-                line=comment['end_line'], \n-                side=comment['end_side'],\n-                start_line=comment['start_line'], \n-                start_side=comment['start_side']\n-            )  \n+        try:\n+            if comment['start_line'] == comment['end_line']:\n+                pull_request.create_review_comment(\n+                    body=comment['body'], \n+                    commit=latest_commit,\n+                    path=comment['filename'], \n+                    line=comment['start_line'], \n+                    side=comment['start_side']\n+                )\n+            else:\n+                pull_request.create_review_comment(\n+                    body=comment['body'], \n+                    commit=latest_commit,\n+                    path=comment['filename'], \n+                    line=comment['end_line'], \n+                    side=comment['end_side'],\n+                    start_line=comment['start_line'], \n+                    start_side=comment['start_side']\n+                )\n+        except github.GithubException as e:\n+            if e.status == 422 and 'Validation Failed' in str(e):\n+                # Handle validation failed exception\n+                logging.error(f\"Validation failed when creating review comment: {e}\")\n+                # You might want to skip this comment or try an alternative approach\n+                continue\n+            else:\n+                # Handle other GitHub exceptions\n+                logging.error(f\"GitHub API error when creating review comment: {e}\")\n+                # You might want to retry or handle the error in some way\n+                raise\n \n-    return JsonResponse({'status': f\"Handled pull_request.opened: {pr_number}\"}, status=200)\n+    # Post overall review comment\n+    pull_request.create_issue_comment(overall_feedback)  \n \n-# Handle issue opened\n-@github_app.on(event_type='issues', action='opened')\n-def handle_issue_opened(request, payload):\n-    issue_title = payload['issue']['title']\n-    issue_url = payload['issue']['html_url']\n-    print(f\"Issue opened: {issue_title} ({issue_url})\")\n-    return JsonResponse({'status': f\"Handled issues.opened: {issue_title}\"}, status=200)\n+    return JsonResponse({'status': f\"Handled pull_request.opened: {pr_number}\"}, status=200)\n \n-# Additional events can be handled in a similar way\n-@github_app.on(event_type='pull_request', action='closed')\n-def handle_pull_request_closed(request, payload):\n-    pr_title = payload['pull_request']['title']\n-    pr_url = payload['pull_request']['html_url']\n-    print(f\"Pull request closed: {pr_title} ({pr_url})\")\n-    return JsonResponse({'status': f\"Handled pull_request.closed: {pr_title}\"}, status=200)
        """

        # invalid lines of code. doesnt match with diff
        code_lines =  [
                "# Post line-specific comments",
                "for comment in line_comments:",
                "    try:",
                "        if comment['start_line'] == comment['end_line']:",
                "            pull_request.create_review_comment(",
                "                body=comment['body'],",
                "                commit=latest_commit,",
                "                path=comment['filename'],",
                "                line=comment['start_line'],",
                "                side=comment['start_side']",
                "            )",
                "        else:",
                "            pull_request.create_review_comment(",
                "                body=comment['body'],",
                "                commit=latest_commit,",
                "                path=comment['filename'],",
                "                line=comment['end_line'],",
                "                side=comment['end_side'],",
                "                start_line=comment['start_line'],",
                "                start_side=comment['start_side']",
                "            )",
                "    except github.GithubException as e:",
                "        if e.status == 422 and 'Validation Failed' in str(e):",
                "            # Handle validation failed exception",
                "            logging.error(f\"Validation failed when creating review comment: {e}\")",
                "            # You might want to skip this comment or try an alternative approach",
                "            continue",
                "        else:",
                "            # Handle other GitHub exceptions",
                "            logging.error(f\"GitHub API error when creating review comment: {e}\")",
                "            # You might want to retry or handle the error in some way",
                "            raise"
            ]

        result = self.ai_helper._extract_line_numbers(file_patch=file_patch, code_lines=code_lines)

        #self.assertEqual(result, (44, 'RIGHT', 75, 'RIGHT'))
        self.assertEqual(result, (None, None, None, None))

    def test_extract_line_numbers_another(self):
        file_patch = """@@ -100,6 +100,47 @@\n     },\n ]\n \n+# Loggers\n+# Logging configuration that logs to console if DEBUG is True\n+if DEBUG:\n+    LOGGING = {\n+        'version': 1,\n+        'disable_existing_loggers': False,\n+        'formatters': {\n+            'colored': {\n+                '()': 'colorlog.ColoredFormatter',\n+                'format': '%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s',\n+                'log_colors': {\n+                    'DEBUG': 'cyan',\n+                    'INFO': 'green',\n+                    'WARNING': 'yellow',\n+                    'ERROR': 'red',\n+                    'CRITICAL': 'red,bg_white',\n+                },\n+            },\n+        },\n+        'handlers': {\n+            'console': {\n+                'class': 'colorlog.StreamHandler',\n+                'formatter': 'colored',\n+                'level': 'DEBUG',\n+            },\n+        },\n+        'loggers': {\n+            '': {  # Root logger\n+                'handlers': ['console'],\n+                'level': 'DEBUG',\n+            },\n+            'django': {\n+                'handlers': ['console'],\n+                'level': 'INFO',\n+                'propagate': False,\n+            },\n+        },\n+    }\n+\n+\n+\n \n # Internationalization\n # https://docs.djangoproject.com/en/5.1/topics/i18n/\n@@ -123,6 +164,25 @@\n \n DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'\n \n+CODE_REVIEW_IGNORE_PATTERNS = [\n+    '.*\.md',\n+    '.*\.txt',\n+    '.*\.json',\n+    '.*\.yml',\n+    '.*\.yaml',\n+    '.*\.ini',\n+    '.*\.cfg',\n+    '.*\.conf',\n+    '.*\.log',\n+    '.*\.pid',\n+    '.*\.lock',\n+    '.*\.tmp',\n+    '.*\.bak',\n+    '.*\.old',\n+    '.*\.save',\n+    '.*\.backup',\n+]\n+\n GITHUBAPP_ID = os.environ.get('GITHUBAPP_ID')\n GITHUBAPP_KEY = os.environ.get('GITHUBAPP_KEY')\n if not GITHUBAPP_KEY:
        """

        code_lines =  ['CODE_REVIEW_IGNORE_PATTERNS = [', "    '.*\\.md',", "    '.*\\.txt',", "    '.*\\.json',", "    '.*\\.yml',", "    '.*\\.yaml',", "    '.*\\.ini',", "    '.*\\.cfg',", "    '.*\\.conf',", "    '.*\\.log',", "    '.*\\.pid',", "    '.*\\.lock',", "    '.*\\.tmp',", "    '.*\\.bak',", "    '.*\\.old',", "    '.*\\.save',", "    '.*\\.backup',", ']']

        result = self.ai_helper._extract_line_numbers(file_patch=file_patch, code_lines=code_lines)

        self.assertEqual(result, (167, 'RIGHT', 184, 'RIGHT'))
