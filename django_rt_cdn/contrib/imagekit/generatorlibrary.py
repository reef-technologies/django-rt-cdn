from imagekit.generatorlibrary import Thumbnail as ImageMagicThumbnail


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
        super(Thumbnail, self).__init__(
            width=width,
            height=height,
            anchor=anchor,
            crop=crop,
            upscale=upscale,
            **kwargs,
        )
