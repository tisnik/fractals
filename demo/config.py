
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

"""Functions to load and store configuration to INI file."""

import configparser


def loadConfiguration(filename: str) -> configparser.ConfigParser:
    """Load configuration from provided INI file."""
    config = configparser.ConfigParser()
    config.read(filename)
    return config


def saveConfiguration(filename: str) -> None:
    """Store configuration into provided INI file."""
    # TODO: add implementation there
