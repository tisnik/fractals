# vim: set fileencoding=utf-8

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

"""All entries from the complex fractals menu."""

from enum import Enum


class CplxMenu(Enum):
    """All entries from the complex fractals menu."""

    MANDELBROT = 1
    JULIA = 2
    MANDELBROT_Z3 = 3
    MANDELBROT_Z4 = 4
    MANDELBROT_Z2_Z = 4
    MANDELBROT_Z3_Z = 5

    QUIT = 7
