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

        #logging.debug('Prompt: %s', prompt)

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
                logging.error('No JSON response found in GPT-4 response')
                raise ValueError('No JSON response found in GPT-4 response')
            try:
                response_json = json.loads(response_json_str)
            except json.JSONDecodeError:
                logging.error('Invalid JSON response from GPT-4. Response: %s', response_json_str)
                raise ValueError('Invalid JSON response from GPT-4')
        
        logging.debug('GPT-4 response: %s', response_json)

        return response_json
