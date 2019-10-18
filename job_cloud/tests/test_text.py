import pytest
from PIL import Image, ImageDraw
import os
from job_cloud.text import ImageText


@pytest.fixture
def base_file():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    filename = 'foobar-text.png'

    # Create base image to draw on
    write_file = "%s/%s" % (cur_dir, filename)
    img = Image.new('RGB', (250, 250), color=(0, 0, 0))
    img.save(write_file)

    return cur_dir, filename


def test_type_error_no_font():
    with pytest.raises(TypeError):
        ImageText()


def test_get_font(base_file):
    font = "%s/../fonts/arial-black.ttf" % base_file[0]
    img_text = ImageText(strings=['foobar title', 'foobar location'], font=font)

    assert str(type(img_text.get_font())) == "<class 'PIL.ImageFont.FreeTypeFont'>"


def test_draw_text(base_file):
    font = "%s/../fonts/arial-black.ttf" % base_file[0]
    img_text = ImageText(strings=['foobar title', 'foobar location'], font=font, color='white')
    write_file = "%s/%s" % (base_file[0], base_file[1])

    cloud_image = Image.open(write_file)
    drawer = ImageDraw.Draw(cloud_image)
    img_text.draw_text(drawer)

    cloud_image.save(write_file)

    # Compare byte data with previously generated test image
    wc = open(write_file, mode='rb').read()

    test_file = "%s/images/%s" % (base_file[0], base_file[1])
    tc = open(test_file, mode='rb').read()

    assert wc == tc

    # Clean up
    os.remove(write_file)


def test_draw_mask_placeholder(base_file):
    font = "%s/../fonts/arial-black.ttf" % base_file[0]
    img_text = ImageText(strings=['foobar title', 'foobar location'], font=font, color=(255, 255, 255))
    write_file = "%s/%s" % (base_file[0], base_file[1])

    cloud_image = Image.open(write_file)
    drawer = ImageDraw.Draw(cloud_image)
    img_text.draw_text(drawer)

    img_text.draw_mask_placeholder(drawer)

    cloud_image.save(write_file)

    # Compare byte data with previously generated test image
    wc = open(write_file, mode='rb').read()

    test_file = "%s/images/%s" % (base_file[0], 'foobar-text-placeholder.png')
    tc = open(test_file, mode='rb').read()

    assert wc == tc

    # Clean up
    os.remove(write_file)
