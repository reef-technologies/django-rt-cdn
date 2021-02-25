import os
import uuid

from django.conf import settings
from pilkit.utils import suggest_extension


def cdn_file_namer(generator):
    """A namer that, given the following source file name with 100w resolution::

        photos/thumbnails/bulldog.jpg

    will generate a name like this::

        /path/to/generated/images/photos/thumbnails/bulldog.jpg/bulldog-100w.jpg

    where "/path/to/generated/images/" is the value specified by the
    ``IMAGEKIT_CACHEFILE_DIR`` setting.
    """
    width = getattr(generator, 'width', None)
    source_filename = getattr(generator.source, 'name', None)
    if source_filename is None:
        source_filename = str(uuid.uuid4().hex)

    if width is None:
        dir = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR, os.path.dirname(source_filename))
    else:
        dir = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR, '{}-cdn'.format(source_filename))

    ext = suggest_extension(source_filename, generator.format)
    if width is None:
        marker = ''
    else:
        marker = '-{}w'.format(width)

    basename = os.path.splitext(os.path.basename(source_filename))[0]
    return os.path.normpath(os.path.join(dir, ''.join([basename, marker, ext])))
