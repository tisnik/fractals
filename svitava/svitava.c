/*

   (C) Copyright 2024, 2025  Pavel Tisnovsky

   All rights reserved. This program and the accompanying materials
   are made available under the terms of the Eclipse Public License v1.0
   which accompanies this distribution, and is available at
   http://www.eclipse.org/legal/epl-v10.html

   Contributors:
       Pavel Tisnovsky

*/

/*
build as shared library: gcc -shared -Wl,-soname,testlib -o testlib.so -fPIC
testlib.c build as executable:
*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define NULL_CHECK(value)  if (value == NULL) {puts("NULL parameter"); return;}

/**
 * Writes an RGB color from the palette at the specified index into the pixel
 * buffer and advances the pixel pointer by 4 bytes.
 */
void putpixel(unsigned char **pixel, const unsigned char *palette,
              int color_index) {
    int color_offset = color_index * 3;
    unsigned char *pal = (unsigned char *)(palette + color_offset);

    *(*pixel)++ = *pal++;
    *(*pixel)++ = *pal++;
    *(*pixel)++ = *pal;
    (*pixel)++;
}

/**
 * Fills the pixel buffer with a test RGB image where the red channel is set to
 * the x-coordinate, the green channel is set to a fixed value, and the blue
 * channel is set to the y-coordinate.
 *
 * The pixel buffer is assumed to use 4 bytes per pixel, with the fourth byte
 * unused or as padding.
 * @param green Value to assign to the green channel for all pixels.
 */
void render_test_rgb_image(unsigned int width, unsigned int height,
                           unsigned char *pixels, unsigned char green) {
    unsigned int i, j;
    unsigned char *p = pixels;

    for (j = 0; j < height; j++) {
        for (i = 0; i < width; i++) {
            *p++ = i;
            *p++ = green;
            *p++ = j;
            p++;
        }
    }
}

/**
 * Fills the pixel buffer with a test image using colors from the palette
 * indexed by the x-coordinate.
 *
 * Each pixel in the image is assigned a color from the palette based on its
 * horizontal position, creating vertical color bands.
 */
void render_test_palette_image(unsigned int width, unsigned int height,
                               const unsigned char *palette,
                               unsigned char *pixels) {
    unsigned int i, j;
    unsigned char *p = pixels;

    for (j = 0; j < height; j++) {
        for (i = 0; i < width; i++) {
            int color = i;
            putpixel(&p, palette, color);
        }
    }
}

/**
 * Renders the Mandelbrot set fractal into a pixel buffer using a specified
 * color palette.
 *
 * Iterates over each pixel, maps it to a point in the complex plane, and
 * computes the escape time for the Mandelbrot set. The iteration count
 * determines the color index used from the palette.
 */
