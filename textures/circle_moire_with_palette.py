#!/usr/bin/env python

"""Vytvoreni textury s "kruznicovym moare"."""

from typing import Tuple

from PIL import Image

# textura by mela byt ctvercova a jeji sirka i vyska by mela byt
# mocninou cisla 2
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


def recalc_circle_pattern(
    image: Image.Image,
    palette: Tuple[Tuple[int, int, int], ...],
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
) -> None:
    """Funkce provadejici vypocet moare s kruznicovym vzorkem."""
    width, height = image.size  # rozmery obrazku
    stepx = (xmax - xmin) / width
    stepy = (ymax - ymin) / height

    y1 = ymin
    for y in range(height):
        x1 = xmin
        for x in range(width):
            x1 += stepx
            x2 = x1 * x1
            y2 = y1 * y1
            i = (int)(x2 + y2) & 255
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
        y1 += stepy


def main() -> None:
    """Vypocet textur s jejich ulozenim do souboru."""
    import palette_blues
    import palette_gold
    import palette_greens
    import palette_ice
    import palette_mandmap

    mez = (2 << 5) + 50 * 2.5
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    image_pals = (
        (palette_blues.palette, "blues"),
        (palette_greens.palette, "greens"),
        (palette_gold.palette, "gold"),
        (palette_ice.palette, "ice"),
        (palette_mandmap.palette, "mandmap"),
    )

    for image_pal in image_pals:
        print(image_pal[1])
        recalc_circle_pattern(image, image_pal[0], -mez, -mez, mez, mez)
        image.save(f"patternB_{image_pal[1]}.png")


if __name__ == "__main__":
    main()
