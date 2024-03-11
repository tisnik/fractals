/*

   (C) Copyright 2024  Pavel Tisnovsky

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

void render_test_palette_image(unsigned int width, unsigned int height,
                               const unsigned char *palette,
                               unsigned char *pixels) {
    unsigned int i, j;
    unsigned char *p = pixels;

    for (j = 0; j < height; j++) {
        for (i = 0; i < width; i++) {
            int color = i * 3;
            *p++ = palette[color];
            *p++ = palette[color + 1];
            *p++ = palette[color + 2];
            p++;
        }
    }
}

void render_mandelbrot(unsigned int width, unsigned int height,
                       const unsigned char *palette, unsigned char *pixels) {
    int x, y;
    double cx, cy;
    double xmin = -2.0, ymin = -1.5, xmax = 1.0, ymax = 1.5;
    unsigned char *p = pixels;

    cy = ymin;
    for (y = 0; y < height; y++) {
        cx = xmin;
        for (x = 0; x < width; x++) {
            double zx = 0.0;
            double zy = 0.0;
            unsigned int i = 0;
            while (i < 150) {
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                if (zx2 + zy2 > 4.0) {
                    break;
                }
                zy = 2.0 * zx * zy + cy;
                zx = zx2 - zy2 + cx;
                i++;
            }
            {
                unsigned char *pal =
                    (unsigned char *)palette + (unsigned char)(i * 3);

                *p++ = *pal++;
                *p++ = *pal++;
                *p++ = *pal;
                p++;
            }
            cx += (xmax - xmin) / width;
        }
        cy += (ymax - ymin) / height;
    }
}

void render_circle_pattern(unsigned int width, unsigned int height,
                           const unsigned char *palette,
                           unsigned char *pixels) {
    unsigned char *p = pixels;

    double xmin = -150;
    double ymin = -150;
    double xmax = 150;
    double ymax = 150;

    int i, j;
    double x1, y1;

    y1=ymin;
    for (j = 0; j < height; j++) {
        x1=xmin;
        for (i = 0; i < width; i++) {
            double x2=x1*x1;
            double y2=y1*y1;
            int i = (int)(x2 + y2) % 256;
            int color = i * 3;
            *p++ = palette[color];
            *p++ = palette[color + 1];
            *p++ = palette[color + 2];
            p++;
            x1+=(xmax-xmin)/width;
        }
        y1+=(ymax-ymin)/height;
    }
}

