package main

import (
	"fmt"
	"math"
	"math/rand"

	"image"
	"image/color"
	"image/png"
	"os"

	"gfx/bitmap"
)

const width = 512
const height = 512

type Bitmap struct {
	image *image.RGBA
}

func New(width int, height int) Bitmap {
	image := image.NewRGBA(image.Rect(0, 0, width, height))
	return Bitmap{image: image}
}

func (bitmap Bitmap) Putpixel(x int, y int, red byte, green byte, blue byte) {
	c := color.RGBA{red, green, blue, 255}
	bitmap.image.SetRGBA(x, y, c)
}

func (bitmap Bitmap) Save(filename string) error {
	outfile, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer outfile.Close()
	png.Encode(outfile, bitmap.image)
	return nil
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

func hLine(bitmap *bitmap.Bitmap, x1 int, x2 int, y int) {
	fromX := min(x1, x2)
	toX := max(x1, x2)
	for x := fromX; x <= toX; x++ {
		bitmap.Putpixel(x, y, 0, 0, 0)
	}
}

func vLine(bitmap *bitmap.Bitmap, x int, y1 int, y2 int) {
	fromY := min(y1, y2)
	toY := max(y1, y2)
	for y := fromY; y <= toY; y++ {
		bitmap.Putpixel(x, y, 0, 0, 0)
	}
}

func line(bitmap *bitmap.Bitmap, x1 int, y1 int, x2 int, y2 int) {
	dx := x2 - x1
	dy := y2 - y1
	var s float64
	var p float64
	var e float64 = 255.0
	var x, y, xdelta, ydelta, xpdelta, ypdelta, xp, yp int
	var imin, imax int

	if x1 == x2 {
		vLine(bitmap, x1, y1, y2)
		return
	}

	if y1 == y2 {
		hLine(bitmap, x1, x2, y1)
		return
	}

	if x1 > x2 {
		x1, x2 = x2, x1
		y1, y2 = y2, y1
	}

	if abs(dx) > abs(dy) {
		s = float64(dy) / float64(dx)
		imin = x1
		imax = x2
		x = x1
		y = y1
		xdelta = 1
		ydelta = 0
		xpdelta = 0
		xp = 0
		if y2 > y1 {
			ypdelta = 1
			yp = 1
		} else {
			s = -s
			ypdelta = -1
			yp = -1
		}
	} else {
		s = float64(dx) / float64(dy)
		xdelta = 0
		ydelta = 1
		ypdelta = 0
		yp = 0
		if y2 > y1 {
			imin = y1
			imax = y2
			x = x1
			y = y1
			xpdelta = 1
			xp = 1
		} else {
			s = -s
			imin = y2
			imax = y1
			x = x2
			y = y2
			xpdelta = -1
			xp = -1
		}
	}
	p = s * 256.0
	for i := imin; i <= imax; i++ {
		var c1 byte = byte(e)
		var c2 byte = 255 - c1
		bitmap.Putpixel(x+xp, y+yp, c1, c1, c1)
		bitmap.Putpixel(x, y, c2, c2, c2)
		e = e - p
		x += xdelta
		y += ydelta
		if e < 0.0 {
			e += 256.0
			x += xpdelta
			y += ypdelta
		}
	}
}

func nprLine(bitmap *bitmap.Bitmap, x1 int, y1 int, x2 int, y2 int, maxd float64) {
	dist := abs(x2-x1) + abs(y2-y1)

	if dist < 20 {
		line(bitmap, x1, y1, x2, y2)
	} else {
		midx := (x1 + x2) >> 1
		midy := (y1 + y2) >> 1

		nx := float64(y1 - y2)
		ny := float64(x2 - x1)
		nd := math.Sqrt(nx*nx + ny*ny)
		nx /= nd
		ny /= nd
		d := maxd * (rand.Float64() - 0.5)
		midx += int(nx * d)
		midy += int(ny * d)
		nprLine(bitmap, x1, y1, midx, midy, maxd/1.8)
		nprLine(bitmap, midx, midy, x2, y2, maxd/1.8)
	}
}

func drawDemo(bitmap *bitmap.Bitmap) {
	for i := 0; i < 500; i += 25 {
		rand.Seed(6503)
		nprLine(bitmap, 50, 25+i, width-50, 25+i, float64(i)/2.0)
	}
}

func drawSquare(bitmap *bitmap.Bitmap) {
	nprLine(bitmap, 20, 20, 200, 20, 10)
	nprLine(bitmap, 200, 20, 200, 200, 10)
	nprLine(bitmap, 20, 200, 200, 200, 10)
	nprLine(bitmap, 20, 200, 20, 20, 10)
}

func drawDiamond(bitmap *bitmap.Bitmap) {
	const W = 50
	nprLine(bitmap, 60-W, 160, 60, 160-W, 10)
	nprLine(bitmap, 60, 160-W, 60+W, 160, 10)
	nprLine(bitmap, 60+W, 160, 60, 160+W, 10)
	nprLine(bitmap, 60, 160+W, 60-W, 160, 10)
}

func drawStar(bitmap *bitmap.Bitmap) {
	const STEP = 5
	for i := 0; i < 360; i += 360 / STEP {
		x1 := 200.0 * math.Cos(float64(i)*math.Pi/180.0)
		y1 := 200.0 * math.Sin(float64(i)*math.Pi/180.0)
		x2 := 200.0 * math.Cos((float64(i)+3*360/STEP)*math.Pi/180.0)
		y2 := 200.0 * math.Sin((float64(i)+3*360/STEP)*math.Pi/180.0)
		nprLine(bitmap, 400+int(x1), 220+int(y1), 400+int(x2), 220+int(y2), 10)
	}
}
func main() {
	bitmap := bitmap.New(width, height)

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			bitmap.Putpixel(x, y, 255, 255, 255)
		}
	}
	fmt.Println("Draw lines")

	drawDemo(&bitmap)
	drawSquare(&bitmap)
	drawDiamond(&bitmap)
	drawStar(&bitmap)

	err := bitmap.Save("test.png")
	if err != nil {
		panic(err)
	}
}
