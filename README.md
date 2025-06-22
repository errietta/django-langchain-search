# Installation


This project runs with `uv`.
```
pip install uv
uv sync --frozen
```

To add to your django project
Add this to apps: `'langchain_search'`

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