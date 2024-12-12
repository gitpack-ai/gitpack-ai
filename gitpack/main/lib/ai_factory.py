from django.conf import settings
from .openai import OpenAIHelper
from .claude import ClaudeHelper
import logging

# Map of supported AI providers
AI_PROVIDERS = {
    'claude': ClaudeHelper,
    'openai': OpenAIHelper,
}

def get_ai_helper():
    """
    Factory function to get the appropriate AI helper based on settings.
    Handles initialization errors gracefully.
    
    Returns:
        An instance of the configured AI helper class
        
    Raises:
        ValueError: If provider initialization fails
    """
    ai_provider = getattr(settings, 'AI_PROVIDER', 'openai').lower()
    provider_class = AI_PROVIDERS.get(ai_provider, OpenAIHelper)
    
    try:
        return provider_class()
    except Exception as e:
        logging.error('Failed to initialize AI provider %s: %s', ai_provider, str(e))
        raise ValueError(f'Failed to initialize AI provider {ai_provider}') from e
