from pathlib import Path
from PIL import Image

size = (500, 374)


def main():
    files = list(Path(".").rglob("*.png"))

    for filename in files:
        print(filename)
        input_image = Image.open(filename)

        output_image = input_image.resize(size, resample=Image.BICUBIC)
        output_image.save("_" + str(filename))


if __name__ == "__main__":
    main()
