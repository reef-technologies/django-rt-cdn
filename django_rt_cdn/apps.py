from django.apps import AppConfig
from django.core import checks
from django.utils.translation import ugettext_lazy as _

from .checks import check_cache_endpoint, check_image_endpoint


class RtCdnConfig(AppConfig):  # pragma: no cover
    name = 'django_rt_cdn'
    verbose_name = _('RT CDN')

    def ready(self):
        checks.register(check_cache_endpoint)
        checks.register(check_image_endpoint)
