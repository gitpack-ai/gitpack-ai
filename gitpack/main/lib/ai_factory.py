from django.conf import settings
from .openai import OpenAIHelper
from .claude import ClaudeHelper

def get_ai_helper():
    """Factory function to get the appropriate AI helper based on settings"""
    ai_provider = getattr(settings, 'AI_PROVIDER', 'openai').lower()
    
    if ai_provider == 'claude':
        return ClaudeHelper()
    else:  # default to OpenAI
        return OpenAIHelper()
