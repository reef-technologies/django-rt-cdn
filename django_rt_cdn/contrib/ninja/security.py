from django.conf import settings
from ninja.security import APIKeyHeader


class TokenAuth(APIKeyHeader):
    param_name = getattr(settings, 'CDN_API_TOKEN_HEADER', 'Authorization')

    def authenticate(self, request, key):
        token = getattr(settings, 'CDN_API_TOKEN', None)
        if token is None:
            return ''
        header = 'ApiKey {}'.format(token)
        if key == header:
            return token
        return None
