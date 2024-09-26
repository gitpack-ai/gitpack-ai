from openai import OpenAI
import json, re
from django.conf import settings
import logging

class OpenAIHelper:

    def __init__(self):
        self.client = OpenAI(
            organization=settings.OPENAI_ORGANIZATION,
            project=settings.OPENAI_PROJECT,
            api_key=settings.OPENAI_API_KEY
        )

    # OpenAI GPT-4 helper to review code
    def get_code_review(self, files_changed):

        all_code = ""

        files_changed_dict = {}

        # Loop through each changed file
        for file in files_changed:
            # Get the file content and diff
            #file_content = file.raw_url
            # Check if the file should be ignored based on CODE_REVIEW_IGNORE_PATTERNS
            if any(re.match(pattern, file.filename) for pattern in settings.CODE_REVIEW_IGNORE_PATTERNS):
                continue
            file_patch = file.patch
            files_changed_dict[file.filename] = file_patch
            all_code += f"File path: {file.filename}\n\nContent:\n{file.patch}\n\n"

        logging.debug('files_changed_dict:\n\n%s\n\n', json.dumps(files_changed_dict, indent=4, sort_keys=True))
        # logging.debug(f"Query:\n\n{all_code}\n\n")

        prompt = """
            Review the following code and provide feedback with positive aspects and areas for improvement:

            Only provide a RFC8259 compliant JSON response. Follow this format without deviation. Do not include any other text or explanations. Also, provide json in raw string format without any quotes,
            ```
            {
                "inline_feedback": [
                        // Inline feedback goes here. Limit the inline feedback to only where there is important areas for improvement. Avoid providing feedback unless it is significant and very impactful. Avoid positive feedback. Feedback for multiple lines of code is encouraged and should be provided in a single feedback object.
                        { 
                            // relative path of the file
                            "file_path": "",
                            // actual lines of the code content for which feedback is provided. This should be an array of strings and each item in the array should be a line of code.
                            "code_lines": ["", ""],
                            // start side of the diff for the multiple line feedback. Response should be strictly either "LEFT" or "RIGHT"
                            "start_side": "",
                            // start line number of the code in the file. This has to be an absolute line number. It's important to provide the correct line number based on the diff offset.
                            "start_line": "",
                            // end side of the diff for the multiple line feedback. Response should be strictly either "LEFT" or "RIGHT"
                            "end_side": "",
                            // end line number of the code. For single line feedback, start_line and end_line should be same. This has to be an absolute line number. It's important to provide the correct line number based on the diff offset.
                            "end_line": "",
                            // actual feedback for this line of code
                            "feedback": "",
                            // optional field to provide the suggested code changes. This should be strictly lines of code and any other text provided as commented code.
                            "suggested_code_changes": ""
                        },
                ],
                "summary": {
                    // feedback summary goes here. Don't just repeat the inline feedback, but provide a strong summary and comment on the overall changes.
                    "summary": "",
                    // positive feedback goes here. This section is optional. If you don't see significant positives skip this section.
                    "positives": ["", ""],
                    // areas of improvement goes here. This section is optional. If you don't see any areas of improvements skip this section.
                    "improvements": ["", ""]
                },
            }
            ```

            === Code starts here

            %s

            === Code ends here
        """ % (all_code)

        #logging.debug('Prompt: %s', prompt)

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a Staff or Principal level Software Engineer. In this contexrt you are acting as a code reviewer. You provide only the high quality feedback and avoid trivial feedback."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=1500
        )
        response_content = response.choices[0].message.content
        try:
            response_json = json.loads(response_content)
        except json.JSONDecodeError:
            try:
                response_json_str = re.search(r'^(?:(?:```json)|(?:```)|(?:json))(.*?)(?:```)?$', response_content, re.DOTALL).group(1)
            except AttributeError:
                logging.error('No JSON response found in GPT-4 response')
                raise ValueError('No JSON response found in GPT-4 response')
            try:
                response_json = json.loads(response_json_str)
            except json.JSONDecodeError:
                logging.error('Invalid JSON response from GPT-4. Response: %s', response_json_str)
                raise ValueError('Invalid JSON response from GPT-4')
        
        logging.debug('GPT-4 response:\n\n%s\n\n', json.dumps(response_json, indent=4, sort_keys=True))

        return self._parse_gpt_response(response_json, files_changed_dict)

    def _parse_gpt_response(self, feedback_json, files_changed_dict):
        overall_feedback = f"## Code Review for this PR\n\n{feedback_json['summary']['summary']}\n\n"
        if feedback_json['summary'].get('positives'):
            if isinstance(feedback_json['summary']['positives'], list):
                positives = ''.join(f'- {s}\n' for s in feedback_json['summary']['positives'])
            else:
                positives = feedback_json['summary']['positives']
            overall_feedback += f"### Positives:\n\n{positives}\n\n"
        if feedback_json['summary'].get('improvements'):
            #if type of feedback_json['summary']['improvements']) is list
            if isinstance(feedback_json['summary']['improvements'], list):
                improvements = ''.join(f'- {s}\n' for s in feedback_json['summary']['improvements'])
            else:
                improvements = feedback_json['summary']['improvements']
            overall_feedback += f"### Areas of Improvement:\n\n{improvements}\n\n"
        
        # Based on GPT feedback, add specific line comments if improvements are needed
        line_comments = []
        if feedback_json.get('inline_feedback'):
            for feedback in feedback_json['inline_feedback']:
                # start_line and end_line provided by GPT have been known to be unreliable. 
                # So, we need to extract the line numbers based on the diff notation in the file patch and the code lines provided in the GPT response
                file_patch = files_changed_dict[feedback['file_path']]
                start_line, start_side, end_line, end_side = self._extract_line_numbers(file_patch, feedback['code_lines'])

                if start_line is not None and end_line is not None:
                    line_comments.append({
                        'body': f"{feedback['feedback']}",
                        'filename': feedback['file_path'],
                        'start_line': start_line,
                        'start_side': feedback['start_side'],
                        'end_line': end_line,
                        'end_side': feedback['end_side'],
                        'suggested_code_changes': feedback.get('suggested_code_changes', None)
                    })
                else:
                    logging.error(f"Could not find the specified code lines in the patch. Feedback: {feedback}")
        
        return overall_feedback, line_comments

    # Extract the line numbers from the diff notation
    def _extract_line_numbers(self, file_patch, code_lines):
        # logging.debug(f"File patch: {file_patch}")
        # logging.debug(f"Code lines: {code_lines}")
        
        lines = file_patch.split('\n')
        start_line = end_line = None
        start_side = end_side = None
        new_current_line = 1
        old_current_line = 1
        start_code_line = code_lines[0].strip()
        end_code_line = code_lines[-1].strip()
        for line in lines:
            if line.startswith('@@'):
                # Parse the diff header
                # Extract the old and new line numbers from the diff header
                match = re.match(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
                if match:
                    old_start = int(match.group(1))
                    new_start = int(match.group(2))
                else:
                    logging.warning(f"Failed to parse diff header: {line}")
                    continue
                
                new_current_line = int(new_start)
                old_current_line = int(old_start)
                continue
            
            if line.startswith('-'):
                side = 'LEFT'
            elif line.startswith('+'):
                side = 'RIGHT'
            else:
                side = 'RIGHT'  # Unchanged lines are considered on the right side

            effective_line = line.strip()
            if not start_code_line.startswith('-') or not start_code_line.startswith('+'):
                effective_line = line[1:].strip()
            if start_line is None and effective_line == start_code_line:
                if side == 'RIGHT':
                    start_line = new_current_line
                else:
                    start_line = old_current_line
                start_side = side
                
            if not end_code_line.startswith('-') or not end_code_line.startswith('+'):
                effective_line = line[1:].strip()
            if end_line is None and effective_line == end_code_line:   
                if side == 'RIGHT':
                    end_line = new_current_line
                else:
                    end_line = old_current_line
                end_side = side
            if start_line is not None and end_line is not None:
                break
            
            if line.startswith('-'):
                old_current_line += 1
            else:
                new_current_line += 1
            
        
        if start_line is None or end_line is None:
            
            return None, None, None, None

        return start_line, start_side, end_line, end_side