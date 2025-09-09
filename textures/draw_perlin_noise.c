#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* be standard with Perlin functions */
#define random() rand()

#include "perlin.h"

/* link */
#include "perlin.c"

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
        0x46, 0x00, 0x00, 0x00, /* file size (to be filled later) */
        0x00, 0x00,             /* unused */
        0x00, 0x00,             /* unused */
        0x36, 0x00, 0x00, 0x00, /* 54 bytes - offset to data */
        0x28, 0x00, 0x00, 0x00, /* 40 bytes - bytes in DIB header */
        0x00, 0x00, 0x00, 0x00, /* width of bitmap (to be filled later) */
        0x00, 0x00, 0x00, 0x00, /* height of bitmap (to be filled later) */
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

    /* initialize BMP header */
    unsigned int pixels_size = width * height * 3;
    unsigned int file_size = sizeof(bmp_header) + pixels_size;

    /* file size */
    bmp_header[2] = file_size & 0xff;
    bmp_header[3] = (file_size >> 8) & 0xff;
    bmp_header[4] = (file_size >> 16) & 0xff;
    bmp_header[5] = (file_size >> 24) & 0xff;

    /* resolution */
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

    /* write BMP header */
    if (fwrite(bmp_header, sizeof(bmp_header), 1, fout) != 1) {
        fclose(fout);
        return 1;
    }

    /* write the whole pixel array into BMP file */
    for (y = height - 1; y >= 0; y--) {
        /* pointer to the 1st pixel on scan line */
        unsigned char *p = pixels + y * width * 4;
        for (x = 0; x < width; x++) {
            /* swap RGB color components as required by file format */
            if (fwrite(p + 2, 1, 1, fout) != 1 ||
                fwrite(p + 1, 1, 1, fout) != 1 ||
                fwrite(p, 1, 1, fout) != 1) {
                fclose(fout);
                return 1;
            }
            /* move to next pixel on scan line */
            p += 4;
        }
    }
    if (fclose(fout) == EOF) {
        return 1;
    }
    return 0;
}

void recalc_perlin_noise_2d(unsigned int width, unsigned int height,
                            const unsigned char *palette, unsigned char *pixels,
                            double xmin, double ymin, double xmax, double ymax,
                            double alpha, double beta, int n) {
  int x, y;
  double x1, y1, z;
  int color, i;
  unsigned char *p = pixels;
  double min = 1e10, max = -min;
  double k;

  init();

  /* find min and max values */
  y1 = ymin;
  for (y = 0; y < height; y++) {
    x1 = xmin;
    for (x = 0; x < width; x++) {
      x1 += (xmax - xmin) / width;
      z = PerlinNoise2D(x1, y1, alpha, beta, n);
      if (z < min)
        min = z;
      if (z > max)
        max = z;
    }
    y1 += (ymax - ymin) / height;
  }
  printf("%f %f\n", min, max);

  init();
  /* compute contrast */
  k = 255.0 / (max - min);

  y1 = ymin;
  for (y = 0; y < height; y++) {
    x1 = xmin;
    for (x = 0; x < width; x++) {
      x1 += (xmax - xmin) / width;
      z = PerlinNoise2D(x1, y1, alpha, beta, n);
      z -= min;
      z *= k;
      i = z;
      /* arithmetic with saturation */
      if (i < 0)
        i = 0;
      if (i > 255)
        i = 255;
      color = i * 3;
      *p++ = palette[color];
      *p++ = palette[color + 1];
      *p++ = palette[color + 2];
      p++;
    }
    y1 += (ymax - ymin) / height;
  }
}

int main(int argc, char **argv) {
#define WIDTH 256
#define HEIGHT 256

  int i = 0;
  double limit = 3;

  unsigned char *pixels = (unsigned char *)malloc(WIDTH * HEIGHT * 4);
  unsigned char *palette = (unsigned char *)malloc(256 * 3);
  for (i = 0; i < 256; i++) {
    int color = i * 3;
    palette[color] = i;
    palette[color + 1] = i;
    palette[color + 2] = i;
  }

  for (i = 0; i < 10; i++) {
    char str[100];
    sprintf(str, "perlin%02d.bmp", i);
    printf("generating noise %s...", str);

    recalc_perlin_noise_2d(WIDTH, HEIGHT, palette, pixels, -limit, -limit, limit, limit,
                           2, 2, i + 2);
    bmp_write(WIDTH, HEIGHT, pixels, str);
    printf("   done\n");
  }
  return 0;
}
