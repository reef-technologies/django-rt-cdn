import os

from django.conf import settings
from pilkit.utils import suggest_extension


def cdn_file_namer(generator):
    """A namer that, given the following source file name with 100w::

        photos/thumbnails/bulldog.jpg

    will generate a name like this::

        /path/to/generated/images/photos/thumbnails/bulldog.jpg/bulldog-100w.jpg

    where "/path/to/generated/images/" is the value specified by the
    ``IMAGEKIT_CACHEFILE_DIR`` setting.
    """
    source_filename = getattr(generator.source, 'name', None)

    if source_filename is None or os.path.isabs(source_filename):
        # Generally, we put the file right in the cache file directory.
        dir = settings.IMAGEKIT_CACHEFILE_DIR
    else:
        # For source files with relative names (like Django media files),
        # use the source's name to create the new filename.
        dir = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR, '{}-cdn'.format(source_filename))

    ext = suggest_extension(source_filename or '', generator.format)
    marker = getattr(generator, 'width', None)
    if marker is None:
        marker = generator.get_hash()[:12]
    else:
        marker = '{}w'.format(marker)

    basename = os.path.splitext(os.path.basename(source_filename))[0]
    return os.path.normpath(os.path.join(dir, '{}-{}{}'.format(basename, marker, ext)))
