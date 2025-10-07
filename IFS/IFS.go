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
 *
 */

package main

import (
	"ifs/bitmap"
	"image"
	"math/rand/v2"
)

// IFS systems

const (
	ImageWidth  = 512
	ImageHeight = 512
	Maxiter     = 300000
)

type IfsSystem [][7]float64

func calcSystem(
	width, height, maxiter int, ifs IfsSystem, scale, xOffset, yOffset float64) *image.RGBA {

	img := image.NewRGBA(image.Rect(0, 0, width, height))
	bmp := bitmap.CreateBitmap(width, height)
	maxPoints := maxiter
	settleDownPoints := 10
	maxPointValue := 50.0

	x1 := 1.0
	y1 := 1.0

	for i := range maxPoints {
		pp := rand.Float64()
		sum := 0.0
		j := 0
		for sum <= pp {
			sum += ifs[j][6]
			j++
		}
		j--

		x2 := x1*ifs[j][0] + y1*ifs[j][1] + ifs[j][4]
		y2 := x1*ifs[j][2] + y1*ifs[j][3] + ifs[j][5]
		if i > settleDownPoints {
			xi := int(float64(width)/2 + scale*x2 + xOffset)
			yi := int(float64(height)/2 + scale*y2 + yOffset)
			if xi >= 0 && yi >= 0 && xi < int(width) && yi < int(height) {
				if bmp[yi][xi] < maxPointValue {
					bmp[yi][xi] += 1.0
				}
			}
		}
		x1, y1 = x2, y2
	}
	bitmap.DrawBitmapToImage(bmp, img, 1.0)
	return img
}

func main() {
	IfsSystems := make(map[string]IfsSystem)

	IfsSystems["binary"] = IfsSystem{
		{0.500000, 0.000000, 0.000000, 0.500000, -2.563477, -0.000003, 0.333333},
		{0.500000, 0.000000, 0.000000, 0.500000, 2.436544, -0.000003, 0.333333},
		{0.000000, -0.500000, 0.500000, 0.000000, 4.873085, 7.563492, 0.333334},
	}

	IfsSystems["coral"] = IfsSystem{
		{0.307692, -0.531469, -0.461538, -0.293706, 5.401953, 8.655175, 0.400000},
		{0.307692, -0.076923, 0.153846, -0.447552, -1.295248, 4.152990, 0.150000},
		{0.000000, 0.545455, 0.692308, -0.195804, -4.893637, 7.269794, 0.450000},
	}

	IfsSystems["dragon"] = IfsSystem{
		{0.824074, 0.281482, -0.212346, 0.864198, -1.882290, -0.110607, 0.787473},
		{0.088272, 0.520988, -0.463889, -0.377778, 0.785360, 8.095795, 0.212527},
	}

	IfsSystems["dragon2"] = IfsSystem{
		{0.824074, 0.281481, -0.212346, 0.864197, -1.772710, 0.137795, 0.771268},
		{-0.138580, 0.283951, -0.670062, -0.279012, 2.930991, 7.338924, 0.228732},
	}

	IfsSystems["feather"] = IfsSystem{
		{0.870370, 0.074074, -0.115741, 0.851852, -1.278016, 0.070331, 0.798030},
		{-0.162037, -0.407407, 0.495370, 0.074074, 6.835726, 5.799174, 0.201970},
	}

	IfsSystems["fern"] = IfsSystem{
		{0.850000, 0.040000, -0.040000, 0.850000, 0.000000, 1.600000, 0.850000},
		{0.200000, -0.260000, 0.230000, 0.220000, 0.000000, 1.600000, 0.070000},
		{-0.150000, 0.280000, 0.260000, 0.240000, 0.000000, 0.440000, 0.070000},
		{0.000000, 0.000000, 0.000000, 0.160000, 0.000000, 0.000000, 0.010000},
	}

	IfsSystems["koch"] = IfsSystem{
		{0.307692, 0.000000, 0.000000, 0.294118, 4.119164, 1.604278, 0.151515},
		{0.192308, -0.205882, 0.653846, 0.088235, -0.688840, 5.978916, 0.253788},
		{0.192308, 0.205882, -0.653846, 0.088235, 0.668580, 5.962514, 0.253788},
		{0.307692, 0.000000, 0.000000, 0.294118, -4.136530, 1.604278, 0.151515},
		{0.384615, 0.000000, 0.000000, -0.294118, -0.007718, 2.941176, 1.000000},
	}

	IfsSystems["spiral"] = IfsSystem{
		{0.787879, -0.424242, 0.242424, 0.859848, 1.758647, 1.408065, 0.895652},
		{-0.121212, 0.257576, 0.151515, 0.053030, -6.721654, 1.377236, 0.052174},
		{0.181818, -0.136364, 0.090909, 0.181818, 6.086107, 1.568035, 0.052174},
	}

	IfsSystems["tree"] = IfsSystem{
		{0.000000, 0.000000, 0.000000, 0.500000, 0.000000, 0.000000, 0.050000},
		{0.420000, -0.420000, 0.420000, 0.420000, 0.000000, 0.200000, 0.400000},
		{0.420000, 0.420000, -0.420000, 0.420000, 0.000000, 0.200000, 0.400000},
		{0.100000, 0.000000, 0.000000, 0.100000, 0.000000, 0.200000, 0.150000},
	}

	IfsSystems["triangle"] = IfsSystem{
		{0.500000, 0.000000, 0.000000, 0.500000, -0.500000, 0.000000, 0.333333},
		{0.500000, 0.000000, 0.000000, 0.500000, 0.500000, 0.000000, 0.333333},
		{0.500000, 0.000000, 0.000000, 0.500000, 0.000000, 0.860000, 0.333334},
	}

	img := calcSystem(ImageWidth, ImageHeight, Maxiter, IfsSystems["spiral"], 30.0, 0.0, -150.0)
	bitmap.SaveImage(img, "ifs_spiral.png")

	img = calcSystem(ImageWidth, ImageHeight, Maxiter, IfsSystems["dragon"], 30.0, 0.0, -150.0)
	bitmap.SaveImage(img, "ifs_dragon.png")
}
