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
	"ifs/bitmap"
	"image"
	"math"
	"math/rand/v2"
)

const ImageWidth = 512
const ImageHeight = 512
const Maxiter = 1000000

func inv_julia(x, y, cx, cy float64) (float64, float64) {
	zx := x - cx
	zy := y - cy
	var zxn, zyn float64

	abs := math.Hypot(zx, zy)

	zxn = math.Sqrt((abs + zx) / 2)
	zyn = math.Sqrt((abs - zx) / 2)

	if zy <= 0 {
		zyn = -zyn
	}
	return zxn, zyn
}

func calcSystem(
	width, height, maxiter int, cx, cy, scale, xOffset, yOffset, maxFactor float64) *image.RGBA {

	img := image.NewRGBA(image.Rect(0, 0, width, height))

	bmp := bitmap.CreateBitmap(width, height)
	maxPoints := maxiter
	settleDownPoints := 100
	maxPointValue := 20.0

	x := 0.5
	y := 0.5

	for i := range maxPoints {
		xn, yn := inv_julia(x, y, cx, cy)
		if rand.IntN(2) == 1 {
			xn = -xn
			yn = -yn
		}
		if i > settleDownPoints {
			xi := int(float64(width)/2 + scale*xn + xOffset)
			yi := int(float64(height)/2 + scale*yn + yOffset)
			if xi >= 0 && yi >= 0 && xi < int(width) && yi < int(height) {
				if bmp[yi][xi] < maxPointValue {
					bmp[yi][xi] += 1.0
				}
			}
			zx := xn
			zy := yn
			for range 40 {
				zx2 := zx * zx
				zy2 := zy * zy
				zxn := zx2 - zy2 + cx
				zyn := 2.0*zx*zy + cy

				xi := int(float64(width)/2 + scale*zx + xOffset)
				yi := int(float64(height)/2 + scale*zy + yOffset)
				if xi >= 0 && yi >= 0 && xi < int(width) && yi < int(height) {
					if bmp[yi][xi] < maxPointValue {
						bmp[yi][xi] += 1.0
					}
				}
				zx, zy = zxn, zyn
			}
		}
		x, y = xn, yn
	}

	bitmap.DrawBitmapToImage(bmp, img, maxFactor)
	return img
}

func main() {
	{
		const Cx = -0.390540870218399
		const Cy = -0.586787907346969
		img := calcSystem(ImageWidth, ImageHeight, Maxiter, Cx, Cy, 180.0, 0.0, 0.0, 1.)
		bitmap.SaveImage(img, "inv_julia_2_1.png")
	}

	{
		const Cx = -0.769824999999999998320
		const Cy = -0.109270000000000000000
		img := calcSystem(ImageWidth, ImageHeight, Maxiter, Cx, Cy, 160.0, 0.0, 0.0, 1.)
		bitmap.SaveImage(img, "inv_julia_2_2.png")
	}
}
