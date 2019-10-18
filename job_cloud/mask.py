from warnings import warn
import datetime
import os
import random
import time
from PIL import Image, ImageDraw


class ImageMask:
    """
    ImageMask

    :param kwargs: image_text, width, height, font

    Required: font
    """
    def __init__(self, **kwargs):
        self._image_text = kwargs.get('image_text', None)
        self._width = kwargs.get('width', 250)
        self._height = kwargs.get('height', 250)
        self._font = kwargs.get('font', None)

        if not self._font:
            raise TypeError("Missing required field 'font'")

        self._tmp_storage = kwargs.get('tmp_storage', '.')
        self._mask_file = None

    def generate(self):
        """
        Generate mask file

        :return: filename of created mask
        """
        if not self._image_text:
            return None

        image = Image.new('RGB', (self._width, self._height), color=(0, 0, 0))
        drawer = ImageDraw.Draw(image)
        self._image_text.draw_mask_placeholder(drawer)

        filename = "%d.%d" % (int(time.mktime(datetime.datetime.now().timetuple())), random.randint(0, 1000))
        self._mask_file = "%s/%s.png" % (self._tmp_storage, filename)

        image.save(self._mask_file)

        return self._mask_file

    def __del__(self):
        try:
            if self._mask_file and os.path.exists(self._mask_file):
                os.remove(self._mask_file)
        except OSError:
            warn("Unable to remove mask file")
