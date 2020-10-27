try:
    from imagekit import register

    from .contrib.imagekit.generatorlibrary import Thumbnail
except ImportError:
    pass
else:
    register.generator('cdn:thumbnail', Thumbnail)
