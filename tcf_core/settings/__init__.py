# pylint: disable=unused-wildcard-import,wildcard-import
"""
Django settings module for local development environment. This is the default
Django settings file that will be used in case the environment variable
`DJANGO_SETTINGS_MODULE` is not set.
"""
from .base import *


# django-silk settings
def custom_recording_logic(request):
    """
    Exclude API views for django-silk
    """
    return not request.path.startswith("/api")


# Performance profiling for non-API views during development
if os.environ.get("DJANGO_SETTINGS_MODULE") not in [
    "tcf_core.settings.dev",
    "tcf_core.settings.prod",
]:
    INSTALLED_APPS.append("silk")
    MIDDLEWARE.append("silk.middleware.SilkyMiddleware")
    SILKY_INTERCEPT_FUNC = custom_recording_logic
