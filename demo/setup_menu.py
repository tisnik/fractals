# vim: set fileencoding=utf-8

#
#  (C) Copyright 2024  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

"""All entries from the setup menu."""

from enum import Enum


class SetupMenu(Enum):
    """All entries from the setup menu."""

    USE_PYTHON_RENDERERS = 0
    USE_C_RENDERERS = 1
    QUIT = 2
