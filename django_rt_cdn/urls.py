from django.urls import path


try:
    from .contrib.ninja.api import api
except ImportError:
    urlpatterns = []
else:
    urlpatterns = [path('', api.urls)]
