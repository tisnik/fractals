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
	"log"

	"github.com/veandco/go-sdl2/sdl"
)

const (
	width  = 800
	height = 800
)

type Gfx interface {
	initialize()
	finalize()
	redraw()
	eventLoop()
}

type State struct {
	Window         *sdl.Window
	PrimarySurface *sdl.Surface
	inverse        bool
	S              float64
	R              float64
	B              float64
}

func NewState() State {
	return State{
		Window:         nil,
		PrimarySurface: nil,
		inverse:        false,
		S:              10.0,
		R:              28.0,
		B:              2.667,
	}
}

func (state *State) initialize() {
	err := sdl.Init(sdl.INIT_VIDEO)
	if err != nil {
		panic(err)
	}

	state.Window, err = sdl.CreateWindow("Strange attractors", sdl.WINDOWPOS_UNDEFINED, sdl.WINDOWPOS_UNDEFINED,
		width, height, sdl.WINDOW_SHOWN)
	if err != nil {
		panic(err)
	}

	state.PrimarySurface, err = state.Window.GetSurface()
	if err != nil {
		panic(err)
	}
}

func (state *State) finalize() {
	if state.PrimarySurface != nil {
		state.PrimarySurface.Free()
	}

	if state.Window != nil {
		err := state.Window.Destroy()
		if err != nil {
			log.Println(err)
		}
	}
	sdl.Quit()
}

func lorenz(x, y, z, s, r, b float64) (float64, float64, float64) {
	xDot := s * (y - x)
	yDot := r*x - y - x*z
	zDot := x*y - b*z
	return xDot, yDot, zDot
}

func (state *State) redraw() {
	backgroundColor := uint8(0x00)
	if state.inverse {
		backgroundColor = 0xff
	}

	err := state.PrimarySurface.FillRect(nil, sdl.MapRGB(state.PrimarySurface.Format, backgroundColor, backgroundColor, backgroundColor))
	if err != nil {
		log.Println(err)
		return
	}

	err = state.PrimarySurface.Lock()
	if err != nil {
		log.Println(err)
		return
	}

	dt := 0.001
	x := 0.0
	y := 1.0
	z := 1.05

	for i := 0; i < 200000; i++ {
		xn, yn, zn := lorenz(x, y, z, state.S, state.R, state.B)
		x = x + xn*dt
		y = y + yn*dt
		z = z + zn*dt
		if i > 1000 {
			r := byte(7)
			g := byte(7)
			b := byte(7)

			xi := int32(200.0 + 8.0*x)
			yi := int32(200.0 + 8.0*y)
			if state.inverse {
				subpixel(state.PrimarySurface, xi, yi, r, g, b)
			} else {
				addpixel(state.PrimarySurface, xi, yi, r, g, b)
			}

			xi = int32(200.0 + 8.0*x)
			yi = int32(400.0 + 8.0*z)
			if state.inverse {
				subpixel(state.PrimarySurface, xi, yi, r, g, b)
			} else {
				addpixel(state.PrimarySurface, xi, yi, r, g, b)
			}

			xi = int32(600.0 + 8.0*y)
			yi = int32(400.0 + 8.0*z)
			if state.inverse {
				subpixel(state.PrimarySurface, xi, yi, r, g, b)
			} else {
				addpixel(state.PrimarySurface, xi, yi, r, g, b)
			}
		}
	}
	state.PrimarySurface.Unlock()

	err = state.Window.UpdateSurface()
	if err != nil {
		log.Println(err)
	}
}

func (state *State) eventLoop() {
	var event sdl.Event
	done := false
	firstFrame := true

	for !done {
		redraw := firstFrame
		event = sdl.PollEvent()
		switch t := event.(type) {
		case *sdl.QuitEvent:
			done = true
		case *sdl.KeyboardEvent:
			keyCode := t.Keysym.Sym
			switch t.State {
			case sdl.PRESSED:
				switch keyCode {
				case sdl.K_ESCAPE:
					done = true
				case sdl.K_q:
					done = true
				case sdl.K_r:
					redraw = true
				case sdl.K_i:
					state.inverse = !state.inverse
					redraw = true
				}
			}
		}
		if redraw {
			state.redraw()
			firstFrame = false
		}
		sdl.Delay(10)
	}
	log.Println("Quitting")
}

func addSaturated(a byte, b byte) byte {
	var c byte = a + b
	if c < a { // can only happen due to overflow
		return 0xff
	}
	return c
}

func subSaturated(a byte, b byte) byte {
	var c byte = a - b
	if c > a { // can only happen due to underflow
		return 0x00
	}
	return c
}

func addpixel(surface *sdl.Surface, x int32, y int32, r byte, g byte, b byte) {
	if x >= 0 && x < surface.W && y >= 0 && y < surface.H {
		switch surface.Format.BitsPerPixel {
		case 24:
			index := x*3 + y*surface.Pitch
			pixels := surface.Pixels()
			pixels[index] = addSaturated(pixels[index], b)
			pixels[index+1] = addSaturated(pixels[index+1], g)
			pixels[index+2] = addSaturated(pixels[index+2], r)
		case 32:
			index := x*4 + y*surface.Pitch
			pixels := surface.Pixels()
			pixels[index] = addSaturated(pixels[index], b)
			pixels[index+1] = addSaturated(pixels[index+1], g)
			pixels[index+2] = addSaturated(pixels[index+2], r)
		}
	}
}

func subpixel(surface *sdl.Surface, x int32, y int32, r byte, g byte, b byte) {
	if x >= 0 && x < surface.W && y >= 0 && y < surface.H {
		switch surface.Format.BitsPerPixel {
		case 24:
			index := x*3 + y*surface.Pitch
			pixels := surface.Pixels()
			pixels[index] = subSaturated(pixels[index], b)
			pixels[index+1] = subSaturated(pixels[index+1], g)
			pixels[index+2] = subSaturated(pixels[index+2], r)
		case 32:
			index := x*4 + y*surface.Pitch
			pixels := surface.Pixels()
			pixels[index] = subSaturated(pixels[index], b)
			pixels[index+1] = subSaturated(pixels[index+1], g)
			pixels[index+2] = subSaturated(pixels[index+2], r)
		}
	}
}

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

func main() {
	state := NewState()
	state.initialize()
	defer state.finalize()

	sdl.Delay(10)
	state.eventLoop()
}
