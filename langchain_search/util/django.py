import decimal

from django.db.models import (
    BooleanField,
    CharField,
    DecimalField,
    FloatField,
    IntegerField,
    TextField,
    DateTimeField,
)
from pydantic import create_model


def create_filter_model_from_django(model_class):
    field_definitions = {}
    for field in model_class._meta.get_fields():
        if field.is_relation or not hasattr(field, "get_internal_type"):
            continue

        name = field.name

        if isinstance(field, (CharField, TextField)):
            name = f"{name}__icontains"
            field_definitions[name] = (str | None, None)
        elif isinstance(field, BooleanField):
            field_definitions[name] = (bool | None, None)
        elif isinstance(field, (IntegerField)):
            field_definitions[f"{name}__gte"] = (int | None, None)
            field_definitions[f"{name}__lte"] = (int | None, None)
        elif isinstance(field, (FloatField)):
            field_definitions[f"{name}__gte"] = (float | None, None)
            field_definitions[f"{name}__lte"] = (float | None, None)
        elif isinstance(field, (DecimalField)):
            field_definitions[f"{name}__gte"] = (decimal.Decimal | None, None)
            field_definitions[f"{name}__lte"] = (decimal.Decimal | None, None)
        elif isinstance(field, DateTimeField):
            field_definitions[f"{name}__gte"] = (str | None, None)
            field_definitions[f"{name}__lte"] = (str | None, None)

    return create_model(f"{model_class.__name__}Filter", **field_definitions)
