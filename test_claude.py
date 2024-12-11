import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gitpack'))

from main.lib.claude import ClaudeHelper
from django.conf import settings

# Configure Django settings
settings.configure(
    ANTHROPIC_API_KEY=os.environ.get('GITPACK_ANTHROPIC_API_KEY'),
    CODE_REVIEW_IGNORE_PATTERNS=[
        '.*\.md',
        '.*\.txt',
        '.*\.json',
        '.*\.yml',
        '.*\.yaml',
    ]
)

def test_claude():
    # Initialize Claude helper
    claude = ClaudeHelper()
    
    # Simple test data
    test_files = [
        type('TestFile', (), {
            'filename': 'test.py',
            'patch': '''@@ -1,3 +1,7 @@
def hello():
-    print("Hello")
+    print("Hello, World!")
+
+def goodbye():
+    print("Goodbye!")
'''
        })()
    ]

    # Get code review
    print("Getting code review...")
    overall_feedback, line_comments = claude.get_code_review(test_files)
    
    print("\nOverall Feedback:")
    print(overall_feedback)
    print("\nLine Comments:")
    for comment in line_comments:
        print(f"\nFile: {comment['filename']}")
        print(f"Lines {comment['start_line']}-{comment['end_line']}")
        print(f"Feedback: {comment['body']}")

if __name__ == '__main__':
    test_claude()
