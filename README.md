django-rt-cdn
=============

Django app for a CDN solution based on [cf-workers-rt-cdn](https://github.com/reef-technologies/cf-workers-rt-cdn)

Dependencies:
-------------

* Cloudflare Workers RT CDN >= 1.0.1 < 2.0.0
* Django ImageKit for image processing (optional)
* Django Ninja for an API (optional)

Django ImageKit support:
------------------------

## Installation

```
pip install django-rt-cdn[imagekit]
```

## Configuration

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

## Usage

```python
from django.db import models
from django.dispatch import receiver
from imagekit.cachefiles import ImageCacheFile
from imagekit.registry import generator_registry


class Image(models.Model):
    image = models.ImageField(upload_to='images')

    
@receiver(models.signals.post_save, sender=Image)
def image_post_save(sender, instance, using, **kwargs):
    generator = generator_registry.get(
        'cdn:thumbnail',
        source=instance.image,
        width=100,
        crop=False,
        upscale=False
    )

    file = ImageCacheFile(generator)
    file.generate(force=True)
```

Django Ninja support:
---------------------

## Installation

```
pip install django-rt-cdn[ninja]
```

It also installs ImageKit.

## Configuration

The same as for ImageKit.

## Usage

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.sites import site
from django.urls import include, path


urlpatterns = [
    path('admin/', site.urls),
    path('', include('django.contrib.auth.urls')),
    path('cdn/', include('django_rt_cdn.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

```
curl "http://127.0.0.1:8000/cdn/image?origin=https%3A%2F%2Fexample.com%2Fimage.jpg&width=100" -H  "Accept: application/json"
```
