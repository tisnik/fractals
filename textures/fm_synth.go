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

// Palette represents color palette - mapping between index and RGB color
// components.
type Palette [][]byte

// LoadTextRGBPalette loads an RGB palette from a text file where each line
// contains three integers representing R, G, and B color components (red,
// gree, blue).
//
// It opens filename, reads it line-by-line and for each line parses three
// integers (red, green, blue), converts them to bytes and appends the 3-byte
// color to the returned Palette slice. Lines that do not contain exactly three
// items are logged and skipped (the parsed values still produce a color).
//
// Note: this function uses log.Fatal on file open, parse, or scanner errors,
// which will log the error and terminate the program; on successful completion
// it returns the constructed Palette and a nil error.
func LoadTextRGBPalette(filename string) (Palette, error) {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	// make sure the file is closed after the function finishes
	defer file.Close()

	var palette Palette

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// read one text line from the file
		line := scanner.Text()
		// parse three color components
		var red, green, blue int
		items, err := fmt.Sscanf(line, "%d %d %d", &red, &green, &blue)
		if err != nil {
			log.Fatal(err)
		}
		if items != 3 {
			log.Println("not expected line:", line)
		}
		// append new color into the color palette
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

// WritePNGImage writes an image represented by standard image.Image data
// structure into file with PNG format.
func (writer PNGImageWriter) WriteImage(filename string, img image.Image) error {
	outfile, err := os.Create(filename)
	if err != nil {
		panic(err)
	}
	// make sure the file is closed after the function finishes
	defer outfile.Close()
	return png.Encode(outfile, img)
}

// NewPNGImageWriter returns a PNGImageWriter ready to encode and write PNG
// images.
//
// The returned value is an empty struct value used to call WriteImage for PNG encoding.
func NewPNGImageWriter() PNGImageWriter {
	return PNGImageWriter{}
}

// ZPixel is a representation of pixel in complex plane with additional
// metadata - number of iterations.
type ZPixel struct {
	Iter uint
	Z    complex128
}

// ZImage is representation of raster image consisting of ZPixels
type ZImage [][]ZPixel

// NewZImage creates a new ZImage with the given width (columns) and height
// (rows).
//
// The returned ZImage is a height-by-width 2D slice (indexed as zimage[y][x])
// with all ZPixel elements zero-initialized.
func NewZImage(width uint, height uint) ZImage {
	zimage := make([][]ZPixel, height)
	for i := uint(0); i < height; i++ {
		zimage[i] = make([]ZPixel, width)
	}
	return zimage
}

// complexImageToImage function converts a ZImage raster image representation
// into an image.NRGBA of the given width and height, mapping each pixel's Iter
// value to an RGB triple from the provided palette and setting the alpha
// channel to 0xff.
//
// The function treats each pixel at (x,y) in zimage as an index: it uses the
// low 8 bits of zimage[y][x].Iter (cast to byte) to select palette[i] which is
// expected to be a 3-byte RGB slice. The returned image has bounds
// [0,0]–[width,height). No bounds checks are performed on palette lookups;
// out-of-range or malformed palette entries may cause a runtime panic.
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

// renderFMPattern fills ZImage structure with a sinusoidal (FM-style) pattern
// by setting each pixel's Iter.
//
// The function treats ZImage data structure as a height-by-width grid (rows =
// height, cols = width) and samples the continuous rectangle defined by (xmin,
// ymin) to (xmax, ymax). For each pixel at image coordinate (x,y) it computes
// a value using a nested sine formula, converts that value to an integer,
// masks it to the low 8 bits, and stores it in the pixel's Iter field. Iter
// values are therefore in the range 0–255 and are intended as indices into a
// palette.
//
// Parameters:
// - zimage: destination image buffer; must have dimensions [height][width].
// - width, height: image dimensions used to compute sampling step sizes.
// - xmin, ymin, xmax, ymax: bounds of the sampled coordinate region.
//
// The function does not return a value; it mutates zimage parameter in place
// instead.
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

// main is the program entry point. It loads an RGB palette from "mandmap.map"
// (panics on load error), creates a 512×512 ZImage, renders FM-like texture
// pattern.
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
