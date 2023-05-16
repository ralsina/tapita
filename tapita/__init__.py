import textwrap
import urllib
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

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


class Cover:
    def __init__(self, title, subtitle, author):
        self.title = title
        self.subtitle = subtitle
        self.author = author

        self.cover_width = 1200
        self.cover_height = 1800

        self.cover_margin = 2
        self.cover_image = Image.new("RGB", (self.cover_width, self.cover_height))
        self.image_draw = ImageDraw.Draw(self.cover_image)

        self._processColors()
        self._drawBackground()
        self._drawArtwork()
        self._drawText()

    def _drawBackground(self):
        # Fill the background of the image with white.
        self.image_draw.rectangle(
            (0, 0, self.cover_width, self.cover_height), fill=self.background
        )

    def _getFont(self, size):
        return ImageFont.truetype(str(Path(__file__).parent / "HackNerdFont-Regular.ttf"), int(size))
    
    def _drawArtwork(self):
        artwork_start_x = 0
        artwork_start_y = self.cover_height - self.cover_width

        with urllib.request.urlopen(
            f"https://api.dicebear.com/6.x/identicon/png?seed={urllib.parse.quote(self.title)}&size={self.cover_width}"
        ) as request:
            art = Image.open(BytesIO(request.read())).resize(
                (self.cover_width, self.cover_width)
            )

        self.cover_image.paste(art, (artwork_start_x, artwork_start_y))

    # Allocate fonts for the title and the author, and draw the text.
    def _drawText(self):
        title_font = self._getFont(self.cover_width * 0.08)
        subtitle_font = self._getFont(self.cover_width * 0.05)
        author_font = self._getFont(self.cover_width * 0.06)

        # Just a fancy way to say "near the top"
        title_height = (
            self.cover_height
            - self.cover_width
            - (self.cover_height * self.cover_margin / 100)
        ) * 0.6

        x = self.cover_height * self.cover_margin / 100
        y = self.cover_height * self.cover_margin / 100 * 2

        wrapped = textwrap.wrap(self.title, 18)
        self.image_draw.text(
            (x, y), "\n".join(wrapped), font=title_font, fill=self.foreground
        )

        bbox = self.image_draw.textbbox((x, y), "\n".join(wrapped), font=title_font)
        title_height = bbox[3] - bbox[1]
        y = y + title_height + 0.03 * self.cover_height

        if self.subtitle:
            self.image_draw.text(
                (x, y),
                "\n".join(textwrap.wrap(self.subtitle)),
                font=subtitle_font,
                fill=self.foreground,
            )

            bbox = self.image_draw.textbbox((x, y), "\n".join(wrapped), font=title_font)
            subtitle_height = bbox[3] - bbox[1]
            y = y + subtitle_height + 0.03 * self.cover_height

        bbox = self.image_draw.textbbox((x, y), self.author, font=author_font)
        author_height = bbox[3] - bbox[1]
        self.image_draw.text(
            (x, self.cover_height * 0.97 - self.cover_width - author_height),
            self.author,
            font=author_font,
            fill=self.foreground,
        )

    def _processColors(self):
        base_saturation = 100
        base_brightness = 90
        color_distance = 100

        counts = len(self.title) + len(self.author)
        color_seed = int(_map(_clip(counts, 2, 80), 2, 80, 10, 360))
        self.shape_color = ImageColor.getrgb(
            f"hsv({color_seed}, {base_saturation}%, {base_brightness - (counts % 20)}%)"
        )
        self.base_color = ImageColor.getrgb(
            f"hsv({(color_seed + color_distance) % 360}, {base_saturation}%, {base_brightness}%)"
        )

        self.background = ImageColor.getrgb("#fff")
        self.foreground = ImageColor.getrgb("rgb(50, 50, 50)")
