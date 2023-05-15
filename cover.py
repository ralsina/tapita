import textwrap
import urllib
import urllib.parse
import urllib.request
from io import BytesIO

import click
from PIL import Image, ImageColor, ImageDraw, ImageFont


def _map(value, istart, istop, ostart, ostop):
    """
    Helper function that implements the Processing function map(). For more
    details see https://processing.org/reference/map_.html
    http://stackoverflow.com/questions/17134839/how-does-the-map-function-in-processing-work
    """
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


def _clip(value, lower, upper):
    """
    Helper function to clip a given value based on a lower/upper bound.
    """
    return lower if value < lower else upper if value > upper else value


cover_width = 1200
cover_height = 1800


@click.command()
@click.option("-t", "--title", metavar="<title>", help="Book title")
@click.option(
    "-s", "--subtitle", metavar="<subtitle>", help="Book subtitle", default=None
)
@click.option("-a", "--author", metavar="<author>", help="Book author", default=None)
@click.option("-o", "--output", metavar="<filename>", help="Output file (- for stdout)")
def cover(title, author, output, subtitle):
    def processColors():
        base_saturation = 100
        base_brightness = 90
        color_distance = 100
        invert = True

        counts = len(title) + len(author)
        color_seed = int(_map(_clip(counts, 2, 80), 2, 80, 10, 360))
        shape_color = ImageColor.getrgb(
            f"hsv({color_seed}, {base_saturation}%, {base_brightness - (counts % 20)}%)"
        )
        base_color = ImageColor.getrgb(
            f"hsv({(color_seed + color_distance) % 360}, {base_saturation}%, {base_brightness}%)"
        )
        if invert:
            shape_color, base_color = base_color, shape_color
        if (counts % 10) == 0:
            shape_color, base_color = base_color, shape_color
        return shape_color, base_color

    # Fill the background of the image with white.
    def drawBackground():
        fill = ImageColor.getrgb("#fff")
        image_draw.rectangle((0, 0, cover_width, cover_height), fill=fill)

    # Allocate fonts for the title and the author, and draw the text.
    def drawText():
        fill = ImageColor.getrgb("rgb(50, 50, 50)")

        title_font_size = int(cover_width * 0.08)
        subtitle_font_size = int(cover_width * 0.05)
        author_font_size = int(cover_width * 0.06)
        title_font = ImageFont.truetype(
            "/usr/share/fonts/TTF/Hack-Regular.ttf", title_font_size
        )
        subtitle_font = ImageFont.truetype(
            "/usr/share/fonts/TTF/Hack-Regular.ttf", subtitle_font_size
        )
        author_font = ImageFont.truetype(
            "/usr/share/fonts/TTF/Hack-Regular.ttf", author_font_size
        )

        title_height = (
            cover_height - cover_width - (cover_height * cover_margin / 100)
        ) * 0.6

        x = cover_height * cover_margin / 100
        y = cover_height * cover_margin / 100 * 2
        wrapped = textwrap.wrap(title, 18)
        image_draw.text((x, y), "\n".join(wrapped), font=title_font, fill=fill)

        bbox = image_draw.textbbox((x, y), "\n".join(wrapped), font=title_font)
        title_height = bbox[3] - bbox[1]
        y = y + title_height + 0.03 * cover_height

        if subtitle:
            image_draw.text(
                (x, y),
                "\n".join(textwrap.wrap(subtitle)),
                font=subtitle_font,
                fill=fill,
            )

            bbox = image_draw.textbbox((x, y), "\n".join(wrapped), font=title_font)
            subtitle_height = bbox[3] - bbox[1]
            y = y + subtitle_height + 0.03 * cover_height

        x = cover_height * cover_margin / 100
        image_draw.text((x, y), author, font=author_font, fill=fill)

    def drawArtwork():
        artwork_start_x = 0
        artwork_start_y = cover_height - cover_width

        with urllib.request.urlopen(
            f"https://api.dicebear.com/6.x/identicon/png?seed={urllib.parse.quote(title)}&size={cover_width}"
        ) as request:
            art = Image.open(BytesIO(request.read())).resize((cover_width, cover_width))

        cover_image.paste(art, (artwork_start_x, artwork_start_y))

    # Create the new cover image.
    cover_margin = 2
    cover_image = Image.new("RGB", (cover_width, cover_height))
    image_draw = ImageDraw.Draw(cover_image)

    # Draw the book cover.
    shape_color, base_color = processColors()
    drawBackground()
    drawArtwork()
    drawText()

    # Return the cover Image instance.
    cover_image.save(output)


if __name__ == "__main__":
    cover()
