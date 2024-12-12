import os
import certifi
from anthropic import Anthropic
import httpx
import json

def test_claude():
    api_key = os.environ.get('GITPACK_ANTHROPIC_API_KEY')
    print(f"Using API key: {api_key[:10]}...")  # Only print first 10 chars for security
    
    # Initialize Claude helper with a custom httpx client that skips SSL verification
    client = Anthropic(
        api_key=api_key,
        http_client=httpx.Client(verify=False)  # Note: Not recommended for production
    )
    
    # Load test data from the fixture file
    with open('gitpack/main/fixtures/test_code_review.json', 'r') as f:
        test_files = json.load(f)

    # Build the prompt
    all_code = ""
    for file_path, patch in test_files.items():
        all_code += f"File path: {file_path}\n\nContent:\n{patch}\n\n"

    prompt = f"""Review the following code and provide feedback with positive aspects and areas for improvement.

You must respond with a RFC8259 compliant JSON object following this exact format. Do not include any other text or explanations:

{{
    "inline_feedback": [
        {{
            "file_path": "relative path of the file",
            "code_lines": ["array of actual code lines receiving feedback"],
            "start_side": "LEFT or RIGHT",
            "start_line": "absolute line number",
            "end_side": "LEFT or RIGHT", 
            "end_line": "absolute line number",
            "feedback": "specific feedback for this code section",
            "suggested_code_changes": "optional suggested code improvements"
        }}
    ],
    "summary": {{
        "summary": "overall code review summary",
        "positives": ["array of positive aspects"],
        "improvements": ["array of areas needing improvement"]
    }}
}}

=== Code to review ===

{all_code}

=== End code ===

Remember to provide only the JSON response with no additional text."""

    print("\nSending request to Claude...")
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        system="You are a Staff or Principal level Software Engineer performing code reviews. Focus only on high-quality, impactful feedback."
    )
    
    print("\nClaude's Response:")
    print(response.content[0].text)
    return "Test completed"

if __name__ == '__main__':
    # Disable SSL verification warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_claude()
