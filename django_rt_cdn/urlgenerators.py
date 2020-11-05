from django.conf import settings
from django.db.models.fields.files import FieldFile


def cdn_cache_url(obj_or_url):
    if settings.CDN_CACHE_ENDPOINT:
        endpoint = _get_endpoint(settings.CDN_CACHE_ENDPOINT)
    else:
        endpoint = ''

    url = _get_url(obj_or_url)
    if endpoint:
        url = url.lstrip('/')

    return f'{endpoint}{url}'


def cdn_image_url(obj_or_url, width='auto'):
    if settings.CDN_IMAGE_ENDPOINT:
        endpoint = _get_endpoint(settings.CDN_IMAGE_ENDPOINT)
        params = f'width={width}/'
    else:
        endpoint = ''
        params = ''

    url = _get_url(obj_or_url)
    if endpoint:
        url = url.lstrip('/')

    return f'{endpoint}{params}{url}'


def _get_endpoint(endpoint):
    sep = '' if endpoint.endswith('/') else '/'
    return f'{endpoint}{sep}'


def _get_url(obj_or_url):
    if isinstance(obj_or_url, FieldFile):
        return obj_or_url.url
    else:
        return str(obj_or_url)
