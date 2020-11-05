import pytest

from django.conf import settings as django_settings


def pytest_configure():
    django_settings.configure(DEBUG=True)


@pytest.fixture
def settings_empty(settings):
    settings.CDN_CACHE_ENDPOINT = ''
    settings.CDN_IMAGE_ENDPOINT = ''


@pytest.fixture
def settings_none(settings):
    settings.CDN_CACHE_ENDPOINT = None
    settings.CDN_IMAGE_ENDPOINT = None


@pytest.fixture
def settings_dummy(settings):
    settings.CDN_CACHE_ENDPOINT = 'https://example.com/cache/'
    settings.CDN_IMAGE_ENDPOINT = 'https://example.com/image/'
