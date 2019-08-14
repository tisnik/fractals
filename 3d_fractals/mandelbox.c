#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#define WIDTH  400
#define HEIGHT 400

void writeImage(int width, int height, unsigned char *image)
{
    int i;
    puts("P2");
    printf("%d %d\n", width, height);
    puts("255");
    for (i=0; i<width*height; i++) {
        printf("%d ", image[i]);
    }
}

#define maxiter 4

int main(int argc, char **argv)
{
    double cx, cy;
    double zx, zy;
    double magnitude;

    const double scale = -1.1;

    int i, j, n;

    char pixels[WIDTH * HEIGHT];
    memset((void*)pixels, 0, (size_t)(WIDTH*HEIGHT));

    cy = -4.0;
    for (j = 0; j < HEIGHT; j++) {
        cx = -4.0;
        for (i = 0; i < WIDTH; i++) {
            double zx = 0, zy = 0;
            for (n = 0; n < maxiter; n++) {
                if (zx>1) {
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
                double zx2 = zx * zx;
                double zy2 = zy * zy;
                magnitude = sqrt(zx2 + zy2);
                if (zx2 + zy2 > 256.0) break;
                if (magnitude < 0.5) {
                    zx = zx * 4;
                    zy = zy * 4;
                }
                else if (magnitude < 1.0) {
                    zx=zx/(magnitude*magnitude);
                    zy=zy/(magnitude*magnitude);
                }
                else {
                    zx = scale * zx;
                    zy = scale * zy;
                }
                zx += cx;
                zy += cy;
            }
            pixels[j*WIDTH+i] = n*20;
            cx += 8.0 / WIDTH;
        }
        cy += 8.0 / HEIGHT;
    }

    writeImage(WIDTH, HEIGHT, pixels);
    return 0;
}

