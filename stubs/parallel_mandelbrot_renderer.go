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

// indexPageHandler writes a minimal HTML page that embeds nine 256×256 image
// endpoints (/image1–/image9).  It sets the response Content-Type to
// "text/html" and writes the static HTML body directly to the response.
//
// Note: it does not perform error handling for potential write failures.
func indexPageHandler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "text/html")
	response := `
<body>
    <h1>Enterprise image renderer</h1>
    <img src="/image1" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image2" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image3" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image4" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image5" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image6" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image7" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image8" width=256 height=256 style='padding:0;border:0;margin:0' /><img src="/image9" width=256 height=256 style='padding:0;border:0;margin:0' />
</body>`
	writer.Write([]byte(response))
}

// calculateColor returns a random opaque color.RGBA where each RGB component
// is in the range 0–254 (via math/rand) and alpha is fixed at 255.
func calculateColor() color.RGBA {
	return color.RGBA{uint8(rand.Intn(255)),
		uint8(rand.Intn(255)),
		uint8(rand.Intn(255)), 255}
}

// iterCount computes the Mandelbrot "escape time" for the point (cx, cy).
//
// It iterates z_{n+1} = z_n^2 + c starting from z0 = 0 and returns the number
// of iterations performed before |z|^2 exceeds 4 (escape), or maxiter if the
// point did not escape within the given limit.
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

// Calculates all pixels on line and then sends `true` on the `done` channel to
// indicate the row is complete.
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

// writeImage converts a packed RGB byte buffer into an *image.NRGBA of the
// given dimensions.
//
// The pixels slice must contain exactly width*height*3 bytes in row-major
// order with three bytes per pixel (R, G, B). The resulting image will have
// its alpha channel set to 0xFF for every pixel. If pixels is shorter than
// required, the function will panic due to out-of-range indexing.
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

// - maxiter: maximum Mandelbrot iterations passed to calcMandelbrot.
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

// imageHandler generates a 256x256 Mandelbrot PNG and writes it to the
// provided HTTP response.
//
// It computes pixel data by calling calculateFractal(width, height, 255),
// converts that buffer into an *image.NRGBA via writeImage, and encodes the
// result as PNG to the response writer.
//
// Note: the function does not set response headers or handle encoding errors.
func imageHandler(w http.ResponseWriter, r *http.Request) {
	const ImageWidth = 256
	const ImageHeight = 256

	w.Header().Set("Content-Type", "image/png")
	pixels := calculateFractal(ImageWidth, ImageHeight, 255)
	outputimage := writeImage(ImageWidth, ImageHeight, pixels)
	png.Encode(w, outputimage)
}

// main starts an HTTP server listening on :8080 and registers handlers for the
// root index page and nine image endpoints.
//
// The root path ("/") is served by indexPageHandler and each "/image1" through
// "/image9" path is served by imageHandler, which generates 256×256 Mandelbrot
// PNG images on demand. The call to ListenAndServe blocks until the process
// exits.
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
