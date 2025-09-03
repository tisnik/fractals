// MIT License
//
// Copyright (c) 2020 Pavel Tišnovský
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

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

// New creates and returns a Bitmap whose underlying image is a new image.RGBA
// sized to the given width and height. The image bounds run from (0,0) to
// (width, height) — i.e., valid pixel coordinates are 0 ≤ x < width and
// 0 ≤ y < height.
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

// abs returns the absolute value of a.
func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

// max returns the larger of a and b.
func max(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

// min returns the smaller of a and b.
func min(a int, b int) int {
	if a < b {
		return a
	}
	return b
}

// hLine draws a horizontal black line on bitmap from x1 to x2 (inclusive) at row y.
// The endpoints may be provided in any order; the function iterates from the lesser
// to the greater x and sets each pixel to black.
func hLine(bitmap *bitmap.Bitmap, x1 int, x2 int, y int) {
	fromX := min(x1, x2)
	toX := max(x1, x2)
	for x := fromX; x <= toX; x++ {
		bitmap.Putpixel(x, y, 0, 0, 0)
	}
}

// vLine draws a vertical black line on bitmap at column x from y1 to y2 (inclusive).
// The function handles the order of y1 and y2 by using their min and max.
func vLine(bitmap *bitmap.Bitmap, x int, y1 int, y2 int) {
	fromY := min(y1, y2)
	toY := max(y1, y2)
	for y := fromY; y <= toY; y++ {
		bitmap.Putpixel(x, y, 0, 0, 0)
	}
}

// line draws a straight anti-aliased-ish grayscale line on the provided bitmap between (x1,y1) and (x2,y2).
// It handles pure vertical and horizontal cases via specialized routines and otherwise steps along the major axis,
// writing two adjacent pixels per step with complementary gray values to produce a smooth-looking stroke.
// Coordinates may be reordered internally so x1<=x2; the function modifies the bitmap in-place.
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

// nprLine draws a non-photorealistic (hand-drawn) line between (x1,y1) and (x2,y2).
// For short segments (Manhattan distance < 20) it draws a straight line; for longer
// segments it recursively subdivides the segment at its midpoint, displacing that
// midpoint perpendicular to the segment by a random amount up to ±maxd, and then
// continues on the two subsegments with maxd reduced by a factor of 1.8.
//
// The bitmap parameter is the target to draw into. The maxd parameter controls
// the maximum perpendicular displacement applied at each subdivision (higher
// values produce rougher, more "sketchy" lines).
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

// drawDemo renders a series of horizontal non-photorealistic lines across the image.
//
// It draws lines from x=50 to x=width-50 at y positions 25, 50, ..., 475. For each
// line it seeds the global RNG with 6503 (resetting randomness for every line) and
// calls nprLine with a maximum displacement proportional to the iteration index
// (maxd = i/2.0).
//
// The bitmap parameter is the target image to draw onto.
func drawDemo(bitmap *bitmap.Bitmap) {
	for i := 0; i < 500; i += 25 {
		rand.Seed(6503)
		nprLine(bitmap, 50, 25+i, width-50, 25+i, float64(i)/2.0)
	}
}

// drawSquare draws a square by rendering four non-photorealistic line segments.
// The square's corners are at (20,20) and (200,200); each edge is drawn via
// nprLine with a maximum midpoint displacement of 10, modifying the provided bitmap.
func drawSquare(bitmap *bitmap.Bitmap) {
	nprLine(bitmap, 20, 20, 200, 20, 10)
	nprLine(bitmap, 200, 20, 200, 200, 10)
	nprLine(bitmap, 20, 200, 200, 200, 10)
	nprLine(bitmap, 20, 200, 20, 20, 10)
}

// drawDiamond draws a diamond-shaped outline near (60,160) using non-photorealistic lines.
//
// It renders four NPR-subdivided edges (width 50) connected around the center point (60,160),
// each edge drawn with a displacement strength of 10 via nprLine.
func drawDiamond(bitmap *bitmap.Bitmap) {
	const W = 50
	nprLine(bitmap, 60-W, 160, 60, 160-W, 10)
	nprLine(bitmap, 60, 160-W, 60+W, 160, 10)
	nprLine(bitmap, 60+W, 160, 60, 160+W, 10)
	nprLine(bitmap, 60, 160+W, 60-W, 160, 10)
}

// drawStar draws a five-point star composed of non-photorealistic lines.
// It emits STEP (5) radial segments by connecting points on a circle of
// radius 200 centered at (400,220). Each segment is drawn with nprLine
// using a displacement magnitude of 10 to produce the stylized, hand-drawn look.
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

// main creates a 512×512 white canvas, draws several non-photorealistic line-art shapes
// (a set of rasterized demo lines, a square, a diamond, and a star), writes "Draw lines"
// to stdout, and saves the resulting image to "test.png".
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
