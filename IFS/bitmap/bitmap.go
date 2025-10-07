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

package bitmap

import (
	"image"
	"image/color"
	"image/png"
	"math"
	"os"
)

func computeMinMax(bitmap [][]float64, width, height int) (float64, float64) {
	minValue := math.MaxFloat64
	maxValue := -math.MaxFloat64
	for j := range height {
		for i := range width {
			z := bitmap[j][i]
			if maxValue < z {
				maxValue = z
			}
			if minValue > z {
				minValue = z
			}
		}
	}
	return minValue, maxValue
}

func CreateBitmap(width, height int) [][]float64 {
	result := make([][]float64, height)
	for i := range height {
		result[i] = make([]float64, width)
	}
	return result
}

func DrawBitmapToImage(bitmap [][]float64, image *image.RGBA, maxFactor float64) {
	size := image.Bounds().Size()
	width := size.X
	height := size.Y

	min, max := computeMinMax(bitmap, width, height)
	max *= maxFactor
	k := 255.0 / (max - min)
	for y := range height {
		for x := range width {
			f := bitmap[y][x]
			f -= min
			f *= k
			if f > 255.0 {
				f = 255
			}
			i := uint8(int(f) & 255)
			i = 255 - i
			c := color.RGBA{i, i, i, 255}
			image.SetRGBA(int(x), int(y), c)
		}
	}
}

func SaveImage(img *image.RGBA, filename string) {
	outfile, err := os.Create(filename)
	if err != nil {
		panic(err)
	}
	defer outfile.Close()

	err = png.Encode(outfile, img)
	if err != nil {
		panic(err)
	}
}
