package main

import (
	"image"
	"image/color"
)

type HDRI struct {
	Width      int
	Height     int
	PixelCount int
	Planes     map[string]PixelPlane
}

func newRGBA(img image.Image) HDRI {
	width := img.Bounds().Dx()
	height := img.Bounds().Dy()
	pixelCount := width * height

	hdri := HDRI{
		Width:      width,
		Height:     height,
		PixelCount: pixelCount,
		Planes:     make(map[string]PixelPlane),
	}

	planeNames := []string{"red", "green", "blue", "alpha"}

	for _, planeName := range planeNames {
		hdri.Planes[planeName] = newPixelPlane(pixelCount)
	}

	hdri.fillInRGBAPlanes(img)
	return hdri
}

func (hdri *HDRI) ToImage() image.Image {
	rect := image.Rect(0, 0, hdri.Width, hdri.Height)
	img := image.NewRGBA(rect)

	rp := hdri.Planes["red"].Pixels
	gp := hdri.Planes["green"].Pixels
	bp := hdri.Planes["blue"].Pixels
	ap := hdri.Planes["alpha"].Pixels
	i := 0
	for y := 0; y < img.Bounds().Dy(); y++ {
		for x := 0; x < img.Bounds().Dx(); x++ {
			r := uint8(uint(rp[i]) >> 8)
			g := uint8(uint(gp[i]) >> 8)
			b := uint8(uint(bp[i]) >> 8)
			a := uint8(uint(ap[i]) >> 8)
			i++
			c := color.NRGBA{r, g, b, a}
			img.Set(x, y, c)
		}
	}
	return img
}

func (hdri *HDRI) Multiply(plane string, scale float32) {
	pixels := hdri.Planes[plane].Pixels

	for i := 0; i < hdri.PixelCount; i++ {
		pixels[i] *= scale
	}
}

func (hdri *HDRI) AddRGBA(rdelta, gdelta, bdelta, adelta float32) {
	hdri.Add("red", rdelta)
	hdri.Add("green", gdelta)
	hdri.Add("blue", bdelta)
	hdri.Add("alpha", adelta)
}

func (hdri *HDRI) Add(plane string, delta float32) {
	pixels := hdri.Planes[plane].Pixels

	for i := 0; i < hdri.PixelCount; i++ {
		pixels[i] += delta
	}
}

func (hdri *HDRI) MultiplyRGBA(rscale, gscale, bscale, ascale float32) {
	hdri.Multiply("red", rscale)
	hdri.Multiply("green", gscale)
	hdri.Multiply("blue", bscale)
	hdri.Multiply("alpha", ascale)
}

func (hdri *HDRI) fillInRGBAPlanes(img image.Image) {
	rp := hdri.Planes["red"].Pixels
	gp := hdri.Planes["green"].Pixels
	bp := hdri.Planes["blue"].Pixels
	ap := hdri.Planes["alpha"].Pixels

	i := 0
	for y := 0; y < img.Bounds().Dy(); y++ {
		for x := 0; x < img.Bounds().Dx(); x++ {
			r, g, b, a := img.At(x, y).RGBA()
			rp[i] = float32(r)
			gp[i] = float32(g)
			bp[i] = float32(b)
			ap[i] = float32(a)
			i++
		}
	}
}
