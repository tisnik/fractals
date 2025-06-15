package main

import (
	"bufio"
	"fmt"
	"image"
	"image/png"
	"log"
	"math"
	"os"
)

type Palette [][]byte

func LoadTextRGBPalette(filename string) (Palette, error) {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var palette Palette

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		var red, green, blue int
		items, err := fmt.Sscanf(line, "%d %d %d", &red, &green, &blue)
		if err != nil {
			log.Fatal(err)
		}
		if items != 3 {
			log.Println("not expected line:", line)
		}
		color := []byte{byte(red), byte(green), byte(blue)}
		palette = append(palette, color)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return palette, err
}

// PNGImageWriter implements image.Writer interface, it writes PNG format
type PNGImageWriter struct{}

// WritePNGImage writes an image represented by standard image.Image structure into file with PNG format.
func (writer PNGImageWriter) WriteImage(filename string, img image.Image) error {
	outfile, err := os.Create(filename)
	if err != nil {
		panic(err)
	}
	defer outfile.Close()
	return png.Encode(outfile, img)
}

// NewPNGImageWriter is a constructor for PNG image writer
func NewPNGImageWriter() PNGImageWriter {
	return PNGImageWriter{}
}

// ZPixel is a representation of pixel in complex plane with additional metadata
type ZPixel struct {
	Iter uint
	Z    complex128
}

// ZImage is representation of raster image consisting of ZPixels
type ZImage [][]ZPixel

// NewZImage constructs new instance of ZImage
func NewZImage(width uint, height uint) ZImage {
	zimage := make([][]ZPixel, height)
	for i := uint(0); i < height; i++ {
		zimage[i] = make([]ZPixel, width)
	}
	return zimage
}

func complexImageToImage(zimage ZImage, width uint, height uint, palette Palette) image.Image {
	image := image.NewNRGBA(image.Rect(0, 0, int(width), int(height)))

	for y := 0; y < int(height); y++ {
		offset := image.PixOffset(0, y)
		for x := uint(0); x < width; x++ {
			i := byte(zimage[y][x].Iter)
			image.Pix[offset] = palette[i][0]
			offset++
			image.Pix[offset] = palette[i][1]
			offset++
			image.Pix[offset] = palette[i][2]
			offset++
			image.Pix[offset] = 0xff
			offset++
		}
	}
	return image
}

func renderFMPattern(zimage ZImage, width uint, height uint, xmin, ymin, xmax, ymax float32) {
	stepx := (xmax - xmin) / float32(width)
	stepy := (ymax - ymin) / float32(height)

	y1 := ymin
	for y := range height {
		x1 := xmin
		for x := range width {
			val := 100.0 + 100.0*math.Sin(float64(x1)/4.0+2*math.Sin(float64(x1)/15.0+float64(y1)/40.0))
			i := int(val) & 255
			zimage[y][x] = ZPixel{Iter: uint(i)}
			x1 += stepx
		}
		y1 += stepy
	}
}

func main() {
	palette, err := LoadTextRGBPalette("mandmap.map")
	if err != nil {
		panic(err)
	}
	zimage := NewZImage(512, 512)
	renderFMPattern(zimage, 512, 512, -100.0, -100.0, 100.0, 100.0)
	image := complexImageToImage(zimage, 512, 512, palette)
	imageWriter := NewPNGImageWriter()
	imageWriter.WriteImage("fm1.png", image)
}
