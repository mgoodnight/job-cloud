import pytest
import re
import os
from job_cloud.mask import ImageMask
from job_cloud.text import ImageText


def test_type_error_no_font():
    with pytest.raises(TypeError):
        ImageText()


def test_generate():
    font = "%s/../fonts/arial-black.ttf" % os.path.dirname(os.path.realpath(__file__))

    img_text = ImageText(strings=['foobar title', 'foobar location'], font=font, color=(255, 255, 255))
    mask = ImageMask(image_text=img_text, font=font)

    assert re.match("\.\/\d{10}\.\d{3}\.png", mask.generate())
