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
	"image"
	"image/color"
	"image/png"
	"math/rand"
	"net/http"
)

func indexPageHandler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "text/html")
	response := `
<body>
    <h1>Enterprise image renderer</h1>
    <img src="/image1" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image2" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image3" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image4" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image5" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image6" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image7" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image8" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image9" width=256 height=256 style='padding:0;border:0;margin:0' />
</body>`
	writer.Write([]byte(response))
}

func calculateColor() color.RGBA {
	return color.RGBA{uint8(rand.Intn(255)),
		uint8(rand.Intn(255)),
		uint8(rand.Intn(255)), 255}
}

func iterCount(cx float64, cy float64, maxiter uint) uint {
	var zx float64 = 0.0
	var zy float64 = 0.0
	var i uint = 0
	for i < maxiter {
		zx2 := zx * zx
		zy2 := zy * zy
		if zx2+zy2 > 4.0 {
			break
		}
		zy = 2.0*zx*zy + cy
		zx = zx2 - zy2 + cx
		i++
	}
	return i
}

func calcMandelbrot(width uint, height uint, maxiter uint, image []byte, cy float64, done chan bool) {
	var cx float64 = -2.0
	for x := uint(0); x < width; x++ {
		i := iterCount(cx, cy, maxiter)
		image[3*x] = byte(i * 2)
		image[3*x+1] = byte(i * 3)
		image[3*x+2] = byte(i * 5)
		cx += 3.0 / float64(width)
	}
	done <- true
}

func writeImage(width uint, height uint, pixels []byte) *image.NRGBA {
	img := image.NewNRGBA(image.Rect(0, 0, int(width), int(height)))
	pixel := 0

	for y := 0; y < int(height); y++ {
		offset := img.PixOffset(0, y)
		for x := uint(0); x < width; x++ {
			img.Pix[offset] = pixels[pixel]
			img.Pix[offset+1] = pixels[pixel+1]
			img.Pix[offset+2] = pixels[pixel+2]
			img.Pix[offset+3] = 0xff
			pixel += 3
			offset += 4
		}
	}
	return img
}

func calculateFractal(width int, height int, maxiter int) []byte {
	done := make(chan bool, height)

	pixels := make([]byte, width*height*3)
	offset := 0
	delta := width * 3

	var cy float64 = -1.5 + rand.Float64() - 0.5
	var dist float64 = 2.0 + 2.0*rand.Float64() - 1.0
	for y := 0; y < height; y++ {
		calcMandelbrot(uint(width), uint(height), uint(maxiter), pixels[offset:offset+delta], cy, done)
		//go calcMandelbrot(uint(width), uint(height), uint(maxiter), pixels[offset:offset+delta], cy, done)
		offset += delta
		cy += dist / float64(height)
	}
	for i := 0; i < height; i++ {
		<-done
	}

	return pixels
}

func imageHandler(w http.ResponseWriter, r *http.Request) {
	const ImageWidth = 256
	const ImageHeight = 256

	pixels := calculateFractal(ImageWidth, ImageHeight, 255)
	outputimage := writeImage(ImageWidth, ImageHeight, pixels)
	png.Encode(w, outputimage)
}

func main() {
	http.HandleFunc("/", indexPageHandler)
	http.HandleFunc("/image1", imageHandler)
	http.HandleFunc("/image2", imageHandler)
	http.HandleFunc("/image3", imageHandler)
	http.HandleFunc("/image4", imageHandler)
	http.HandleFunc("/image5", imageHandler)
	http.HandleFunc("/image6", imageHandler)
	http.HandleFunc("/image7", imageHandler)
	http.HandleFunc("/image8", imageHandler)
	http.HandleFunc("/image9", imageHandler)
	http.ListenAndServe(":8080", nil)
}
