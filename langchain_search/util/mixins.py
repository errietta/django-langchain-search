
from django.conf import settings
from langchain_search.util.langchain import get_llm_filter


class LangChainSearchMixin():
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get(
            settings.LANGCHAIN_SEARCH_QUERY_PARAM,
            'q'
        )
        if search_query:
            filter = get_llm_filter(
                queryset,
                search_query,
                **settings.LANGCHAIN_SEARCH_MODEL_SETTINGS,
            )
            queryset = queryset.filter(**filter)
        return queryset
