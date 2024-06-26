#!/usr/bin/env python

#
#  (C) Copyright 2023  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#


"""IFS systémy."""

from random import random

from PIL import Image

# rozměry obrázku s fraktálem
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512

# transformace a jejich pravděpodobnosti
IFS_SYSTEMS = {
    "binary": (
        (0.500000, 0.000000, 0.000000, 0.500000, -2.563477, -0.000003, 0.333333),
        (0.500000, 0.000000, 0.000000, 0.500000, 2.436544, -0.000003, 0.333333),
        (0.000000, -0.500000, 0.500000, 0.000000, 4.873085, 7.563492, 0.333333),
    ),
    "coral": (
        (0.307692, -0.531469, -0.461538, -0.293706, 5.401953, 8.655175, 0.400000),
        (0.307692, -0.076923, 0.153846, -0.447552, -1.295248, 4.152990, 0.150000),
        (0.000000, 0.545455, 0.692308, -0.195804, -4.893637, 7.269794, 0.450000),
    ),
    "crystal": (
        (0.696970, -0.481061, -0.393939, -0.662879, 2.147003, 10.310288, 0.747826),
        (0.090909, -0.443182, 0.515152, -0.094697, 4.286558, 2.925762, 0.252174),
    ),
    "dragon": (
        (0.824074, 0.281482, -0.212346, 0.864198, -1.882290, -0.110607, 0.787473),
        (0.088272, 0.520988, -0.463889, -0.377778, 0.785360, 8.095795, 0.212527),
    ),
    "dragon2": (
        (0.824074, 0.281481, -0.212346, 0.864197, -1.772710, 0.137795, 0.771268),
        (-0.138580, 0.283951, -0.670062, -0.279012, 2.930991, 7.338924, 0.228732),
    ),
    "feather": (
        (0.870370, 0.074074, -0.115741, 0.851852, -1.278016, 0.070331, 0.798030),
        (-0.162037, -0.407407, 0.495370, 0.074074, 6.835726, 5.799174, 0.201970),
    ),
    "fern": (
        (0.850000, 0.040000, -0.040000, 0.850000, 0.000000, 1.600000, 0.850000),
        (0.200000, -0.260000, 0.230000, 0.220000, 0.000000, 1.600000, 0.070000),
        (-0.150000, 0.280000, 0.260000, 0.240000, 0.000000, 0.440000, 0.070000),
        (0.000000, 0.000000, 0.000000, 0.160000, 0.000000, 0.000000, 0.010000),
    ),
    "koch": (
        (0.307692, 0.000000, 0.000000, 0.294118, 4.119164, 1.604278, 0.151515),
        (0.192308, -0.205882, 0.653846, 0.088235, -0.688840, 5.978916, 0.253788),
        (0.192308, 0.205882, -0.653846, 0.088235, 0.668580, 5.962514, 0.253788),
        (0.307692, 0.000000, 0.000000, 0.294118, -4.136530, 1.604278, 0.151515),
        (0.384615, 0.000000, 0.000000, -0.294118, -0.007718, 2.941176, 1.000000),
    ),
    "spiral": (
        (0.787879, -0.424242, 0.242424, 0.859848, 1.758647, 1.408065, 0.895652),
        (-0.121212, 0.257576, 0.151515, 0.053030, -6.721654, 1.377236, 0.052174),
        (0.181818, -0.136364, 0.090909, 0.181818, 6.086107, 1.568035, 0.052174),
    ),
    "tree": (
        (0.000000, 0.000000, 0.000000, 0.500000, 0.000000, 0.000000, 0.050000),
        (0.420000, -0.420000, 0.420000, 0.420000, 0.000000, 0.200000, 0.400000),
        (0.420000, 0.420000, -0.420000, 0.420000, 0.000000, 0.200000, 0.400000),
        (0.100000, 0.000000, 0.000000, 0.100000, 0.000000, 0.200000, 0.150000),
    ),
    "triangle": (
        (0.500000, 0.000000, 0.000000, 0.500000, -0.500000, 0.000000, 0.333333),
        (0.500000, 0.000000, 0.000000, 0.500000, 0.500000, 0.000000, 0.333333),
        (0.500000, 0.000000, 0.000000, 0.500000, 0.000000, 0.860000, 0.333334),
    ),
}


def generate_ifs(
    image: Image.Image, width: int, height: int, maxiter: int, startiter: int, ifs
):
    delitel = 12.0

    # obdélník opsaný IFS
    xmin = -7.0
    ymin = -1.0

    # libovolné počáteční souřadnice v rovině
    x1 = y1 = 0

    for i in range(maxiter):
        # pp leží v rozsahu 0.0 - 1.0
        pp = random()

        # na základě náhodného čísla najít transformaci
        suma = 0
        j = 0
        while suma <= pp:
            suma += ifs[j][6]
            j += 1
        j -= 1

        # aplikovat vybranou transformaci
        x2 = x1 * ifs[j][0] + y1 * ifs[j][1] + ifs[j][4]
        y2 = x1 * ifs[j][2] + y1 * ifs[j][3] + ifs[j][5]
        x1 = x2
        y1 = y2

        # pokud byl překročen počet startovních iterací
        if i > startiter:
            # vypočítat a zobrazit bod
            x2 = (x1 - xmin) * width / delitel
            y2 = (y1 - ymin) * height / delitel

            x = int(x2)
            y = int(y2)
            if x >= 0 and y >= 0 and x < IMAGE_WIDTH and y < IMAGE_HEIGHT:
                image.putpixel((x, y), 0xFFFFFF)


def main() -> None:
    # vykreslit všechny IFS
    for name, transformations in IFS_SYSTEMS.items():
        print(name)

        # inicializace prázdného obrázku
        image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

        # vykreslení IFS
        generate_ifs(image, IMAGE_WIDTH, IMAGE_HEIGHT, 100000, 1000, transformations)

        # uložení obrázku do souboru
        image.save(name + ".png")


if __name__ == "__main__":
    main()
