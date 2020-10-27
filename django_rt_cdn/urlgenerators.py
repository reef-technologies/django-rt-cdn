from django.conf import settings
from django.db.models.fields.files import FieldFile
from environ import ImproperlyConfigured


def cdn_cache_url(obj_or_url):
    if not settings.CDN_CACHE_ENDPOINT:
        raise ImproperlyConfigured(
            "CDN cache entrypoint is disabled. To enable, please set 'CDN_CACHE_ENDPOINT'"
        )

    url = _get_url(obj_or_url)
    endpoint = _get_endpoint(settings.CDN_CACHE_ENDPOINT)

    return f'{endpoint}{url}'


def cdn_image_url(obj_or_url, width='auto'):
    if not settings.CDN_IMAGE_ENDPOINT:
        raise ImproperlyConfigured(
            "CDN image entrypoint is disabled. To enable, please set 'CDN_IMAGE_ENDPOINT'"
        )

    url = _get_url(obj_or_url)
    endpoint = _get_endpoint(settings.CDN_IMAGE_ENDPOINT)
    params = f'width={width}/'

    return f'{endpoint}{params}{url}'


def _get_endpoint(endpoint):
    sep = '' if settings.CDN_IMAGE_ENDPOINT.endswith('/') else '/'
    return f'{endpoint}{sep}'


def _get_url(obj_or_url):
    if isinstance(obj_or_url, FieldFile):
        return obj_or_url.url
    else:
        return str(obj_or_url)
