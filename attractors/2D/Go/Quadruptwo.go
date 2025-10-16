/*
 *  (C) Copyright 2025  Pavel Tisnovsky
 *
 *  All rights reserved. This program and the accompanying materials
 *  are made available under the terms of the Eclipse Public License v1.0
 *  which accompanies this distribution, and is available at
 *  http://www.eclipse.org/legal/epl-v10.html
 *
 *  Contributors:
 *      Pavel Tisnovsky
 */

package main

import (
	"attractors/bitmap"
	"image"
	"math"
)

const ImageWidth = 800
const ImageHeight = 600
const Maxiter = 1000000

func sqr(x float64) float64 {
	return x * x
}

func sign(x float64) float64 {
	if x > 0 {
		return 1
	}
	return -1
}

func quadruptwo(x, y, a, b, c float64) (float64, float64) {
	xn := y - sign(x)*math.Sin(math.Log(math.Abs(b*x-c)))*math.Atan(sqr(math.Log(math.Abs(c*x-b))))
	yn := a - x
	return xn, yn
}

func calcSystem(
	width, height, maxiter int,
	A, B, C, scale, xOffset, yOffset, maxFactor float64) *image.RGBA {

	img := image.NewRGBA(image.Rect(0, 0, width, height))

	bmp := bitmap.CreateBitmap(width, height)
	maxPoints := maxiter
	settleDownPoints := 100

	x := 0.0
	y := 0.0

	for i := range maxPoints {
		xn, yn := quadruptwo(x, y, A, B, C)
		xi := int(float64(width)/2 + scale*xn + xOffset)
		yi := int(float64(height)/2 + scale*yn + yOffset)
		if i > settleDownPoints {
			if xi >= 0 && yi >= 0 && xi < int(width) && yi < int(height) {
				bmp[yi][xi] += 1.0
			}
		}
		x, y = xn, yn
	}

	bitmap.DrawBitmapToImage(bmp, img, maxFactor)
	return img
}

func main() {
	{
		const A = 3.1
		const B = 1.8
		const C = -0.9
		img := calcSystem(ImageWidth, ImageHeight, Maxiter, A, B, C, 9.0, 0, 0, 1/3.0)
		bitmap.SaveImage(img, "quadruptwo.png")
	}
}
