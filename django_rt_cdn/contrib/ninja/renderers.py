from mimetypes import guess_type

from accept_types import get_best_match
from ninja.renderers import JSONRenderer
from ninja.responses import codes_2xx


class ImageRenderer(JSONRenderer):
    media_type = 'application/json'
    charset = 'utf-8'

    def render(self, request, data, *, response_status):
        if response_status in codes_2xx:
            media_type, charset = guess_type(data['url'])
            if media_type is None:
                media_type = 'image/jpeg'
            if charset is None:
                charset = 'utf-8'

            accept_header = request.headers.get('Accept')
            accept_types = [self.__class__.media_type, media_type]
            if get_best_match(accept_header, accept_types) == media_type:
                self.media_type = media_type
                self.charset = charset
            else:
                self._reset_content_type()
        else:
            self._reset_content_type()

        if self.media_type == self.__class__.media_type:
            return super().render(request, data, response_status=response_status)
        else:
            return self._get_image_file_content(request)

    def _reset_content_type(self):
        self.media_type = self.__class__.media_type
        self.charset = self.__class__.charset

    @classmethod
    def _get_image_file_content(cls, request):
        image_file = getattr(request, 'image_file')
        with image_file.file as image_fd:
            return image_fd.read()
