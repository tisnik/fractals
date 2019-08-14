#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#define WIDTH  400
#define HEIGHT 400

void writeImage(const int width, const int height, const unsigned char *image)
{
    int i;
    puts("P2");
    printf("%d %d\n", width, height);
    puts("255");
    for (i=0; i<width*height; i++) {
        printf("%d ", image[i]);
    }
}

void toLogarithmicScale(const int width, const int height,
                        unsigned char *pixels, const float *floatPixels, const float max)
{
    int i;
    for (i = 0; i < WIDTH*HEIGHT; i++) {
        if (floatPixels[i] == -1) {
            pixels[i] = 0x00;
        }
        else {
            int val = (int)(log(floatPixels[i])/log(max)*255);
            pixels[i] = val;
        }
    }
}

void calcMandelbox(const int width, const int height, float *floatPixels, const int maxiter, float *max)
{
    float cx, cy;
    float zx, zy;
    float magnitude, squared;

    int i, j, n;

    cy = -4.0;
    for (j = 0; j < height; j++) {
        cx = -4.0;
        for (i = 0; i < width; i++) {
            float zx = 0, zy = 0;
            for (n = 0; n < maxiter; n++) {
                if (zx>1.0) {
                    zx = 2.0-zx;
                }
                else if (zx<-1.0) {
                    zx = -2.0-zx;
                }
                if (zy>1.0) {
                    zy = 2.0-zy;
                }
                else if (zy<-1.0) {
                    zy = -2.0-zy;
                }
                float zx2 = zx * zx;
                float zy2 = zy * zy;
                squared = zx2 + zy2;
                magnitude = sqrt(squared);
                if (squared > 256.0) {
                    break;
                }
                if (magnitude < 0.5) {
                    zx = zx * 8.0 * magnitude;
                    zy = zy * 8.0 * magnitude;
                }
                else if (magnitude < 1.0) {
                    zx = zx * 2.0 / (magnitude*magnitude);
                    zy = zy * 2.0 / (magnitude*magnitude);
                }
                else {
                    zx = zx * 2.0 * magnitude;
                    zy = zy * 2.0 * magnitude;
                }
                zx += cx;
                zy += cy;
                zx2 = zx * zx;
                zy2 = zy * zy;
                squared = zx2 + zy2;
            }
            if (squared > *max) {
                *max = squared;
            }
            if (n == maxiter) {
                floatPixels[i+j*WIDTH] = squared;
            }
            else {
                floatPixels[i+j*WIDTH] = -1;
            }
            cx += 4.0 / WIDTH;
        }
        cy += 4.0 / HEIGHT;
    }

}

int main(int argc, char **argv)
{
    char pixels[WIDTH * HEIGHT];
    float floatPixels[WIDTH * HEIGHT];
    float max = 0;

    calcMandelbox(WIDTH, HEIGHT, floatPixels, 6, &max);
    toLogarithmicScale(WIDTH, HEIGHT, pixels, floatPixels, max);
    writeImage(WIDTH, HEIGHT, pixels);

    return 0;
}
