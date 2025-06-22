import logging
from typing import TypedDict
from django.db.models.query import QuerySet

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from langchain_search.util.django import (
    create_filter_model_from_django,
)

logger = logging.getLogger(__name__)


class ModelSettings(TypedDict):
    """
    Settings for the model, including the model name and any additional parameters.
    """

    model: str = "gpt-4.1"
    temperature: float = 0.0
    max_tokens: int = 1000
    timeout: int = 60
    max_retries: int = 2


def get_llm_filter(queryset: QuerySet, query_text: str, **kwargs: ModelSettings) -> dict:
    """
    Generate a filter using an LLM based on the provided query text.
    EXAMPLE:

    ```
        query_text = "at least $80000 medium size company remote in Matthewshaven"

        {
            'salary__gte': 80000,
            'remote': True,
            'location__ilike': 'Matthewshaven',
            'company_employee_count__gte': 51,
            'company_employee_count__lte': 250
        }
    ```

    ```
    query_text = "salary of at least $100000 in San Francisco"

    {
        'salary__gte': 100000,
        'location__ilike': 'San Francisco'
    }
    ```
    """
    opts = {
        "model": kwargs.get("model", "gpt-4.1"),
        "temperature": kwargs.get("temperature", 0.0),
        "max_tokens": kwargs.get("max_tokens", 1000),
        "timeout": kwargs.get("timeout", 60),
        "max_retries": kwargs.get("max_retries", 2),
    }

    llm = ChatOpenAI(**opts)#.with_structured_output(
        #method="json_mode",
    #) # Not sure why this doesn't work

    template = """
    You are a filter generator.
    Given a query, generate a JSON object that can be used to filter a table in a database.
    Each value should only be used on a single field based on what is most suitable
    where the values belong to one of the field examples, the field should take priority.
    {format_instructions}
    {query}
    """
    filter_model = create_filter_model_from_django(queryset.model)

    parser = JsonOutputParser(pydantic_object=filter_model)
    prompt = PromptTemplate(
        template=template,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    logger.info("LLM prompt: %s", prompt)

    chain = LLMChain(llm=llm, prompt=prompt)

    logger.info("query  text: %s", query_text)
    response = chain.run({"query": query_text})

    logger.info("LLM response: %s", response)

    response = parser.parse(response)

    smart_filter = {k: v for k, v in response.items() if v not in (None, 0, "", [], {})}

    return smart_filter
