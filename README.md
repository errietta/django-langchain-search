# Overview

This project uses langchain (currently only OpenAI) to search a Django model.
Simply use LangChainSearchMixin in your view, and let the user perform
a query with the `?q=` parameter.
Example:
```
http://127.0.0.1:8000/api/jobs/?q=Engineer jobs posted after or on June 22 2025 salary minimum 40000 hybrid
```

The human language query will be converted to your model fields using LangChain
and ChatGPT.

# Installation


This project runs with `uv`.
```
pip install uv
uv sync --frozen
```

To add to your django project
Add this to apps: `'langchain_search'`


You need to also set your openai key

```
export OPENAI_API_KEY=....
```


# Usage example

```
from .models import Job
from rest_framework import generics
from .serializers import JobSerializer
from langchain_search import LangChainSearchMixin

# Add mixin here
class JobListAPI(LangChainSearchMixin, generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
```

Example project: https://github.com/errietta/django-langchain-search-example