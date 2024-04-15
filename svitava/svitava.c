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

#include <stdio.h>
#include <stdlib.h>


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

void render_julia(unsigned int width, unsigned int height,
                  const unsigned char *palette, unsigned char *pixels,
                  double cx, double cy) {
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
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

void render_barnsley_m1(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels) {
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
            while (i < 150) {
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

void render_barnsley_j1(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        double cx, double cy) {
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
            while (i < 150) {
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
            {
                unsigned char *pal =
                    (unsigned char *)palette + (unsigned char)(i * 3);

                *p++ = *pal++;
                *p++ = *pal++;
                *p++ = *pal;
                p++;
            }
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

void render_barnsley_m2(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels) {
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
            while (i < 150) {
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

void render_barnsley_j2(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        double cx, double cy) {
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
            while (i < 150) {
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
            {
                unsigned char *pal =
                    (unsigned char *)palette + (unsigned char)(i * 3);

                *p++ = *pal++;
                *p++ = *pal++;
                *p++ = *pal;
                p++;
            }
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

void render_barnsley_m3(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels) {
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
            while (i < 150) {
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

void render_barnsley_j3(unsigned int width, unsigned int height,
                        const unsigned char *palette, unsigned char *pixels,
                        double cx, double cy) {
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
            while (i < 150) {
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
            {
                unsigned char *pal =
                    (unsigned char *)palette + (unsigned char)(i * 3);

                *p++ = *pal++;
                *p++ = *pal++;
                *p++ = *pal;
                p++;
            }
            zx0 += (xmax - xmin) / width;
        }
        zy0 += (ymax - ymin) / height;
    }
}

void render_magnet_m1(unsigned int width, unsigned int height,
                     const unsigned char *palette, unsigned char *pixels) {
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
            while (i < 150) {
                double zx2, zy2, zxn, zyn, tzx, tzy, bzx, bzy, div;
                zx2=zx*zx;
                zy2=zy*zy;
                if (zx2+zy2>100) break;
                if (((zx-1.0)*(zx-1.0)+zy*zy)<0.001) break;
                tzx=zx2-zy2+cx-1;
                tzy=2.0*zx*zy+cy;
                bzx=2.0*zx+cx-2;
                bzy=2.0*zy+cy;
                div=bzx*bzx+bzy*bzy;
#define MIN_VALUE 1.0-100
                if (div<MIN_VALUE) break;
                zxn=(tzx*bzx+tzy*bzy)/div;
                zyn=(tzy*bzx-tzx*bzy)/div;
                zx=(zxn+zyn)*(zxn-zyn);
                zy=2.0*zxn*zyn;
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

void ppm_write_ascii_to_stream(unsigned int width, unsigned int height, unsigned char *pixels, FILE *fout)
{
    int x, y;
    unsigned char r, g, b;
    unsigned char *p = pixels;

    /* header */
    fprintf(fout, "P3 %d %d 255\n", width, height);

    /* pixel array */
    for (y=height-1; y>=0; y--) {
        for (x=0; x<width; x++) {
            r = *p++;
            g = *p++;
            b = *p++;
            p++;
            fprintf(fout, "%d %d %d\n", r, g, b);
        }
    }
}

int ppm_write_ascii(unsigned int width, unsigned int height, unsigned char *pixels, const char *file_name)
{
    FILE *fout;

    fout = fopen(file_name, "wb");
    if (!fout)
    {
        return -1;
    }

    ppm_write_ascii_to_stream(width, height, pixels, fout);

    if (fclose(fout) == EOF)
    {
        return -1;
    }
    return 0;
}

int main(void) {
#define WIDTH 256
#define HEIGHT 256
    unsigned char *pixels = (unsigned char*) malloc(WIDTH*HEIGHT*4);
    render_test_rgb_image(WIDTH, HEIGHT, pixels, 0);
    ppm_write_ascii(WIDTH, HEIGHT, pixels, "test_rgb_1.ppm");
    return 0;
}
