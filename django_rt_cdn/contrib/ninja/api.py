from typing import List, Literal, Union
from urllib.parse import unquote, urlparse

import requests

from django.conf import settings
from django.core.files.base import ContentFile
from imagekit.cachefiles import ImageCacheFile
from imagekit.registry import generator_registry
from imagekit.utils import get_by_qname
from ninja import NinjaAPI
from ninja.responses import codes_4xx
from ninja.schema import Schema, validator
from pydantic import PositiveInt
from pydantic.networks import HttpUrl

from .security import TokenAuth


FormatType = Literal['bmp', 'ico', 'jpeg', 'png', 'tiff', 'webp']


api = NinjaAPI(title='RT CDN API', version='1.0.0', auth=TokenAuth())


class ImageIn(Schema):
    origin: HttpUrl
    path: str = ""
    width: PositiveInt = None
    format: FormatType = None
    force: bool = False

    @validator('path', pre=True, always=True)
    def default_path(cls, v, *, values, **kwargs):
        return v or unquote(urlparse(values['origin']).path.lstrip('/'))


class ImageOut(ImageIn):
    url: HttpUrl


class ErrorDetail(Schema):
    loc: List[str]
    msg: str
    type: str


class Error(Schema):
    detail: Union[str, List[ErrorDetail]]


@api.exception_handler(Exception)
def exception_handler(request, exc):
    return api.create_response(request, {'detail': str(exc)}, status=500)


@api.post('/images', tags=['Images'], response={200: ImageOut, codes_4xx: Error})
def images(request, image_in: ImageIn):
    image_input_processor_func = getattr(settings, 'CDN_IMAGE_INPUT_PROCESSOR', None)
    if image_input_processor_func is not None:
        get_by_qname(image_input_processor_func, 'image input processor')(image_in)

    kwargs = getattr(settings, 'CDN_IMAGE_REQUEST_ARGS', {'timeout': 5.0})
    response = requests.get(image_in.origin, **kwargs)

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

    with ContentFile(response.content, name=image_in.path) as image_fd:
        if image_in.width is None:
            generator = generator_registry.get(
                'cdn:origin_resolution',
                source=image_fd,
                format=image_in.format,
            )
        else:
            generator = generator_registry.get(
                'cdn:thumbnail',
                source=image_fd,
                width=image_in.width,
                format=image_in.format,
                crop=False,
                upscale=False,
            )

        file = ImageCacheFile(generator)
        file.generate(force=image_in.force)

    image_out = ImageOut(
        url=file.url,
        origin=response.url,
        width=image_in.width,
        format=image_in.format,
        force=image_in.force,
    )

    image_output_processor_func = getattr(settings, 'CDN_IMAGE_OUTPUT_PROCESSOR', None)
    if image_output_processor_func is not None:
        get_by_qname(image_output_processor_func, 'image output processor')(image_out)

    return image_out
