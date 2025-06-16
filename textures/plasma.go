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

func randomGauss() float32 {
	const N = 50
	sum := float32(0)
	for range N {
		sum += rand.Float32()
	}
	return sum / N
}

type FImage [][]float32

// NewFImage constructs new instance of FImage
func NewFImage(width uint, height uint) FImage {
	fimage := make([][]float32, height)
	for i := uint(0); i < height; i++ {
		fimage[i] = make([]float32, width)
	}
	return fimage
}
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
