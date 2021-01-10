from PIL import Image, ImageDraw, ImageFont
from random import randint, choice, choices, shuffle
from string import ascii_lowercase, ascii_uppercase, digits


class Captcha:
    @staticmethod
    def get_captcha() -> (Image, str):
        """
        Returns a captcha drawing 400 * 200.

        :return: Finished captcha image + answer.
        """

        image_width = 100
        image_height = 50

        line_width_min = 1
        line_width_max = int(image_height * 0.1)
        count_of_lines = 3

        count_of_points = int(image_width * image_height * 0.1)

        text_size = 14
        text_coordinates_start = get_random_coordinates(int(image_width * 0.1), int(image_height * 0.1))

        image = Image.new("RGB", (image_width, image_height), get_random_color())
        draw = ImageDraw.Draw(image)

        for i in range(count_of_lines):
            draw.line(
                (get_random_coordinates(image_width, image_height), get_random_coordinates(image_width, image_height)),
                fill=get_random_color(),
                width=randint(line_width_min, line_width_max)
            )

        for i in range(count_of_points):
            draw.point(get_random_coordinates(image_width, image_height), fill=get_random_color())

        text = get_random_text()
        text_color = get_random_color()
        text_font_file = "src/fonts/ComingSoon-Regular.ttf"
        text_font = ImageFont.truetype(text_font_file, text_size)
        draw.text(text_coordinates_start, text, fill=text_color, font=text_font)

        return image, text


def get_random_color() -> tuple:
    """
    Returns a random RGB color.

    :return: Random color.
    """

    return randint(0, 255), randint(0, 255), randint(0, 255)


def get_random_coordinates(width: int, height: int) -> tuple:
    """
    Returns random x and y.

    :param width: Canvas width.
    :param height: Canvas height.
    :return: Random coordinates on canvas.
    """

    return randint(0, width), randint(0, height)


def get_random_text() -> str:
    """
    Returns a random text of length 5-10. At least one digit.

    :return: Random string.
    """

    length = randint(5, 10)
    all_symbols = ascii_lowercase + ascii_uppercase + digits

    temp_list_of_symbols = choices(all_symbols, k=length-1)
    temp_list_of_symbols.append(choice(digits))
    shuffle(temp_list_of_symbols)

    return ''.join(temp_list_of_symbols)
