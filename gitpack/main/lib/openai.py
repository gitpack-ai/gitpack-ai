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
                "inline_feedback": [
                        // Inline feedback goes here. Limit the inline feedback to only where there is important areas for improvement. Avoid providing feedback unless it is significant and very impactful. Avoid positive feedback.
                        { 
                            // relative path of the file
                            "file_path": "",
                            // actual line content of the code for which feedback is provided.
                            "actual_line_content": "",
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
        """ % (code)

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

        return self._parse_gpt_response(response_json)

    def _parse_gpt_response(self, feedback_json):
        overall_feedback = f"## Code Review for this PR\n\n{feedback_json['summary']['summary']}\n\n"
        if feedback_json['summary'].get('positives'):
            if type(feedback_json['summary']['positives']) is list:
                positives = ''.join(f'- {s}\n' for s in feedback_json['summary']['positives'])
            else:
                positives = feedback_json['summary']['positives']
            overall_feedback += f"### Positives:\n\n{positives}\n\n"
        if feedback_json['summary'].get('improvements'):
            #if type of feedback_json['summary']['improvements']) is list
            if type(feedback_json['summary']['improvements']) is list:
                improvements = ''.join(f'- {s}\n' for s in feedback_json['summary']['improvements'])
            else:
                improvements = feedback_json['summary']['improvements']
            overall_feedback += f"### Areas of Improvement:\n\n{improvements}\n\n"
        
        # Based on GPT feedback, add specific line comments if improvements are needed
        line_comments = []
        if feedback_json.get('inline_feedback'):
            for feedback in feedback_json['inline_feedback']:
                line_comments.append({
                    'body': f"{feedback['feedback']}",
                    'filename': feedback['file_path'],
                    'start_line': feedback['start_line'],
                    'start_side': feedback['start_side'],
                    'end_line': feedback['end_line'],
                    'end_side': feedback['end_side'],
                    'suggested_change': feedback.get('suggested_change', None)
                })
        
        return overall_feedback, line_comments
