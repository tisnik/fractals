import os

directories = "complex",

for directory in directories:
    cwd = os.getcwd()
    os.chdir(directory)

    with open("00_index.py", "w") as indexfile:
        print("# List of source files stored in this directory", file=indexfile)
        print("# ---------------------------------------------", file=indexfile)
        print("#", file=indexfile)
        files = sorted(os.listdir())

        for file in files:
            if file.endswith(".py") and file != "00_index.py":
                print("# " + file + ":", file=indexfile)
                with open(file, "r") as fin:
                    for line in fin:
                        line = line.strip()
                        if line.startswith('"""') and line.endswith('"""'):
                            line=line[3:][:-3]
                            print("# " + line, file=indexfile)
                            break
                print("#", file=indexfile)
    os.chdir(cwd)
