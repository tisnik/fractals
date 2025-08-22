package main

import (
	"bufio"
	"fmt"
	"image"
	"image/png"
	"log"
	"math"
	"math/rand/v2"
	"os"
)

type Palette [][]byte

// LoadTextRGBPalette loads a palette of RGB colors from a whitespace-separated text file.
// Each non-empty line of the file must contain three integers ("R G B") in the 0–255 range;
// those triplets are converted to byte RGB entries and appended to the returned Palette.
// LoadTextRGBPalette will call log.Fatal and exit the program on unrecoverable errors such as
// failure to open the file, a scanning error, or a failed integer parse; lines that do not
// contain exactly three integers are logged (via log.Println) and skipped from the palette.
// It returns the populated Palette and an error value (which is typically nil given the
// function's use of log.Fatal for many error conditions).
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

// NewPNGImageWriter returns a new PNGImageWriter instance.
// The returned writer is a lightweight value (empty struct) used to encode images as PNG.
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

// zimage[y][x]).
func NewZImage(width uint, height uint) ZImage {
	zimage := make([][]ZPixel, height)
	for i := uint(0); i < height; i++ {
		zimage[i] = make([]ZPixel, width)
	}
	return zimage
}

// complexImageToImage converts a ZImage into an *image.NRGBA by mapping each pixel's
// Iter value to an RGB entry from palette. The image has the specified width and
// height; each pixel's alpha is set to 0xff. The function casts Iter to a byte
// (low 8 bits) when indexing the palette, so only the lower 8 bits of Iter are used.
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

// randomGauss returns an approximately Gaussian-distributed float32 in [0,1)
// produced by averaging 50 independent uniform(0,1) samples (Central Limit
// Theorem). The result has mean ~0.5 and reduced variance compared to a single
// uniform sample.
func randomGauss() float32 {
	const N = 50
	sum := float32(0)
	for range N {
		sum += rand.Float32()
	}
	return sum / N
}

type FImage [][]float32

// NewFImage returns a new FImage with the specified width and height.
// The result is a slice of `height` rows, each being a slice of `width` float32 values.
// Pixels should be accessed as `img[y][x]`; all values are zero-initialized.
func NewFImage(width uint, height uint) FImage {
	fimage := make([][]float32, height)
	for i := uint(0); i < height; i++ {
		fimage[i] = make([]float32, width)
	}
	return fimage
}
// minMax returns the minimum and maximum float32 values found in img
// over the provided width and height bounds.
// The return values are (min, max). If the scanned region is empty
// (for example when width or height is zero), min will be +Inf and
// max will be -Inf. The caller must ensure width and height match img's dimensions.
func minMax(img FImage, width, height uint) (float32, float32) {
	min := float32(math.Inf(1))
	max := float32(math.Inf(-1))

	for j := range height {
		for i := range width {
			z := img[j][i]
			if max < z {
				max = z
			}
			if min > z {
				min = z
			}
		}
	}
	return min, max
}

// floatImageToImage converts an FImage into an *image.NRGBA sized width×height.
// It linearly normalizes fimage values using the image minimum and maximum to the
// 0–255 range, then maps each normalized value (low 8 bits) into an RGB color
// from palette and writes alpha=0xff.
//
// palette is expected to contain 256 entries where each entry is a 3-byte RGB
// triplet (R,G,B). Behavior is undefined if all fimage values are equal
// (min == max), which would cause a divide-by-zero during scaling.
func floatImageToImage(fimage FImage, width uint, height uint, palette Palette) image.Image {
	image := image.NewNRGBA(image.Rect(0, 0, int(width), int(height)))
	min, max := minMax(fimage, width, height)
	k := 255.0 / (max - min)

	for y := uint(0); y < height; y++ {
		offset := image.PixOffset(0, int(y))
		for x := uint(0); x < width; x++ {
			f := fimage[y][x]
			f -= min
			f *= k
			i := int(f) & 255
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

// spectralSynthesis fills img (width × height) with a fractal/plasma-like field using
// spectral synthesis.
//
// The function generates two small frequency-domain spectra (A and B) of size
// (n/2) × (n/2) whose amplitudes follow a power-law ~ k^{-beta/2} with beta = 2*h+1
// and randomized Gaussian-modulated phases. It then synthesizes the spatial field by
// summing cosine and sine basis functions over those frequencies and writes the
// resulting float values into img in-place.
//
// Parameters:
// - img: destination FImage that will be populated; it must be indexed as img[0..height-1][0..width-1].
// - width, height: dimensions of the target image.
// - n: size parameter for the spectral grid (the code uses n/2 × n/2 frequency components).
// - h: controls the spectral slope (higher h produces smoother fields).
//
// Notes:
// - The function mutates img directly and does not return a value.
// - n should be chosen so that n/2 matches the intended frequency resolution.
func spectralSynthesis(img FImage, width, height uint, n uint, h float32) {
	A := NewFImage(n/2, n/2)
	B := NewFImage(n/2, n/2)
	beta := float64(2.0*h + 1)

	for j := range n / 2 {
		for i := range n / 2 {
			rad_i := math.Pow(float64(i)+1.0, -beta/2.0) * float64(randomGauss())
			rad_j := math.Pow(float64(j)+1.0, -beta/2.0) * float64(randomGauss())
			phase_i := 2.0 * math.Pi * rand.Float64()
			phase_j := 2.0 * math.Pi * rand.Float64()
			A[j][i] = float32(rad_i * math.Cos(phase_i) * rad_j * math.Cos(phase_j))
			B[j][i] = float32(rad_i * math.Sin(phase_i) * rad_j * math.Sin(phase_j))
		}
	}

	for j := range height {
		for i := range width {
			z := 0.0
			for k := range n / 2 {
				for l := range n / 2 {
					u := float64(i) * 2.0 * math.Pi / float64(width)
					v := float64(j) * 2.0 * math.Pi / float64(height)
					w := float64(k)*u + float64(l)*v
					z += float64(A[k][l])*math.Cos(w) +
						float64(B[k][l])*math.Sin(w)
				}
			}
			img[j][i] = float32(z)
		}
	}
}

// main is the program entry point. It loads an RGB palette from "mandmap.map",
// generates a 512×512 plasma-like image via spectral synthesis, maps the computed
// float values to colors using the palette, and writes the result to "plasma.png".
func main() {
	palette, err := LoadTextRGBPalette("mandmap.map")
	if err != nil {
		panic(err)
	}
	fimage := NewFImage(512, 512)
	spectralSynthesis(fimage, 512, 512, 4, 0.5)
	image := floatImageToImage(fimage, 512, 512, palette)
	imageWriter := NewPNGImageWriter()
	imageWriter.WriteImage("plasma.png", image)
}
