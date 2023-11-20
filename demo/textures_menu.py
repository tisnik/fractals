# vim: set fileencoding=utf-8

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

"""All entries from the procedural textures menu."""

from enum import Enum


class TexturesMenu(Enum):
    """All entries from the procedural textures menu."""

    CIRCLE_MOIRE = 0
    OTHER_MOIRE = 1
    QUIT = 2
