import pytest

from django_rt_cdn.contrib.ninja import ImageIn


class TestImageIn:
    @pytest.mark.parametrize(
        ('origin', 'expected'),
        [
            ('https://example.com/origin.jpg', 'origin.jpg'),
            ('https://example.com/deeply/nested/origin.jpg', 'deeply/nested/origin.jpg'),
        ],
    )
    def test_default_path(self, origin, expected):
        image_in = ImageIn(origin=origin)

        assert image_in.path == expected

    def test_setting_path(self):
        image_in = ImageIn(origin='https://example.com/origin.jpg', path='custom.jpg')

        assert image_in.path == 'custom.jpg'
