from django.conf import settings
from .openai import OpenAIHelper
from .claude import ClaudeHelper

# Map of supported AI providers
AI_PROVIDERS = {
    'claude': ClaudeHelper,
    'openai': OpenAIHelper,
}

def get_ai_helper():
    """Factory function to get the appropriate AI helper based on settings"""
    ai_provider = getattr(settings, 'AI_PROVIDER', 'openai').lower()
    provider_class = AI_PROVIDERS.get(ai_provider, OpenAIHelper)
    return provider_class()
