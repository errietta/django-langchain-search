from django.apps import AppConfig
from django.conf import settings

class LangChainSearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "langchain_search"

    def ready(self):
        # Set default settings if not already set
        if not hasattr(settings, 'LANGCHAIN_SEARCH_QUERY_PARAM'):
            setattr(settings, 'LANGCHAIN_SEARCH_QUERY_PARAM', 'q')
        if not hasattr(settings, 'LANGCHAIN_SEARCH_MODEL_SETTINGS'):
            setattr(settings, 'LANGCHAIN_SEARCH_MODEL_SETTINGS', {})
