package main

import (
	"image"
	"image/color"
	"image/png"
	"math"
	"math/rand/v2"
	"os"
)

const ImageWidth = 800
const ImageHeight = 600
const Maxiter = 20000

func computeMinMax(bitmap [][]float64, width, height int) (float64, float64) {
	minValue := math.MaxFloat64
	maxValue := -math.MaxFloat64
	for j := range height {
		for i := range width {
			z := bitmap[j][i]
			if maxValue < z {
				maxValue = z
			}
			if minValue > z {
				minValue = z
			}
		}
	}
	return minValue, maxValue
}

func CreateBitmap(width, height int) [][]float64 {
	result := make([][]float64, height)
	for i := range height {
		result[i] = make([]float64, width)
	}
	return result
}

func DrawBitmapToImage(bitmap [][]float64, image *image.RGBA, maxFactor float64) {
	size := image.Bounds().Size()
	width := size.X
	height := size.Y

	min, max := computeMinMax(bitmap, width, height)
	max *= maxFactor
	k := 255.0 / (max - min)
	for y := range height {
		for x := range width {
			f := bitmap[y][x]
			f -= min
			f *= k
			if f > 255.0 {
				f = 255
			}
			i := uint8(int(f) & 255)
			i = 255 - i
			c := color.RGBA{i, i, i, 255}
			image.SetRGBA(int(x), int(y), c)
		}
	}
}

func SaveImage(img *image.RGBA, filename string) {
	outfile, err := os.Create(filename)
	if err != nil {
		panic(err)
	}
	defer outfile.Close()

	err = png.Encode(outfile, img)
	if err != nil {
		panic(err)
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func hline(bitmap [][]float64, x1, x2, y int) {
	fromX := min(x1, x2)
	toX := max(x1, x2)

	for x := fromX; x <= toX; x++ {
		bitmap[y][x] += 1.0
	}
}

func vline(bitmap [][]float64, x, y1, y2 int) {
	fromY := min(y1, y2)
	toY := max(y1, y2)

	for y := fromY; y <= toY; y++ {
		bitmap[y][x] += 1.0
	}
}

func line(bitmap [][]float64, x1 int, y1 int, x2 int, y2 int) {
	dx := abs(x2 - x1)
	dy := abs(y2 - y1)
	sx := 1
	sy := 1
	if x1 >= x2 {
		sx = -1
	}
	if y1 >= y2 {
		sy = -1
	}
	err := dx / 2
	if dx <= dy {
		err = -dy / 2
	}

	for {
		bitmap[y1][x1] += 1.0
		if x1 == x2 && y1 == y2 {
			break
		}
		e2 := err
		if e2 > -dx {
			err -= dy
			x1 += sx
		}
		if e2 < dy {
			err += dx
			y1 += sy
		}
	}
}

func calcSystem(width, height, maxiter int) *image.RGBA {
	img := image.NewRGBA(image.Rect(0, 0, width, height))

	bmp := CreateBitmap(width, height)

	for range maxiter {
		line(bmp, rand.IntN(width), rand.IntN(height), rand.IntN(width), rand.IntN(height))
	}

	DrawBitmapToImage(bmp, img, 1.0)
	return img
}

func main() {
	img := calcSystem(ImageWidth, ImageHeight, Maxiter)
	SaveImage(img, "T.png")
}
