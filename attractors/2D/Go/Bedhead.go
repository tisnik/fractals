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

func bedhead(x, y, a, b float64) (float64, float64) {
	xn := math.Sin(x*y/b)*y + math.Cos(a*x-y)
	yn := x + math.Sin(y)/b
	return xn, yn
}

func calcSystem(
	width, height, maxiter int,
	A, B, scale, xOffset, yOffset, maxFactor float64) *image.RGBA {

	img := image.NewRGBA(image.Rect(0, 0, width, height))

	bmp := bitmap.CreateBitmap(width, height)
	maxPoints := maxiter
	settleDownPoints := 100

	x := 0.0
	y := 0.0

	for i := range maxPoints {
		xn, yn := bedhead(x, y, A, B)
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
	img := calcSystem(ImageWidth, ImageHeight, Maxiter, 0.06, 0.98, 80, 50, 10, 1/100.0)
	bitmap.SaveImage(img, "bedhead_1.png")

	img = calcSystem(ImageWidth, ImageHeight, Maxiter, -0.67, 0.83, 220, -100, -350, 1/100.0)
	bitmap.SaveImage(img, "bedhead_2.png")

	img = calcSystem(ImageWidth, ImageHeight, Maxiter, -0.67, 0.68, 70, 0, 50, 1/50.0)
	bitmap.SaveImage(img, "bedhead_3.png")
}
