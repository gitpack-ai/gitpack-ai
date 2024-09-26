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
    def get_code_review(self, code):
        prompt = """
            Review the following code and provide feedback with positive aspects and areas for improvement:

            Only provide a RFC8259 compliant JSON response. Follow this format without deviation. Do not include any other text or explanations. Also, provide json in raw string format without any quotes,
            ```
            {
                "overall": {
                    // overall feedback summary goes here.
                    "summary": "",
                    // positive feedback goes here. provide a list of string type. This section is optional. If you don't see significant positives skip this section.
                    "positives": ["", ""],
                    // areas of improvement goes here. provide a a list of string type. This section is optional. If you don't see any areas of improvements skip this section.
                    "improvements": ["", ""]
                },
                "inline_feedback": [
                        // line specific feedback goes here. use the diff notation to provide the absolute line number and diff offset
                        { 
                            // relative path of the file
                            "file_path": "",
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
                            // optional field to provide the suggested change for this line of code
                            "suggested_change": ""
                        },
                ],
            }
            ```

            === Code starts here

            %s

            === Code ends here
        """ % (code)
        #print('prompt:', prompt) 
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a code reviewer."},
                {"role": "user", "content": prompt}
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
                print("response: ", response_content)
                raise ValueError('No JSON response found in GPT-4 response')
            try:
                response_json = json.loads(response_json_str)
            except json.JSONDecodeError:
                print("response_json_str: ", response_json_str)
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

    # Extract the line numbers from the diff notation
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
            
            # Check if the code block starts at this line
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
                # else:
                #     # OpenAI is known to not return exact code block. It's generally correct but has small differences. 
                #     # So, it's best to call this good enough check. Ideally we should only have above check
                #     start_line = new_current_line if line.startswith('+') else old_current_line
                #     end_line = start_line + len(code_lines) - 1
                #     start_side = end_side = 'RIGHT' if line.startswith('+') else 'LEFT'
                #     logging.debug('** Did "good enough" check for extracting lines **')
                #     break
                
            
                logging.debug(f"potential_block len: {len(patch_lines[i:i+len(code_lines)])} code_block: {len(code_lines)}")
                logging.debug(f"potential_block:\n{potential_block}\n\n code_block:\n{code_block}")
            
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
