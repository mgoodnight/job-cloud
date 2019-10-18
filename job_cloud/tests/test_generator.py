import pytest
import os
from PIL import Image
from job_cloud.generator import ImageGenerator


@pytest.fixture()
def phrases_and_desc():
    weighted_phrases = dict([
        ('Perl', 3), ('Python', 3), ('PHP', 2), ('MySQL', 2), ('Linux', 2), ('Angular', 2), ('Node.js', 2),
        ('React', 2), ('PostgreSQL', 1), ('DevOps', 1), ('HTML', 1), ('CSS', 1), ('Jenkins', 1), ('CircleCI', 1),
        ('Java', 1), ('C', 1), ('C++', 1), ('MongoDB', 1), ('Apache', 1), ('nginx', 1), ('Redis', 1), ('GoLang', 1)
    ])
    desc_fixture = "%s/fixtures/description" % os.path.dirname(os.path.realpath(__file__))
    description = open(desc_fixture, 'r').read()

    return weighted_phrases, description


def test_generator(phrases_and_desc):
    file = '%s/foobar-dimensions.png' % os.path.dirname(os.path.realpath(__file__))
    cloud = ImageGenerator(width=500, height=250)
    cloud.generate(file, phrases=phrases_and_desc[0])

    img = Image.open(file)

    assert img.size == (500, 250)

    cleanup(file)


def test_generator_errors(phrases_and_desc):
    with pytest.raises(TypeError):
        ImageGenerator(theme='fake-theme')
    with pytest.raises(TypeError):
        ImageGenerator(cloud_font='fake-font')
    with pytest.raises(TypeError):
        ImageGenerator(text_font='fake-font')
    with pytest.raises(TypeError):
        img = ImageGenerator()
        img.generate()


def compare_images(f1, f2):
    f1_content = open(f1, 'rb').read()
    f2_content = open(f2, 'rb').read()

    return f1_content == f2_content


def cleanup(file):
    os.remove(file)
