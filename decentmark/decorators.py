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
from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import Http404
from django.shortcuts import resolve_url, get_object_or_404
from typing import Callable

from decentmark.models import UnitUsers


def model_object_required(model: models.Model, field_pk: str=None, field_out: str=None):
    """
    Decorator for views that retrieves a model object, 404'ing if it does not exist.
    By default expects kwarg of '<model_name>_id' which it uses to do the lookup, also removing it from kwargs.
    It then stores the object into the requests object as the field '<model_name>'.
    """

    if not field_pk:
        field_pk = model._meta.model_name + "_id"
    if not field_out:
        field_out = model._meta.model_name

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            setattr(request, field_out, get_object_or_404(model, pk=kwargs[field_pk]))
            del kwargs[field_pk]
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def unit_user_passes_test(test_func: Callable[[UnitUsers], bool]) -> ...:
    """
    Decorator for views that checks that the unit_user passes the test.
    Adds unit_user to the request object if it does not exist.
    It obtains the unit and user from the request object.
    Also makes sure the user is part of the unit
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'unit_user'):
                setattr(request, 'unit_user', UnitUsers.objects.filter(user=request.user, unit=request.unit).first())
            if request.unit_user and test_func(request.unit_user):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

def unit_permissions_required(test_func: Callable[[UnitUsers], bool]):
    return unit_user_passes_test(test_func)

def modify_request(key: str, mod_func):
    """
    Save the result of a function to the requests object
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            setattr(request, key, mod_func(request))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

