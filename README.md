django-rt-cdn
=============

Django app for a CDN solution based on [cf-workers-rt-cdn](https://github.com/reef-technologies/cf-workers-rt-cdn)

Dependencies:
-------------

* Cloudflare Workers RT CDN >= 1.0.1 < 2.0.0

ImageKit support:
-----------------

Add to the `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    'imagekit',
    'django_rt_cdn',
    ...
]

IMAGEKIT_CACHEFILE_NAMER = 'django_rt_cdn.contrib.imagekit.namers.cdn_file_namer'
IMAGEKIT_SPEC_CACHEFILE_NAMER = IMAGEKIT_CACHEFILE_NAMER
IMAGEKIT_CACHEFILE_DIR = ''
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = 'imagekit.cachefiles.backends.Simple'
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
```

Example of usage:

```python
from imagekit.cachefiles import ImageCacheFile
from imagekit.registry import generator_registry

...

generator = generator_registry.get(
    'cdn:thumbnail',
    source=instance.image,
    width=width,
    crop=False,
    upscale=False
)

file = ImageCacheFile(generator)
file.generate(force=True)
```
