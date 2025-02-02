from anthropic import Anthropic
import json, re
from django.conf import settings
import logging

class ClaudeHelper:
    def __init__(self):
        self.client = Anthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )
        # Get model settings with defaults
        self.model = getattr(settings, 'CLAUDE_MODEL', 'claude-3-opus-20240229')
        self.max_tokens = getattr(settings, 'CLAUDE_MAX_TOKENS', 1500)

    def get_code_review(self, files_changed):
        all_code = ""
        files_changed_dict = {}

        # Loop through each changed file
        for file in files_changed:
            if any(re.match(pattern, file.filename) for pattern in settings.CODE_REVIEW_IGNORE_PATTERNS):
                continue
            file_patch = file.patch
            files_changed_dict[file.filename] = file_patch
            all_code += f"File path: {file.filename}\n\nContent:\n{file.patch}\n\n"

        logging.debug('files_changed_dict:\n\n%s\n\n', json.dumps(files_changed_dict, indent=4, sort_keys=True))

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

Only provide feedback for significant and impactful issues. Avoid trivial feedback.
For multi-line code sections, provide feedback in a single feedback object.

=== Code to review ===

{all_code}

=== End code ===

Remember to provide only the JSON response with no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                system="You are a Staff or Principal level Software Engineer performing code reviews. Focus only on high-quality, impactful feedback."
            )
        except anthropic.APIConnectionError as e:
            logging.error('Network error when calling Claude API: %s', str(e))
            raise ValueError('Failed to connect to Claude API') from e
        except anthropic.APIError as e:
            logging.error('Claude API error: %s', str(e))
            raise ValueError('Claude API returned an error') from e
        except anthropic.RateLimitError as e:
            logging.error('Claude API rate limit exceeded: %s', str(e))
            raise ValueError('Claude API rate limit exceeded') from e
        except Exception as e:
            logging.error('Unexpected error calling Claude API: %s', str(e))
            raise ValueError('Unexpected error when calling Claude API') from e
        
        response_content = response.content[0].text
        try:
            response_json = json.loads(response_content)
        except json.JSONDecodeError:
            try:
                # Try to extract JSON if wrapped in code blocks
                response_json_str = re.search(r'^(?:(?:```json)|(?:```)|(?:json))(.*?)(?:```)?$', response_content, re.DOTALL).group(1)
                response_json = json.loads(response_json_str)
            except (AttributeError, json.JSONDecodeError):
                logging.error('Invalid JSON response from Claude. Response: %s', response_content)
                raise ValueError('Invalid JSON response from Claude')

        logging.debug('Claude response:\n\n%s\n\n', json.dumps(response_json, indent=4, sort_keys=True))

        return self._parse_claude_response(response_json, files_changed_dict)

    def _parse_claude_response(self, feedback_json, files_changed_dict):
        overall_feedback = f"## Code Review for this PR\n\n{feedback_json['summary']['summary']}\n\n"
        
        if feedback_json['summary'].get('positives'):
            if isinstance(feedback_json['summary']['positives'], list):
                positives = ''.join(f'- {s}\n' for s in feedback_json['summary']['positives'])
            else:
                positives = feedback_json['summary']['positives']
            overall_feedback += f"### Positives:\n\n{positives}\n\n"
            
        if feedback_json['summary'].get('improvements'):
            if isinstance(feedback_json['summary']['improvements'], list):
                improvements = ''.join(f'- {s}\n' for s in feedback_json['summary']['improvements'])
            else:
                improvements = feedback_json['summary']['improvements']
            overall_feedback += f"### Areas of Improvement:\n\n{improvements}\n\n"

        line_comments = []
        if feedback_json.get('inline_feedback'):
            for feedback in feedback_json['inline_feedback']:
                file_patch = files_changed_dict[feedback['file_path']]
                start_line, start_side, end_line, end_side = self._extract_line_numbers(file_patch, feedback['code_lines'])

                if start_line is None or end_line is None:
                    logging.error(f"Could not find the specified code lines in the patch. Feedback: {feedback}")
                    continue
                if feedback['start_side'] == feedback['end_side'] and start_line > end_line:
                    logging.error(f"Invalid extraction of line numbers. Feedback: {feedback}")
                    continue

                line_comments.append({
                    'body': f"{feedback['feedback']}",
                    'filename': feedback['file_path'],
                    'start_line': start_line,
                    'start_side': feedback['start_side'],
                    'end_line': end_line,
                    'end_side': feedback['end_side'],
                    'suggested_code_changes': feedback.get('suggested_code_changes', None)
                })

        return overall_feedback, line_comments

    def _extract_line_numbers(self, file_patch, code_lines):
        logging.debug(f"File patch: {file_patch}")
        logging.debug(f"Code lines: {code_lines}")
        
        patch_lines = file_patch.split('\n')
        code_block = '\n'.join(line.lstrip('+-').strip() for line in code_lines)
        
        new_current_line = old_current_line = 1
        start_line = end_line = None
        start_side = end_side = None

        start_code_line = code_lines[0].strip()
        
        for i, line in enumerate(patch_lines):
            if line.startswith('@@'):
                match = re.match(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
                if match:
                    old_current_line = int(match.group(1))
                    new_current_line = int(match.group(2))
                continue
            
            effective_line = line.strip()
            if not start_code_line.startswith('-') or not start_code_line.startswith('+'):
                effective_line = line[1:].strip()
            if start_line is None and effective_line == start_code_line:
                potential_block = '\n'.join(line.lstrip('+-').strip() for line in patch_lines[i:i+len(code_lines)])
                if potential_block.strip() == code_block.strip():
                    start_line = new_current_line if line.startswith('+') else old_current_line
                    end_line = start_line + len(code_lines) - 1
                    start_side = end_side = 'RIGHT' if line.startswith('+') else 'LEFT'
                    break
                
            if line.startswith('-'):
                old_current_line += 1
            elif line.startswith('+'):
                new_current_line += 1
            else:
                old_current_line += 1
                new_current_line += 1
        
        if start_line is None or end_line is None:
            return None, None, None, None

        return start_line, start_side, end_line, end_side
