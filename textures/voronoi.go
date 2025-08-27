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
	"math"

	"github.com/veandco/go-sdl2/sdl"
)

const (
	width  = 640
	height = 480
)

// putpixel sets the pixel at (x, y) on surface to the specified RGB color.
// It checks bounds and writes directly into the surface pixel buffer for
// 24- and 32-bit surface formats. For 24-bit surfaces bytes are written as
// B, G, R (3 bytes per pixel); for 32-bit surfaces the same order is used
// (alpha is not modified). If (x, y) is out of bounds or the format is
// unsupported no write is performed.
func putpixel(surface *sdl.Surface, x int32, y int32, r byte, g byte, b byte) {
	if x >= 0 && x < surface.W && y >= 0 && y < surface.H {
		switch surface.Format.BitsPerPixel {
		case 24:
			index := x*3 + y*surface.Pitch
			pixels := surface.Pixels()
			pixels[index] = b
			pixels[index+1] = g
			pixels[index+2] = r
		case 32:
			index := x*4 + y*surface.Pitch
			pixels := surface.Pixels()
			pixels[index] = b
			pixels[index+1] = g
			pixels[index+2] = r
		}
	}
}

type Point struct {
	X float64
	Y float64
}

// main is the program entry point.
// It initializes SDL video, creates a 640×480 window, rasterizes a grayscale Voronoi-like diagram
// by sampling distance to a fixed set of 2D sites (clamped to 0–255) and writes pixels directly
// to the window surface, updates the surface, then exits after a short delay.
func main() {
	if err := sdl.Init(sdl.INIT_VIDEO); err != nil {
		panic(err)
	}
	defer sdl.Quit()

	window, err := sdl.CreateWindow("Texture based on Voronoi diagram", sdl.WINDOWPOS_UNDEFINED, sdl.WINDOWPOS_UNDEFINED,
		width, height, sdl.WINDOW_SHOWN)
	if err != nil {
		panic(err)
	}
	defer window.Destroy()

	primarySurface, err := window.GetSurface()
	if err != nil {
		panic(err)
	}

	points := []Point{
		{100, 200},
		{200, 100},
		{500, 100},
		{400, 420},
		{150, 50},
		{250, 400},
		{550, 520},
		{400, 100},
	}
	for y := int32(0); y < height; y++ {
		for x := int32(0); x < width; x++ {
			var color byte = 0
			var minDistance float64 = math.MaxFloat64
			for i := 0; i < len(points); i++ {
				distance := math.Hypot(float64(x)-points[i].X, float64(y)-points[i].Y)
				if distance < minDistance {
					d := distance
					if d > 255 {
						d = 255
					}
					color = byte(d)
					minDistance = distance
				}
			}
			putpixel(primarySurface, x, y, color, color, color)
		}
	}

	sdl.Delay(100)

	window.UpdateSurface()

	sdl.Delay(2000)
}
