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

func svensson(x, y, a, b, c, d float64) (float64, float64) {
	xn := d*math.Sin(x*a) - math.Sin(y*b)
	yn := c*math.Cos(x*a) + math.Cos(y*b)
	return xn, yn
}

func calcSystem(
	width, height, maxiter int,
	A, B, C, D, scale, xOffset, yOffset, maxFactor float64) *image.RGBA {

	img := image.NewRGBA(image.Rect(0, 0, width, height))

	bmp := bitmap.CreateBitmap(width, height)
	maxPoints := maxiter
	settleDownPoints := 100

	x := 0.1
	y := 0.0

	for i := range maxPoints {
		xn, yn := svensson(x, y, A, B, C, D)
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
	const A = -2.337
	const B = -2.337
	const C = 0.533
	const D = 1.378
	img := calcSystem(ImageWidth, ImageHeight, Maxiter, A, B, C, D, 160.0, 0, 0, 1/15.0)
	bitmap.SaveImage(img, "svensson.png")
}
