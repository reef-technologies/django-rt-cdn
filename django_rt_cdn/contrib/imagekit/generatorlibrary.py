from imagekit import ImageSpec
from imagekit.generatorlibrary import Thumbnail as ImageMagicThumbnail


class OriginResolution(ImageSpec):
    def __init__(self, format=None, **kwargs):
        if format is not None:
            self.format = format
        super().__init__(
            **kwargs,
        )


class Thumbnail(ImageMagicThumbnail):
    def __init__(
        self,
        width=None,
        height=None,
        anchor=None,
        crop=None,
        upscale=None,
        format=None,
        **kwargs,
    ):
        self.width = width
        if format is not None:
            self.format = format
        super().__init__(
            width=width,
            height=height,
            anchor=anchor,
            crop=crop,
            upscale=upscale,
            **kwargs,
        )
