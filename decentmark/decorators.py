from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import Http404
from django.shortcuts import resolve_url, get_object_or_404


def model_object_required(model: models.Model, field_pk: str=None, field_out: str=None):
    if not field_pk:
        field_pk = model._meta.model_name + "_id"
    if not field_out:
        field_out = model._meta.model_name
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            kwargs[field_out] = get_object_or_404(model, pk=kwargs[field_pk])
            del kwargs[field_pk]
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
