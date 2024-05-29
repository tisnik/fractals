
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

"""All entries from the main menu."""

from enum import Enum


class MainMenu(Enum):
    """All entries from the main menu."""

    PROCEDURAL_TEXTURES = 0
    COMPLEX_FRACTALS = 1
    STRANGE_ATTRACTORS = 2
    IFS = 3
    DYNAMIC_SYSTEMS = 4
    SETUP = 5
    ABOUT = 6
    QUIT = 7
