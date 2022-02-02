#!/usr/bin/env python

from PIL import Image
import palette_mandmap
import palette_greens
import palette_blues

IMAGE_WIDTH = 400
IMAGE_HEIGHT = 300


def mandelbrot(cx, cy, maxiter):
    """Výpočet, kolik iterací je nutné pro opuštění jednotkového kruhu."""
    c = complex(cx, cy)
    z = 0
    for i in range(0, maxiter):
        if abs(z) > 2:
            return i
        z = z * z + c
    return 0


def recalc_fractal(image, palette, xmin, ymin, xmax, ymax, maxiter=1000):
    """Přepočet celého fraktálu."""
    width, height = image.size       # rozměry obrázku
    stepx = (xmax - xmin)/width
    stepy = (ymax - ymin)/height

    y1 = ymin
    for y in range(0, height):
        x1 = xmin
        for x in range(0, width):
            i = mandelbrot(x1, y1, maxiter)
            i = 3*i % 256
            color = (palette[i][0], palette[i][1], palette[i][2])
            image.putpixel((x, y), color)
            x1 += stepx
        y1 += stepy


def addImages(image1, image2):
    width, height = image1.size
    image = Image.new("RGB", (width, height))
    for y in range(0, height):
        for x in range(0, width):
            color1 = image1.getpixel((x,y))
            color2 = image2.getpixel((x,y))
            color = ((color1[0]+color2[0])//2, (color1[1]+color2[1])//2, (color1[2]+color2[2])//2)
            image.putpixel((x, y), color)
    return image


image1 = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
image2 = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

recalc_fractal(image1, palette_blues.palette,
               -0.769824999999999998320, -0.109270000000000000000,
               -0.766247499999999998426, -0.106570000000000000000, 1000)

recalc_fractal(image2, palette_greens.palette,
               -0.207190825000000012496, 0.676656624999999999983,
               -0.206107925000000012496, 0.677468799999999999983, 1000)

image3 = addImages(image1, image2)
image3.save("blend_add.png")
