import operator
import os
import random
import numpy
from wordcloud import WordCloud, STOPWORDS
from PIL import Image, ImageDraw
from .mask import ImageMask
from .text import ImageText


class ImageGenerator:
    """
    ImageGenerator
    :param kwargs: theme, height, width, padding, cloud_font, text_font,
                   prefer_horizontal, job_title_text, job_location_text

    width: integer
    height: integer
    job_title_text: string
    job_location_text: string
    theme: string (default, autumn, dusk, or neon as accepted values)
    cloud_font: see fonts folder for availability
    text_font: string font path
    prefer_horizontal: integer >= 1 sets prefer_horizontal to true

    If we have either job_title_text or job_location_text, we need to create a mask that will contain
    placeholder spots for these strings.  Necessary so that the word cloud generator knows not to write
    in or near their positions while keeping it as natural looking as possible.
    """
    def __init__(self, **kwargs):
        self._fonts = ['arial', 'arial-bold', 'arial-black', 'arial-narrow', 'courier-new', 'verdana']
        self._themes = self.__load_themes()
        self._theme = kwargs.get('theme', 'default')

        if self._theme not in self._themes.keys():
            raise TypeError("'%s' is not a valid theme value" % self._theme)

        self._height = kwargs.get('height', 250)
        self._width = kwargs.get('width', 250)
        self._padding = kwargs.get('padding', 0)

        self._cloud_font = kwargs.get('cloud_font', 'arial-black')
        if self._cloud_font not in self._fonts:
            raise TypeError("'%s' is not valid cloud_font value" % self._cloud_font)

        self._cloud_font = self.__build_font_path(self._cloud_font)

        self._text_font = kwargs.get('text_font', 'arial-bold')
        if self._text_font not in self._fonts:
            raise TypeError("'%s' is not valid text_font value" % self._text_font)

        self._text_font = self.__build_font_path(self._text_font)

        self._prefer_horizontal = kwargs.get('prefer_horizontal', 0.90)
        self._tmp_storage = kwargs.get('tmp_storage', './')

        job_title_text = kwargs.get('job_title_text', None)
        job_location_text = kwargs.get('job_location_text', None)
        self._image_text = self.__create_text(job_title_text, job_location_text)

        self._mask = self.__generate_base_mask()

        self._cloud = WordCloud(height=self._height,
                                width=self._width,
                                background_color=self._themes[self._theme]['background_color'],
                                font_path=self._cloud_font,
                                prefer_horizontal=self._prefer_horizontal,
                                mask=self._mask,
                                color_func=self._themes[self._theme]['cloud_generator'],
                                stopwords=set(STOPWORDS))

    def generate(self, filename, **kwargs):
        """
        Generate word cloud image
        :param filename: File to save cloud image to
        :param kwargs: phrases, description

        Required: phrases or description

        :return: void
        """
        weighted_phrases = kwargs.get('phrases', list())

        description = kwargs.get('description', '')

        if not weighted_phrases and not description:
            raise TypeError("Please provide phrases or a description")

        p_d_normalized = self.__normalize_phrases_desc(weighted_phrases, description)

        self._cloud.generate_from_frequencies(p_d_normalized)
        self._cloud.to_file(filename)

        if self._image_text:
            cloud_image = Image.open(filename)
            drawer = ImageDraw.Draw(cloud_image)

            self._image_text.draw_text(drawer)

            cloud_image.save(filename)

    def __build_font_path(self, font):
        pwd = os.path.dirname(os.path.realpath(__file__))
        return "%s/fonts/%s.ttf" % (pwd, font)

    def __normalize_phrases_desc(self, phrases, description=''):
        # We want to prioritize/emphasize phrases in the cloud image

        if not description:
            return phrases

        # Get word frequencies of description

        # Find the word with the most weight
        desc_freq = self._cloud.process_text(description)
        largest_d_key = max(desc_freq.items(), key=operator.itemgetter(1))[0]
        largest_d_value = desc_freq[largest_d_key]

        # Get the phrase with the least weight
        smallest_p_key = min(phrases.items(), key=operator.itemgetter(1))[0]
        smallest_p_value = phrases[smallest_p_key]

        # Alter each phrases weight to be more than the word with the largest weight from the description

        if smallest_p_value < largest_d_value:
            for phrase in phrases.keys():
                phrases[phrase] += largest_d_value

        desc_freq.update({p: phrases[p] * 2 for p in phrases.keys()})

        return desc_freq

    def __create_text(self, title=None, location=None):
        if not title and not location:
            return None

        return ImageText(
            strings=list([title, location]),
            font=self._text_font,
            color=self._themes[self._theme]['text_color'],
            image_width=self._width,
            image_height=self._height,
            image_padding=self._padding)

    def __generate_base_mask(self):
        mask = ImageMask(width=self._width,
                         height=self._height,
                         image_text=self._image_text,
                         font=self._text_font,
                         tmp_storage=self._tmp_storage)

        mask_file = mask.generate()

        if mask_file:
            return numpy.array(Image.open(mask_file))

        return None

    def __load_themes(self):
        default_text_color = (107, 178, 255)
        dusk_text_color = (255, 103, 104)
        neon_text_color = (252, 37, 113)
        autumn_text_color = (255, 255, 255)

        def dusk(*a, **kw):
            colors = list([
                (0, 125, 141),
                (0, 172, 144),
                (103, 88, 126),
                (149, 116, 158),
                (185, 193, 226),
                (130, 215, 126),
                (249, 248, 113)
            ])

            if not self._image_text:
                colors += [dusk_text_color] * 3

            random_index = random.randint(0, len(colors)-1)
            return colors[random_index]

        def neon(*a, **kw):
            colors = list([
                (255, 149, 28),
                (105, 217, 238),
                (166, 226, 39),
                (164, 128, 252),
            ])

            if not self._image_text:
                colors += [neon_text_color]

            random_index = random.randint(0, len(colors) - 1)
            return colors[random_index]

        def default(*a, **kw):
            colors = list([
                (255, 0, 60),
                (255, 0, 60),
                (255, 0, 60),
                (136, 193, 0),
                (136, 193, 0),
                (136, 193, 0),
                (253, 138, 0),
                (253, 138, 0),
                (253, 138, 0),
                (250, 190, 40),
                (250, 190, 40),
                (1, 193, 188),
                (1, 193, 188),
                (172, 99, 200),
                (172, 99, 200)
            ])

            if not self._image_text:
                colors += [default_text_color] * 3

            random_index = random.randint(0, len(colors) - 1)
            return colors[random_index]

        def autumn(*a, **kw):
            colors = list([
                (210, 193, 152),
                (210, 193, 152),
                (210, 193, 152),
                (217, 92, 53),
                (217, 92, 53),
                (217, 92, 53),
                (134, 90, 55),
                (134, 90, 55),
                (134, 90, 55),
                (101, 101, 75),
                (101, 101, 75),
                (134, 137, 138),
                (134, 137, 138),
                (85, 73, 75),
            ])

            random_index = random.randint(0, len(colors) - 1)
            return colors[random_index]

        return dict({
            'autumn': {
                'text_color': autumn_text_color,
                'cloud_generator': autumn,
                'background_color': (62, 28, 0)
            },
            'default': {
                'text_color': default_text_color,
                'cloud_generator': default,
                'background_color': (255, 255, 255)
            },
            'dusk': {
                'text_color': dusk_text_color,
                'cloud_generator': dusk,
                'background_color': (23, 34, 59)
            },
            'neon': {
                'text_color': neon_text_color,
                'cloud_generator': neon,
                'background_color': (0, 0, 0)
            }
        })
