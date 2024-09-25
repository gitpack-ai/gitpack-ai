from django.test import TestCase
from .lib.openai import OpenAIHelper


class TestOpenAIHelper(TestCase):
    
    def test_get_code_review(self):
        openai_helper = OpenAIHelper()

        # Load test data from a fixture file
        with open('gitpack/main/fixtures/test_code_review_query.txt', 'r') as file:
            test_query = file.read()

        overall_feedback, line_comments = openai_helper.get_code_review(test_query)
        
        from pprint import pprint
        pprint(overall_feedback)
        pprint(line_comments)

        self.assertIsNotNone(overall_feedback)
        self.assertIsNotNone(line_comments)

