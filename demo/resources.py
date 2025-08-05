#
#  (C) Copyright 2023, 2024  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

"""Resources used within the demo."""

import configparser
import os
from os.path import isfile, join
from typing import Dict, List, Tuple

import pygame
from pygame.font import Font

from textures import (
    palette_blues,
    palette_gold,
    palette_greens,
    palette_ice,
    palette_juteblue,
    palette_jutemap,
    palette_jutes,
    palette_mandmap,
    palette_phong,
    palette_rose,
)


class Resources:
    """Resources used within the demo."""

    FONT_FILE_NAME = "FreeSans.ttf"

    def __init__(self, configuration: configparser.ConfigParser) -> None:
        """Resource initialization."""
        self.loadFonts(configuration)
        self.loadImages(configuration)
        self.loadPalettes()

    def loadFonts(self, configuration: configparser.ConfigParser) -> None:
        """Load all required fonts."""
        fontDirectory = configuration["paths"]["fonts"]
        fullFontFileName = os.path.join(fontDirectory, Resources.FONT_FILE_NAME)

        # check if file with font exists
        if not os.path.isfile(fullFontFileName):
            raise FileNotFoundError(f"Font file not found: {fullFontFileName}")

        self._big_font = pygame.font.Font(fullFontFileName, 60)
        self._normal_font = pygame.font.Font(fullFontFileName, 40)
        self._small_font = pygame.font.Font(fullFontFileName, 20)

    def loadImages(self, configuration: configparser.ConfigParser) -> None:
        """Load all images from specified directory."""
        imageList = get_list_of_images(configuration)
        self._images = {}
        for imageName in imageList:
            try:
                self._images[imageName[0]] = pygame.image.load(imageName[1])
            except pygame.error as e:
                print(f"Warning: Could not load image {imageName[1]}: {e}")

    def loadPalettes(self) -> None:
        self._palettes = []
        self._palettes.append(palette_blues.palette)
        self._palettes.append(palette_gold.palette)
        self._palettes.append(palette_greens.palette)
        self._palettes.append(palette_ice.palette)
        self._palettes.append(palette_mandmap.palette)
        self._palettes.append(palette_juteblue.palette)
        self._palettes.append(palette_jutemap.palette)
        self._palettes.append(palette_jutes.palette)
        self._palettes.append(palette_phong.palette)
        self._palettes.append(palette_rose.palette)

    @property
    def palettes(self) -> list[list[tuple[int, int, int]]]:
        """Color palettes."""
        return self._palettes

    @property
    def bigFont(self) -> Font:
        """Big font to be used on all screens."""
        return self._big_font

    @property
    def normalFont(self) -> Font:
        """Middle font to be used on all screens."""
        return self._normal_font

    @property
    def smallFont(self) -> Font:
        """Small font to be used on all screens."""
        return self._small_font

    @property
    def images(self) -> Dict[str, pygame.Surface]:
        """All images available as list."""
        return self._images


def get_list_of_images(
    configuration: configparser.ConfigParser,
) -> List[Tuple[str, str]]:
    """Retrieve list of all image files from specified directory."""
    path = configuration["paths"]["images"]
    return [
        (short_filename(fileName), join(path, fileName))
        for fileName in os.listdir(path)
        if isfile(join(path, fileName))
    ]


def short_filename(filename: str) -> str:
    """Take just filename without extension."""
    return filename[0 : filename.index(".")]
