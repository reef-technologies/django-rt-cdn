from typing import List, Literal
from urllib.parse import unquote, urlparse

import requests

from django.core.files.base import ContentFile
from imagekit.cachefiles import ImageCacheFile
from imagekit.registry import generator_registry
from ninja import NinjaAPI, Schema
from ninja.responses import codes_4xx
from pydantic import PositiveInt
from pydantic.networks import HttpUrl

from .renderers import ImageRenderer
from .security import TokenAuth


FormatType = Literal['bmp', 'ico', 'jpeg', 'png', 'tiff', 'webp']


api = NinjaAPI(title='RT CDN API', version='1.0.0', auth=TokenAuth(), renderer=ImageRenderer())
session = requests.Session()


class Success(Schema):
    url: HttpUrl


class ErrorDetail(Schema):
    loc: List[str]
    msg: str
    type: str


class Error(Schema):
    detail: List[ErrorDetail]


@api.get('/image', tags=['Image processing'], response={200: Success, codes_4xx: Error})
def image(
    request,
    origin: HttpUrl,
    width: PositiveInt = None,
    format: FormatType = None,
    force: bool = False,
):
    response = session.get(origin)

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        if 400 <= exc.response.status_code < 500:
            return exc.response.status_code, {
                'detail': [
                    {
                        'loc': ['query', 'origin'],
                        'msg': str(exc),
                        'type': 'requests_error.http_4xx',
                    }
                ]
            }
        raise

    name = unquote(urlparse(response.url).path.lstrip('/'))
    content = response.content

    with ContentFile(content, name=name) as image_fd:
        if width is None:
            generator = generator_registry.get(
                'cdn:origin_resolution',
                source=image_fd,
                format=format,
            )
        else:
            generator = generator_registry.get(
                'cdn:thumbnail',
                source=image_fd,
                width=width,
                format=format,
                crop=False,
                upscale=False,
            )

        file = ImageCacheFile(generator)
        file.generate(force=force)
        setattr(request, 'image_file', file)

    return {'url': file.url}