void render_mandelbrot(unsigned int width, unsigned int height,
                       const unsigned char *palette, unsigned char *pixels,
                       int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -2.0, ymin = -1.5, xmax = 1.0, ymax = 1.5;
    unsigned char *p = pixels;

    NULL_CHECK(palette)
    NULL_CHECK(pixels)

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + cy;
                zx = zx2 - zy2 + cx;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders a Julia set fractal image into the provided pixel buffer.
 *
 * Maps each pixel to a point in the complex plane and iterates the function z =
 * z^2 + c, where c is specified by `cx` and `cy`. Colors are assigned based on
 * the number of iterations before escape, using the provided palette.
 */
void render_julia(unsigned int width, unsigned int height,
                  const unsigned char *palette, unsigned char *pixels,
                  double cx, double cy, int maxiter) {
    int x, y;
    double zx0, zy0;
    double xmin = -1.5, ymin = -1.5, xmax = 1.5, ymax = 1.5;
    unsigned char *p = pixels;

#ifdef DEBUG
    printf("%f %f\n", cx, cy);
#endif

    zy0 = ymin;
    for (y = 0; y < height; y++) {
        zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + cy;
                zx = zx2 - zy2 + cx;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders a cubic Mandelbrot fractal (z = z³ + c) into the pixel buffer.
 *
 * Each pixel is mapped to a point in the complex plane, and the cubic
 * Mandelbrot iteration is performed up to `maxiter` times. The number of
 * iterations before escape determines the color index from the palette.
 */
void render_mandelbrot_3(unsigned int width, unsigned int height,
                         const unsigned char *palette, unsigned char *pixels,
                         int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -1.5, ymin = -1.5, xmax = 1.5, ymax = 1.5;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zx3 = zx2 * zx;
                double zy3 = zy2 * zy;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zxn = zx3 - 3.0 * zx * zy2 + cx;
                zyn = -zy3 + 3.0 * zx2 * zy + cy;
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders a cubic Julia set fractal image using the formula z = z³ + c.
 *
 * Each pixel is mapped to a point in the complex plane, and the cubic Julia
 * iteration is performed up to `maxiter` times or until the escape radius is
 * exceeded. The number of iterations before escape determines the color, which
 * is selected from the palette.
 *
 * @param cx Real part of the constant complex parameter c.
 * @param cy Imaginary part of the constant complex parameter c.
 * @param maxiter Maximum number of iterations for the escape test.
 */
void render_julia_3(unsigned int width, unsigned int height,
                    const unsigned char *palette, unsigned char *pixels,
                    double cx, double cy, int maxiter) {
    int x, y;
    double zx0, zy0;
    double xmin = -1.5, ymin = -1.5, xmax = 1.5, ymax = 1.5;
    unsigned char *p = pixels;

#ifdef DEBUG
    printf("%f %f\n", cx, cy);
#endif

    zy0 = ymin;
    for (y = 0; y < height; y++) {
        zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zx3 = zx2 * zx;
                double zy3 = zy2 * zy;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zxn = zx3 - 3.0 * zx * zy2 + cx;
                zyn = -zy3 + 3.0 * zx2 * zy + cy;
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders a quartic Mandelbrot set fractal image into a pixel buffer.
 *
 * Iterates the function z = z⁴ + c for each pixel mapped to the complex plane,
 * coloring pixels based on the number of iterations before escape, using the
 * provided palette. The fractal is rendered over the region [-1.5, 1.5] x
 * [-1.5, 1.5] in the complex plane.
 *
 * @param width Image width in pixels.
 * @param height Image height in pixels.
 * @param palette Pointer to the color palette (array of RGB triplets).
 * @param pixels Output pixel buffer (4 bytes per pixel, RGB in first 3 bytes).
 * @param maxiter Maximum number of iterations for the escape algorithm.
 */
void render_mandelbrot_4(unsigned int width, unsigned int height,
                         const unsigned char *palette, unsigned char *pixels,
                         int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -1.5, ymin = -1.5, xmax = 1.5, ymax = 1.5;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zx4, zy4;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zxn = zx2 - zy2;
                zyn = 2.0 * zx * zy;
                zx4 = zxn * zxn;
                zy4 = zyn * zyn;
                zy = 2.0 * zxn * zyn + cy;
                zx = zx4 - zy4 + cx;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders a quartic Julia set fractal image using the formula z = z⁴ + c.
 *
 * Iterates the quartic Julia set for each pixel, mapping image coordinates to
 * the complex plane in the range [-1.5, 1.5] for both axes. The constant
 * complex parameter c is specified by `cx` and `cy`. Each pixel is colored
 * based on the number of iterations before escape, using the provided palette.
 *
 * @param cx Real part of the constant parameter c for the Julia set.
 * @param cy Imaginary part of the constant parameter c for the Julia set.
 * @param maxiter Maximum number of iterations for the escape condition.
 */
void render_julia_4(unsigned int width, unsigned int height,
                    const unsigned char *palette, unsigned char *pixels,
                    double cx, double cy, int maxiter) {
    int x, y;
    double zx0, zy0;
    double xmin = -1.5, ymin = -1.5, xmax = 1.5, ymax = 1.5;
    unsigned char *p = pixels;

#ifdef DEBUG
    printf("%f %f\n", cx, cy);
#endif

    zy0 = ymin;
    for (y = 0; y < height; y++) {
        zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zx4, zy4;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zxn = zx2 - zy2;
                zyn = 2.0 * zx * zy;
                zx4 = zxn * zxn;
                zy4 = zyn * zyn;
                zy = 2.0 * zxn * zyn + cy;
                zx = zx4 - zy4 + cx;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders the Barnsley Mandelbrot-type fractal (variant 1) into a pixel buffer.
 *
 * Iterates a piecewise complex function for each pixel mapped to the complex
 * plane, coloring pixels based on the number of iterations before escape or
 * reaching `maxiter`. The function uses a conditional transformation depending
 * on the sign of the real part of z.
 */
void render_barnsley_m1(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                if (zx >= 0) {
                    zxn = zx * cx - zy * cy - cx;
                    zyn = zx * cy + zy * cx - cy;
                } else {
                    zxn = zx * cx - zy * cy + cx;
                    zyn = zx * cy + zy * cx + cy;
                }
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders a Barnsley Julia fractal image using a piecewise complex function.
 *
 * Maps each pixel to a point in the complex plane and iterates a piecewise
 * function based on the sign of the real part, using parameters `cx` and `cy`.
 * Colors are assigned from the palette based on the number of iterations before
 * escape or reaching `maxiter`.
 */
void render_barnsley_j1(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        double cx, double cy, int maxiter) {
    int x, y;
    double zx0, zy0;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    zy0 = ymin;
    for (y = 0; y < height; y++) {
        zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                if (zx >= 0) {
                    zxn = zx * cx - zy * cy - cx;
                    zyn = zx * cy + zy * cx - cy;
                } else {
                    zxn = zx * cx - zy * cy + cx;
                    zyn = zx * cy + zy * cx + cy;
                }
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders a Barnsley fractal (variant m2) to a pixel buffer using a piecewise
 * complex function.
 *
 * The fractal is generated by iterating a piecewise function on the complex
 * plane for each pixel, with the function branch determined by the sign of (zx
 * * cy + zy * cx). The number of iterations before escape (or reaching maxiter)
 * determines the color index for each pixel.
 *
 * @param width Width of the output image in pixels.
 * @param height Height of the output image in pixels.
 * @param palette Pointer to the color palette used for mapping iteration counts
 * to RGB values.
 * @param pixels Pointer to the pixel buffer to be filled (assumes 4 bytes per
 * pixel).
 * @param maxiter Maximum number of iterations for the fractal calculation.
 */
void render_barnsley_m2(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                if (zx * cy + zy * cx >= 0) {
                    zxn = zx * cx - zy * cy - cx;
                    zyn = zx * cy + zy * cx - cy;
                } else {
                    zxn = zx * cx - zy * cy + cx;
                    zyn = zx * cy + zy * cx + cy;
                }
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders a Barnsley Julia set fractal variant using a piecewise complex
 * function.
 *
 * For each pixel, maps its coordinates to the complex plane and iterates a
 * piecewise function based on the sign of a linear combination of zx and zy,
 * with parameters cx and cy. Colors are assigned from the palette based on the
 * number of iterations before escape or reaching maxiter.
 */
void render_barnsley_j2(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        double cx, double cy, int maxiter) {
    int x, y;
    double zx0, zy0;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    zy0 = ymin;
    for (y = 0; y < height; y++) {
        zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                if (zx * cy + zy * cx >= 0) {
                    zxn = zx * cx - zy * cy - cx;
                    zyn = zx * cy + zy * cx - cy;
                } else {
                    zxn = zx * cx - zy * cy + cx;
                    zyn = zx * cy + zy * cx + cy;
                }
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders the Barnsley M3 fractal set into a pixel buffer using a palette.
 *
 * Iterates a piecewise quadratic function over the complex plane for each
 * pixel, with the function's behavior depending on the sign of the real part of
 * z. Colors are assigned based on the number of iterations before escape, up to
 * `maxiter`.
 */
void render_barnsley_m3(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                if (zx > 0) {
                    zxn = zx2 - zy2 - 1;
                    zyn = 2.0 * zx * zy;
                } else {
                    zxn = zx2 - zy2 - 1 + cx * zx;
                    zyn = 2.0 * zx * zy + cy * zx;
                }
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders a Barnsley Julia-type fractal variant using a piecewise quadratic
 * iteration.
 *
 * For each pixel, maps coordinates to the complex plane and iterates a
 * piecewise function:
 * - If the real part is positive, applies z = z^2 - 1.
 * - If the real part is non-positive, applies z = z^2 - 1 + c*z, where c = cx +
 * i*cy. Iteration stops when the magnitude squared exceeds 4 or the maximum
 * number of iterations is reached. The number of iterations determines the
 * color index for each pixel.
 *
 * @param width Image width in pixels.
 * @param height Image height in pixels.
 * @param palette Pointer to the color palette (array of RGB triples).
 * @param pixels Output pixel buffer (4 bytes per pixel, RGB in first 3 bytes).
 * @param cx Real part of the Julia parameter c.
 * @param cy Imaginary part of the Julia parameter c.
 * @param maxiter Maximum number of iterations per pixel.
 */
void render_barnsley_j3(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        double cx, double cy, int maxiter) {
    int x, y;
    double zx0, zy0;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    zy0 = ymin;
    for (y = 0; y < height; y++) {
        zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn, zyn;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                if (zx > 0) {
                    zxn = zx2 - zy2 - 1;
                    zyn = 2.0 * zx * zy;
                } else {
                    zxn = zx2 - zy2 - 1 + cx * zx;
                    zyn = 2.0 * zx * zy + cy * zx;
                }
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders a "magnet" type 1 Mandelbrot fractal into the pixel buffer.
 *
 * Iterates a rational function over the complex plane for each pixel, mapping
 * escape or convergence behavior to color indices from the palette. The fractal
 * is rendered over the region [-2, 2] x [-2, 2] with up to `maxiter` iterations
 * per pixel.
 */
void render_magnet_m1(unsigned int width, unsigned int height,
                      const unsigned char *palette, unsigned char *pixels,
                      int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2, zy2, zxn, zyn, tzx, tzy, bzx, bzy, div;
                zx2 = zx * zx;
                zy2 = zy * zy;
                if (zx2 + zy2 > 100)
                    break;
                if (((zx - 1.0) * (zx - 1.0) + zy * zy) < 0.001)
                    break;
                tzx = zx2 - zy2 + cx - 1;
                tzy = 2.0 * zx * zy + cy;
                bzx = 2.0 * zx + cx - 2;
                bzy = 2.0 * zy + cy;
                div = bzx * bzx + bzy * bzy;
#define MIN_VALUE 1.0 - 100
                if (div < MIN_VALUE)
                    break;
                zxn = (tzx * bzx + tzy * bzy) / div;
                zyn = (tzy * bzx - tzx * bzy) / div;
                zx = (zxn + zyn) * (zxn - zyn);
                zy = 2.0 * zxn * zyn;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders a "magnet" type Julia fractal image using a rational function
 * iteration.
 *
 * The fractal is generated by iterating a complex rational function for each
 * pixel, using the provided Julia parameters (`cx`, `cy`). The number of
 * iterations before escape or convergence determines the color, which is
 * selected from the palette and written to the pixel buffer.
 *
 * @param width Width of the output image in pixels.
 * @param height Height of the output image in pixels.
 * @param palette Pointer to the color palette (array of RGB triplets).
 * @param pixels Pointer to the output pixel buffer (4 bytes per pixel).
 * @param cx Real part of the Julia set parameter.
 * @param cy Imaginary part of the Julia set parameter.
 * @param maxiter Maximum number of iterations per pixel.
 */
void render_magnet_j1(unsigned int width, unsigned int height,
                      const unsigned char *palette, unsigned char *pixels,
                      double cx, double cy, int maxiter) {
    int x, y;
    double zx0, zy0;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    zy0 = ymin;
    for (y = 0; y < height; y++) {
        zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;
            unsigned int i = 0;
            while (i < maxiter) {
                double zx2, zy2, zxn, zyn, tzx, tzy, bzx, bzy, div;
                zx2 = zx * zx;
                zy2 = zy * zy;
                if (zx2 + zy2 > 100)
                    break;
                if (((zx - 1.0) * (zx - 1.0) + zy * zy) < 0.001)
                    break;
                tzx = zx2 - zy2 + cx - 1;
                tzy = 2.0 * zx * zy + cy;
                bzx = 2.0 * zx + cx - 2;
                bzy = 2.0 * zy + cy;
                div = bzx * bzx + bzy * bzy;
#define MIN_VALUE 1.0 - 100
                if (div < MIN_VALUE)
                    break;
                zxn = (tzx * bzx + tzy * bzy) / div;
                zyn = (tzy * bzx - tzx * bzy) / div;
                zx = (zxn + zyn) * (zxn - zyn);
                zy = 2.0 * zxn * zyn;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders the Magnet type 2 fractal (Mandelbrot variant) into a pixel buffer
 * using a given color palette.
 *
 * Iterates a complex rational function for each pixel mapped to the complex
 * plane, coloring pixels based on the number of iterations before escape or
 * convergence, up to `maxiter`.
 */
void render_magnet_m2(unsigned int width, unsigned int height,
                      const unsigned char *palette, unsigned char *pixels,
                      int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -1.5, ymin = -2.0, xmax = 2.5, ymax = 2.0;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            double cm1x = cx - 1.0;
            double cm1y = cy;
            double cm2x = cx - 2.0;
            double cm2y = cy;
            double cm1cm2x = cm1x * cm2x - cm1y * cm2y;
            double cm1cm2y = cm1x * cm2y + cm1y * cm2x;
            unsigned int i = 0;

            cm1x += cm1x + cm1x;
            cm1y += cm1y + cm1y;
            cm2x += cm2x + cm2x;
            cm2y += cm2y + cm2y;

            while (i < maxiter) {
                double zx2, zy2, zxn, zyn, tzx, tzy, bzx, bzy, div;
                zx2 = zx * zx;
                zy2 = zy * zy;
                tzx = zx * (zx2 - 3.0 * zy2 + cm1x) - zy * cm1y + cm1cm2x;
                tzy = zy * (3.0 * zx2 - zy2 + cm1x) + zx * cm1y + cm1cm2y;
                bzx = zx2 - zy2;
                bzx = 3.0 * bzx + zx * cm2x - zy * cm2y + cm1cm2x + 1.0;
                bzy = 2.0 * zx * zy;
                bzy = 3.0 * bzy + zx * cm2y + zy * cm2x + cm1cm2y;
                div = bzx * bzx + bzy * bzy;
#define MIN_VALUE 1.0 - 100
                if (div < MIN_VALUE)
                    break;
                zxn = (tzx * bzx + tzy * bzy) / div;
                zyn = (tzy * bzx - tzx * bzy) / div;
                zx = (zxn + zyn) * (zxn - zyn);
                zy = 2.0 * zxn * zyn;
                if (zx2 + zy2 > 100 * 100)
                    break;
                if (((zx - 1.0) * (zx - 1.0) + zy * zy) < 0.001)
                    break;
                if (zx2 + zy2 > 100)
                    break;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders the Magnet type 2 Julia fractal set into a pixel buffer using the
 * specified complex parameter.
 *
 * Each pixel is mapped to a point in the complex plane and iterated using a
 * rational function involving the parameter (cx, cy). The number of iterations
 * before escape or convergence determines the color index from the palette.
 *
 * @param width Width of the image in pixels.
 * @param height Height of the image in pixels.
 * @param palette Pointer to the color palette (array of RGB triplets).
 * @param pixels Output pixel buffer (4 bytes per pixel).
 * @param cx Real part of the Julia set parameter.
 * @param cy Imaginary part of the Julia set parameter.
 * @param maxiter Maximum number of iterations per pixel.
 */
void render_magnet_j2(unsigned int width, unsigned int height,
                      const unsigned char *palette, unsigned char *pixels,
                      double cx, double cy, int maxiter) {
    int x, y;
    double cx0, cy0;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    cy0 = ymin;
    for (y = 0; y < height; y++) {
        cx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = cx0;
            double zy = cy0;
            double cm1x = cx - 1.0;
            double cm1y = cy;
            double cm2x = cx - 2.0;
            double cm2y = cy;
            double cm1cm2x = cm1x * cm2x - cm1y * cm2y;
            double cm1cm2y = cm1x * cm2y + cm1y * cm2x;
            unsigned int i = 0;

            cm1x += cm1x + cm1x;
            cm1y += cm1y + cm1y;
            cm2x += cm2x + cm2x;
            cm2y += cm2y + cm2y;

            while (i < maxiter) {
                double zx2, zy2, zxn, zyn, tzx, tzy, bzx, bzy, div;
                zx2 = zx * zx;
                zy2 = zy * zy;
                tzx = zx * (zx2 - 3.0 * zy2 + cm1x) - zy * cm1y + cm1cm2x;
                tzy = zy * (3.0 * zx2 - zy2 + cm1x) + zx * cm1y + cm1cm2y;
                bzx = zx2 - zy2;
                bzx = 3.0 * bzx + zx * cm2x - zy * cm2y + cm1cm2x + 1.0;
                bzy = 2.0 * zx * zy;
                bzy = 3.0 * bzy + zx * cm2y + zy * cm2x + cm1cm2y;
                div = bzx * bzx + bzy * bzy;
#define MIN_VALUE 1.0 - 100
                if (div < MIN_VALUE)
                    break;
                zxn = (tzx * bzx + tzy * bzy) / div;
                zyn = (tzy * bzx - tzx * bzy) / div;
                zx = (zxn + zyn) * (zxn - zyn);
                zy = 2.0 * zxn * zyn;
                if (zx2 + zy2 > 100 * 100)
                    break;
                if (((zx - 1.0) * (zx - 1.0) + zy * zy) < 0.001)
                    break;
                if (zx2 + zy2 > 100)
                    break;
                i++;
            }
            putpixel(&p, palette, i);
            cx0 += (xmax - xmin) / width;
        }
        cy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders a Phoenix Mandelbrot fractal image into a pixel buffer.
 *
 * Iterates the Phoenix fractal formula over each pixel, mapping pixel
 * coordinates to the complex plane and using the number of iterations before
 * escape to select a color from the palette. The resulting image is written to
 * the provided pixel buffer.
 */
void render_phoenix_m(unsigned int width, unsigned int height,
                      const unsigned char *palette, unsigned char *pixels,
                      int maxiter) {
    int x, y;
    double cx, cy;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = cx;
            double zy = cy;
            double ynx = 0.0;
            double yny = 0.0;

            unsigned int i = 0;

            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn = zx2 - zy2 + cx + cy * ynx;
                double zyn = 2.0 * zx * zy + cy * yny;
                if (zx2 + zy2 > 4) {
                    break;
                }
                ynx = zx;
                yny = zy;
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

/**
 * Renders a Phoenix Julia fractal image into a pixel buffer using the specified
 * palette and Julia parameters.
 *
 * The function maps each pixel to a point in the complex plane and iterates the
 * Phoenix Julia set formula, using `cx` and `cy` as parameters. The number of
 * iterations before escape determines the color index for each pixel.
 *
 * @param width Width of the output image in pixels.
 * @param height Height of the output image in pixels.
 * @param palette Pointer to the color palette (array of RGB triplets).
 * @param pixels Pointer to the output pixel buffer (4 bytes per pixel).
 * @param cx Real part of the Julia parameter.
 * @param cy Imaginary part of the Julia parameter and Phoenix coupling
 * parameter.
 * @param maxiter Maximum number of iterations for the fractal calculation.
 */
void render_phoenix_j(unsigned int width, unsigned int height,
                      const unsigned char *palette, unsigned char *pixels,
                      double cx, double cy, int maxiter) {
    int x, y;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

    double zy0 = ymin;

    for (y = 0; y < height; y++) {
        double zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;
            double ynx = 0.0;
            double yny = 0.0;

            unsigned int i = 0;

            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn = zx2 - zy2 + cx + cy * ynx;
                double zyn = 2.0 * zx * zy + cy * yny;
                if (zx2 + zy2 > 4) {
                    break;
                }
                ynx = zx;
                yny = zy;
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders a Newton fractal for the roots of unity over the complex plane and
 * writes the result to a pixel buffer.
 *
 * Each pixel is mapped to a point in the complex plane and iteratively updated
 * using Newton's method for the equation z³ = 1. The pixel color is determined
 * by the number of iterations required to converge to one of the three roots,
 * using the provided palette.
 */
void render_newton_m(unsigned int width, unsigned int height,
                     const unsigned char *palette, unsigned char *pixels,
                     int maxiter) {
    int x, y;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

#define PI 3.1415927
#define EPSILON 0.1
#define DIST2(x1, y1, x2, y2)                                                  \
    (((x1) - (x2)) * ((x1) - (x2)) + ((y1) - (y2)) * ((y1) - (y2)))

    double rootx[3];
    double rooty[3];

    double zy0 = ymin;

    rootx[0] = 1.0;
    rootx[1] = cos(2.0 * PI / 3.0);
    rootx[2] = cos(4.0 * PI / 3.0);
    rooty[0] = 0.0;
    rooty[1] = sin(2.0 * PI / 3.0);
    rooty[2] = sin(4.0 * PI / 3.0);

    for (y = 0; y < height; y++) {
        double zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;

            unsigned int i = 0;

            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn =
                    2.0 / 3.0 * zx +
                    (zx2 - zy2) /
                        (3.0 * (zx2 * zx2 + zy2 * zy2 + 2.0 * zx2 * zy2));
                double zyn =
                    2.0 / 3.0 * zy -
                    2.0 * zx * zy /
                        (3.0 * (zx2 * zx2 + zy2 * zy2 + 2.0 * zx2 * zy2));
                if (DIST2(zxn, zyn, rootx[0], rooty[0]) < EPSILON ||
                    DIST2(zxn, zyn, rootx[1], rooty[1]) < EPSILON ||
                    DIST2(zxn, zyn, rootx[2], rooty[2]) < EPSILON)
                    break;
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders a Newton fractal for a cubic polynomial with one user-specified root
 * and two fixed roots, coloring pixels by convergence.
 *
 * The function maps each pixel to a point in the complex plane and applies
 * Newton's method to find roots of a cubic polynomial. The roots are at (cx,
 * cy) and two fixed points on the unit circle. Iteration stops when the current
 * value is sufficiently close to any root or when the maximum number of
 * iterations is reached. The number of iterations determines the color assigned
 * from the palette.
 *
 * @param cx Real part of the user-specified root.
 * @param cy Imaginary part of the user-specified root.
 * @param maxiter Maximum number of Newton iterations per pixel.
 */
void render_newton_j(unsigned int width, unsigned int height,
                     const unsigned char *palette, unsigned char *pixels,
                     double cx, double cy, int maxiter) {
    int x, y;
    double xmin = -2.0, ymin = -2.0, xmax = 2.0, ymax = 2.0;
    unsigned char *p = pixels;

#define PI 3.1415927
#define EPSILON 0.1
#define DIST2(x1, y1, x2, y2)                                                  \
    (((x1) - (x2)) * ((x1) - (x2)) + ((y1) - (y2)) * ((y1) - (y2)))

    double rootx[3];
    double rooty[3];

    double zy0 = ymin;

    rootx[0] = cx;
    rootx[1] = cos(2.0 * PI / 3.0);
    rootx[2] = cos(4.0 * PI / 3.0);
    rooty[0] = cy;
    rooty[1] = sin(2.0 * PI / 3.0);
    rooty[2] = sin(4.0 * PI / 3.0);

    for (y = 0; y < height; y++) {
        double zx0 = xmin;
        for (x = 0; x < width; x++) {
            double zx = zx0;
            double zy = zy0;

            unsigned int i = 0;

            while (i < maxiter) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                double zxn =
                    2.0 / 3.0 * zx +
                    (zx2 - zy2) /
                        (3.0 * (zx2 * zx2 + zy2 * zy2 + 2.0 * zx2 * zy2));
                double zyn =
                    2.0 / 3.0 * zy -
                    2.0 * zx * zy /
                        (3.0 * (zx2 * zx2 + zy2 * zy2 + 2.0 * zx2 * zy2));
                if (DIST2(zxn, zyn, rootx[0], rooty[0]) < EPSILON ||
                    DIST2(zxn, zyn, rootx[1], rooty[1]) < EPSILON ||
                    DIST2(zxn, zyn, rootx[2], rooty[2]) < EPSILON)
                    break;
                zx = zxn;
                zy = zyn;
                i++;
            }
            putpixel(&p, palette, i);
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

/**
 * Renders a synthetic Mandelbrot-like pattern using frequency-modulated sine
 * functions and writes the result to the pixel buffer.
 *
 * The generated image displays smooth, wave-like color variations based on the
 * pixel's mapped coordinates, producing a non-fractal but visually complex
 * pattern. Colors are selected from the palette using the computed value.
 */
void render_fm_synth_mandelbrot(unsigned int width, unsigned int height,
                                const unsigned char *palette,
                                unsigned char *pixels, int maxiter) {
#define LIMIT 100
    double xmin = -LIMIT, ymin = -LIMIT, xmax = LIMIT, ymax = LIMIT;
    double stepx = (xmax - xmin) / (double)width;
    double stepy = (ymax - ymin) / (double)height;

    double y1 = ymin;
    unsigned char *p = pixels;

    int x, y;

    for (y = 0; y < height; y++) {
        double x1 = xmin;
        for (x = 0; x < width; x++) {
            double val = 100.0 + 100.0 * sin(x1 / 4.0 +
                                             2.0 * sin(x1 / 15.0 + y1 / 40.0));
            int i = (int)val & 255;
            putpixel(&p, palette, i);
            x1 += stepx;
        }
        y1 += stepy;
    }
}

/**
 * Renders a synthetic Julia-like pattern using frequency-modulated sine
 * functions and writes the result to the pixel buffer.
 *
 * The color of each pixel is determined by a combination of its mapped
 * coordinates and the parameters `cx` and `cy`, producing smooth, wave-like
 * color variations. The palette is used to map computed values to RGB colors.
 */
void render_fm_synth_julia(unsigned int width, unsigned int height,
                           const unsigned char *palette, unsigned char *pixels,
                           double cx, double cy, int maxiter) {
#define LIMIT 100
    double xmin = -LIMIT, ymin = -LIMIT, xmax = LIMIT, ymax = LIMIT;
    double stepx = (xmax - xmin) / (double)width;
    double stepy = (ymax - ymin) / (double)height;

    double y1 = ymin;
    unsigned char *p = pixels;

    int x, y;

    for (y = 0; y < height; y++) {
        double x1 = xmin;
        for (x = 0; x < width; x++) {
            double val =
                100.0 + 100.0 * sin(x1 / 4.0 +
                                    2.0 * sin(cx * x1 / 15.0 + cy * y1 / 40.0));
            int i = (int)val & 255;
            putpixel(&p, palette, i);
            x1 += stepx;
        }
        y1 += stepy;
    }
}

/**
 * Renders a concentric circle pattern by coloring each pixel based on the
 * squared distance from the image center modulo 256.
 *
 * The color index for each pixel is determined by (x^2 + y^2) % 256, producing
 * repeating circular bands using the provided palette.
 */
void render_circle_pattern(unsigned int width, unsigned int height,
                           const unsigned char *palette, unsigned char *pixels,
                           int maxiter) {
    unsigned char *p = pixels;

    double xmin = -150;
    double ymin = -150;
    double xmax = 150;
    double ymax = 150;

    int i, j;
    double x1, y1;

    y1 = ymin;
    for (j = 0; j < height; j++) {
        x1 = xmin;
        for (i = 0; i < width; i++) {
            double x2 = x1 * x1;
            double y2 = y1 * y1;
            int i = (int)(x2 + y2) % 256;
            putpixel(&p, palette, i);
            x1 += (xmax - xmin) / width;
        }
        y1 += (ymax - ymin) / height;
    }
}

/**
 * Writes pixel data to a file stream in ASCII PPM (P3) format.
 *
 * The output image is written from bottom to top, with each pixel's RGB values
 * output as text. Assumes the pixel buffer uses 4 bytes per pixel, with the
 * fourth byte ignored.
 */
void ppm_write_ascii_to_stream(unsigned int width, unsigned int height,
                               unsigned char *pixels, FILE *fout) {
    int x, y;
    unsigned char r, g, b;
    unsigned char *p = pixels;

    /* header */
    fprintf(fout, "P3 %d %d 255\n", width, height);

    /* pixel array */
    for (y = height - 1; y >= 0; y--) {
        for (x = 0; x < width; x++) {
            r = *p++;
            g = *p++;
            b = *p++;
            p++;
            fprintf(fout, "%d %d %d\n", r, g, b);
        }
    }
}

/**
 * Writes pixel data to a file in ASCII PPM (P3) format.
 *
 * @param width Image width in pixels.
 * @param height Image height in pixels.
 * @param pixels Pointer to the pixel buffer (assumed 4 bytes per pixel, RGB in
 * first 3 bytes).
 * @param file_name Name of the output file.
 * @return 0 on success, -1 on failure to open or close the file.
 */
int ppm_write_ascii(unsigned int width, unsigned int height,
                    unsigned char *pixels, const char *file_name) {
    FILE *fout;

    fout = fopen(file_name, "wb");
    if (!fout) {
        return -1;
    }

    ppm_write_ascii_to_stream(width, height, pixels, fout);

    if (fclose(fout) == EOF) {
        return -1;
    }
    return 0;
}

/**
 * Writes a pixel buffer to a BMP file with 24 bits per pixel.
 *
 * The pixel data is written in bottom-up order, with each pixel's RGB channels
 * reordered as BGR. The function assumes the input buffer uses 4 bytes per
 * pixel, with the fourth byte ignored. Returns 0 on success, or 1 if the file
 * cannot be opened.
 *
 * @param width Width of the image in pixels.
 * @param height Height of the image in pixels.
 * @param pixels Pointer to the pixel buffer (4 bytes per pixel, only RGB used).
 * @param file_name Name of the output BMP file.
 * @return 0 on success, 1 on failure to open the file.
 */
int bmp_write(unsigned int width, unsigned int height, unsigned char *pixels,
              const char *file_name) {
    unsigned char bmp_header[] = {
        /* BMP header structure: */
        0x42, 0x4d,             /* magic number */
        0x46, 0x00, 0x00, 0x00, /* size of header=70 bytes */
        0x00, 0x00,             /* unused */
        0x00, 0x00,             /* unused */
        0x36, 0x00, 0x00, 0x00, /* 54 bytes - offset to data */
        0x28, 0x00, 0x00, 0x00, /* 40 bytes - bytes in DIB header */
        0x00, 0x00, 0x00, 0x00, /* width of bitmap */
        0x00, 0x00, 0x00, 0x00, /* height of bitmap */
        0x01, 0x0,              /* 1 pixel plane */
        0x18, 0x00,             /* 24 bpp */
        0x00, 0x00, 0x00, 0x00, /* no compression */
        0x00, 0x00, 0x00, 0x00, /* size of pixel array */
        0x13, 0x0b, 0x00, 0x00, /* 2835 pixels/meter */
        0x13, 0x0b, 0x00, 0x00, /* 2835 pixels/meter */
        0x00, 0x00, 0x00, 0x00, /* color palette */
        0x00, 0x00, 0x00, 0x00, /* important colors */
    };
    FILE *fout;
    int x, y;

    bmp_header[18] = width & 0xff;
    bmp_header[19] = (width >> 8) & 0xff;
    bmp_header[20] = (width >> 16) & 0xff;
    bmp_header[21] = (width >> 24) & 0xff;
    bmp_header[22] = height & 0xff;
    bmp_header[23] = (height >> 8) & 0xff;
    bmp_header[24] = (height >> 16) & 0xff;
    bmp_header[25] = (height >> 24) & 0xff;

    fout = fopen(file_name, "wb");
    if (!fout) {
        return 1;
    }
    fwrite(bmp_header, sizeof(bmp_header), 1, fout);

    /* pixel array */
    for (y = height - 1; y >= 0; y--) {
        unsigned char *p = pixels + y * width * 4;
        for (x = 0; x < width; x++) {
            /* swap RGB */
            fwrite(p + 2, 1, 1, fout);
            fwrite(p + 1, 1, 1, fout);
            fwrite(p, 1, 1, fout);
            /* next pixel */
            p += 4;
        }
    }
    fclose(fout);
    return 0;
}

/**
 * Entry point for the program. Renders a test RGB image and writes it to both
 * PPM and BMP files.
 * @returns 0 on successful execution.
 */
int main(void) {
#define WIDTH 256
#define HEIGHT 256
    unsigned char *pixels = (unsigned char *)malloc(WIDTH * HEIGHT * 4);
    render_test_rgb_image(WIDTH, HEIGHT, pixels, 0);
    ppm_write_ascii(WIDTH, HEIGHT, pixels, "test_rgb_1.ppm");
    bmp_write(WIDTH, HEIGHT, pixels, "test_rgb_1.bmp");
    return 0;
}
