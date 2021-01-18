from PIL import Image, ImageDraw, ImageFont
from random import randint, choice, choices, shuffle
from string import ascii_lowercase, ascii_uppercase, digits


class Captcha:
    @staticmethod
    def get_captcha() -> (Image, str):
        """
        Returns a captcha drawing 100 * 50.

        :return: Finished captcha image + answer.
        """

        # Colors
        background_colors = (
            (205, 0, 116), (153, 38, 103), (133, 0, 75), (230, 57, 155), (230, 103, 175),
            (255, 0, 0), (191, 48, 48), (166, 0, 0), (255, 64, 64), (255, 115, 115),
            (113, 9, 170), (95, 37, 128), (72, 3, 111), (159, 62, 213), (173, 102, 213)
        )
        text_colors = ((159, 238, 0), (134, 179, 45), (103, 155, 0), (185, 247, 62), (201, 247, 111))
        line_colors = ((0, 158, 142), (30, 119, 109), (0, 103, 92), (52, 207, 190), (93, 207, 195))

        image_width = 100
        image_height = 50

        line_width_min = 1
        line_width_max = int(image_height * 0.1)
        count_of_lines = 3

        count_of_points = int(image_width * image_height * 0.1)

        text_size = 14
        text_coordinates_start = get_random_coordinates(int(image_width * 0.1), int(image_height * 0.5))

        # Start draw captcha
        image = Image.new("RGB", (image_width, image_height), choice(background_colors))
        draw = ImageDraw.Draw(image)

        # Draw lines
        for i in range(count_of_lines):
            draw.line(
                (get_random_coordinates(image_width, image_height), get_random_coordinates(image_width, image_height)),
                fill=choice(line_colors),
                width=randint(line_width_min, line_width_max)
            )

        # Draw points
        for i in range(count_of_points):
            draw.point(get_random_coordinates(image_width, image_height), fill=get_random_color())

        # Draw text
        text = get_random_text()
        text_color = choice(text_colors)
        text_font_file = "src/fonts/ComicNeue-Bold.ttf"
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
