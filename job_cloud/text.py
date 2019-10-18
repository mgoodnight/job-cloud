from PIL import Image, ImageDraw, ImageFont


class ImageText:
    """
    ImageText

    :param kwargs: strings, font, color, image_width, image_height, image_padding

    strings: list of strings
    font: string path to font
    color: RGB tuple
    image_width: integer
    image_height: integer
    image_padding: integer

    Required: font
    """
    def __init__(self, **kwargs):
        strings = kwargs.get('strings', list())
        self._font = kwargs.get('font', None)

        if not self._font:
            raise TypeError("Missing required field 'font'")

        self._color = kwargs.get('color', (0, 0, 0))
        self._image_width = kwargs.get('image_width', 250)
        self._image_height = kwargs.get('image_height', 250)
        self._image_padding = kwargs.get('image_padding', 0)

        self._text = "\n".join(filter(None, strings)).rstrip()
        self._font_size = self.__calculate_font_size()
        self._image_font = ImageFont.truetype(self._font, self._font_size)

        self._aggregate_height = sum([self.__calculate_string_size(self._image_font, s)[1] for s in strings])
        self._strings_detail = list()

        previous_str_size = (0, 0)
        for s in strings:
            size = self.__calculate_string_size(self._image_font, s)

            start_x = (self._image_padding + (self._image_width - size[0]) / 2) - self._image_padding
            start_y = ((self._image_height - self._aggregate_height) / 2) + previous_str_size[1]

            self._strings_detail.append((s, size, (start_x, start_y)))

            previous_str_size = size

    def draw_text(self, drawer):
        """
        Draw text to image.
        :param drawer: ImageDraw object
        :return: void
        """
        for s_details in self._strings_detail:
            drawer.text((s_details[2][0], s_details[2][1]), s_details[0],
                        font=self._image_font, fill=self._color, align='center')

    def draw_mask_placeholder(self, drawer):
        """
        Draw the placeholder for text
        :param drawer: ImageDraw object
        :return: void
        """
        for s_details in self._strings_detail:

            end_x = s_details[2][0] + s_details[1][0] + 5  # 5 px for bottom padding
            end_y = s_details[2][1] + s_details[1][1] + 5  # 5 px for bottom padding

            drawer.rectangle((s_details[2], (end_x, end_y)), fill=(255, 255, 255))

    def get_font(self):
        """
        Return Font object
        :return: PIL Font object
        """
        return self.__get_font(self._font_size)

    def __calculate_font_size(self):
        start_font_size = 10
        max_width = self._image_width - (self._image_padding * 2)

        # Check font size on each iteration until the width is too long for image.
        # Once its too large, return the previous value.
        while True:
            font_size = start_font_size + 1
            font = ImageFont.truetype(self._font, font_size)
            string_size = self.__calculate_string_size(font, self._text)

            if string_size[0] > max_width:
                return start_font_size

            start_font_size += 1

    def __calculate_string_size(self, font, string):
        img = Image.new('RGB', (self._image_width, self._image_height))
        draw = ImageDraw.Draw(img)

        return draw.textsize(string, font)

    def __get_font(self, font_size):
        return ImageFont.truetype(self._font, font_size)
