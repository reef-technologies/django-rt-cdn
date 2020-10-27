from django.conf import settings
from django.core import checks


E001 = checks.Error(
    "Missing 'CDN_CACHE_ENDPOINT' setting.",
    hint="It should be set to CDN 'cache' endpoint or set to None.",
    id='django_rt_cdn.E001',
)


E002 = checks.Error(
    "Missing 'CDN_IMAGE_ENDPOINT' setting.",
    hint="It should be set to CDN 'image' endpoint or set to None.",
    id='django_rt_cdn.E002',
)


def check_cache_endpoint(app_configs, **kwargs):  # pragma: no cover
    if not hasattr(settings, 'CDN_CACHE_ENDPOINT'):
        return [E001]
    return []


def check_image_endpoint(app_configs, **kwargs):  # pragma: no cover
    if not hasattr(settings, 'CDN_IMAGE_ENDPOINT'):
        return [E002]
    return []
