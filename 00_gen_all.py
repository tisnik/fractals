#!/usr/bin/env python3

import os

import ast
from pathlib import Path


for path in Path(".").rglob("*"):
    if str(path) != "attractors/3D":
        continue
    if path.is_dir():
        directory = path
        cwd = os.getcwd()
        os.chdir(directory)

        try:
            with open("00_index.py", "w") as indexfile:
                print("# List of source files stored in this directory", file=indexfile)
                print("# ---------------------------------------------", file=indexfile)
                print("#", file=indexfile)
                files = sorted(os.listdir())

                for file in files:
                    if file.endswith(".py"):
                        if file == "00_index.py":
                            continue
                        print(f"# {file}:", file=indexfile)
                        with open(file, "r", encoding="utf-8") as fin:
                            source = fin.read()
                        try:
                            mod = ast.parse(source)
                            doc = ast.get_docstring(mod)
                        except SyntaxError:
                            doc = None
                        if doc:
                            print("# " + doc.splitlines()[0], file=indexfile)
                        print("#", file=indexfile)
        finally:
            os.chdir(cwd)
