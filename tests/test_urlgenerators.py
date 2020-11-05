import pytest

from django_rt_cdn.urlgenerators import cdn_cache_url, cdn_image_url


@pytest.mark.usefixtures('settings_empty')
@pytest.mark.parametrize(
    'url',
    (
        '',
        '/',
        '/media/image.jpg',
        'http://example.com/image.jpg',
    ),
)
class TestSettingsEmpty:
    def test_cdn_cache_url(self, url):
        assert cdn_cache_url(url) == url

    def test_image_cache_url(self, url):
        assert cdn_image_url(url) == url


@pytest.mark.usefixtures('settings_none')
@pytest.mark.parametrize(
    'url',
    (
        '',
        '/',
        '/media/image.jpg',
        'http://example.com/image.jpg',
    ),
)
class TestSettingsNone:
    def test_cdn_cache_url(self, url):
        assert cdn_cache_url(url) == url

    def test_image_cache_url(self, url):
        assert cdn_image_url(url) == url


@pytest.mark.usefixtures('settings_dummy')
class TestSettingsDummy:
    @pytest.mark.parametrize(
        'url, url_expected',
        (
            ('', 'https://example.com/cache/'),
            ('/', 'https://example.com/cache/'),
            ('/media/image.jpg', 'https://example.com/cache/media/image.jpg'),
            (
                'http://example.com/image.jpg',
                'https://example.com/cache/http://example.com/image.jpg',
            ),
        ),
    )
    def test_cdn_cache_url(self, url, url_expected):
        assert cdn_cache_url(url) == url_expected

    @pytest.mark.parametrize(
        'url, url_expected',
        (
            ('', 'https://example.com/image/width=auto/'),
            ('/', 'https://example.com/image/width=auto/'),
            (
                '/media/image.jpg',
                'https://example.com/image/width=auto/media/image.jpg',
            ),
            (
                'http://example.com/image.jpg',
                'https://example.com/image/width=auto/http://example.com/image.jpg',
            ),
        ),
    )
    def test_image_cache_url_width_auto(self, url, url_expected):
        assert cdn_image_url(url) == url_expected

    @pytest.mark.parametrize(
        'url, url_expected',
        (
            ('', 'https://example.com/image/width=100/'),
            ('/', 'https://example.com/image/width=100/'),
            ('/media/image.jpg', 'https://example.com/image/width=100/media/image.jpg'),
            (
                'http://example.com/image.jpg',
                'https://example.com/image/width=100/http://example.com/image.jpg',
            ),
        ),
    )
    def test_image_cache_url_width_100(self, url, url_expected):
        assert cdn_image_url(url, width=100) == url_expected
