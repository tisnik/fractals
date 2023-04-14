package main

import (
	"fmt"
	"image"
	"image/png"
	"log"
	"os"
)

func readImage(filePath string) (image.Image, error) {
	f, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	image, err := png.Decode(f)
	return image, err
}

func writeImage(img image.Image, filePath string) error {
	outfile, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer outfile.Close()

	return png.Encode(outfile, img)
}

func main() {
	img, err := readImage("test.png")
	if err != nil {
		log.Fatal(err)
	}

	hdri := newRGBA(img)
	fmt.Println(hdri.Width, hdri.Height)

	hdri.MultiplyRGBA(1.0, 1.0, 1.0, 0.8)

	img2 := hdri.ToImage()
	writeImage(img2, "test2.png")

	hdri.MultiplyRGBA(0.7, 0.7, 0.7, 1.0)
	hdri.AddRGBA(0.0, 0.0, 10000.0, 0.0)

	img3 := hdri.ToImage()
	writeImage(img3, "test3.png")
}
