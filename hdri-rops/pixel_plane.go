package main

type PixelPlane struct {
	Pixels []float32
}

func newPixelPlane(pixelCount int) PixelPlane {
	pp := PixelPlane{
		Pixels: make([]float32, pixelCount, pixelCount),
	}
	return pp
}
