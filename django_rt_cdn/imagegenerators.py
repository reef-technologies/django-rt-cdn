try:
    from imagekit import register

    from .contrib.imagekit.generatorlibrary import OriginResolution, Thumbnail
except ImportError:
    pass
else:
    register.generator('cdn:thumbnail', Thumbnail)
    register.generator('cdn:origin_resolution', OriginResolution)
