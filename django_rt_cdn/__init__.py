# flake8: noqa
from importlib.metadata import version

import django


__version__ = version('django-rt-cdn')

if django.VERSION < (3, 2):
    default_app_config = 'django_rt_cdn.apps.RtCdnConfig'
