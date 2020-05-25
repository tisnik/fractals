package main

import (
	"math"

	"github.com/veandco/go-sdl2/sdl"
)

const (
	width  = 640
	height = 480
)

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
