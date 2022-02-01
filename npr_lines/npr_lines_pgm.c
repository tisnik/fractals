#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define WIDTH 640
#define HEIGHT 480

#define ABS(a) ((a)<0 ? -(a) : (a) )
#define MAX(a,b) ((a)>(b) ? (a) : (b))
#define MIN(a,b) ((a)<(b) ? (a) : (b))

unsigned char bitmap[HEIGHT][WIDTH];

void clear_bitmap()
{
    memset(bitmap, 255, sizeof(bitmap));
}

void putpixel(int x, int y, int c)
{
    if (x>=0 && x<WIDTH && y>=0 && y<HEIGHT)
    {
        bitmap[y][x] = c;
    }
}

void putpixel_min(int x, int y, int c)
{
    if (x>=0 && x<WIDTH && y>=0 && y<HEIGHT)
    {
        bitmap[y][x] = MIN(bitmap[y][x], c);
    }
}

void write_pgm(char *file_name)
{
    FILE *fout = fopen(file_name, "wb");
    fprintf(fout, "P5\n");
    fprintf(fout, "%d\n%d\n255\n", WIDTH, HEIGHT);
    fwrite(bitmap, sizeof(bitmap), 1, fout);
    fclose(fout);
}

void h_line(int x1, int x2, int y)
{
    int x, from_x=MIN(x1, x2), to_x=MAX(x1, x2);
    for (x=from_x; x<=to_x; x++)
    {
        putpixel_min(x, y, 0);
    }
}

void v_line(int x, int y1, int y2)
{
    int y, from_y=MIN(y1, y2), to_y=MAX(y1, y2);
    for (y=from_y; y<=to_y; y++)
    {
        putpixel_min(x, y, 0);
    }
}

void line(int x1, int y1, int x2, int y2)
{
    int dx=x2-x1;
    int dy=y2-y1;
    double s, p, e=255.0;
    int x, y, xdelta, ydelta, xpdelta, ypdelta, xp, yp;
    int i, imin, imax;

    if (x1==x2)
    {
        v_line(x1, y1, y2);
        return;
    }

    if (y1==y2)
    {
        h_line(x1, x2, y1);
        return;
    }
    if (x1>x2)
    {
        x1=x1^x2; x2=x1^x2; x1=x1^x2;
        y1=y1^y2; y2=y1^y2; y1=y1^y2;
    }

    if (ABS(dx)>ABS(dy))
    {
        s=(double)dy/(double)dx;
        imin=x1;  imax=x2;
        x=x1;     y=y1;
        xdelta=1; ydelta=0;
        xpdelta=0;
        xp=0;
        if (y2>y1)
        {
            ypdelta=1;
            yp=1;
        }
        else
        {
            s=-s;
            ypdelta=-1;
            yp=-1;
        }
    }
    else
    {
        s=(double)dx/(double)dy;
        xdelta=0; ydelta=1;
        ypdelta=0;
        yp=0;
        if (y2>y1)
        {
            imin=y1;    imax=y2;
            x=x1;       y=y1;
            xpdelta=1;
            xp=1;
        }
        else
        {
            s=-s;
            imin=y2;    imax=y1;
            x=x2;       y=y2;
            xpdelta=-1;
            xp=-1;
        }
    }
    p=s*256.0;
    for (i=imin; i<=imax; i++) {
        int c1=(int)e;
        int c2=255-c1;
        putpixel_min(x+xp, y+yp, c1);
        putpixel_min(x, y, c2);
        e=e-p;
        x+=xdelta;
        y+=ydelta;
        if (e<0.0) {
            e+=256.0;
            x+=xpdelta;
            y+=ypdelta;
        }
    }
}

void npr_line(int x1, int y1, int x2, int y2, double maxd)
{
 //   line(x1, y1, x2, y2);
    int dist = ABS(x2-x1) + ABS(y2-y1);
    if (dist < 20)
    {
        line(x1, y1, x2, y2);
    }
    else
    {
        int midx, midy;
        float nx, ny;
        float d;
        float nd;

        midx = (x1 + x2) >> 1;
        midy = (y1 + y2) >> 1;

        nx = (y1-y2);
        ny = (x2-x1);
        nd = sqrtf(nx*nx + ny*ny);
        nx /= nd;
        ny /= nd;
        d = maxd * (((float)rand()/RAND_MAX) - 0.5);
        midx += nx * d;
        midy += ny * d;
        npr_line(x1, y1, midx, midy, maxd/1.8);
        npr_line(midx, midy, x2, y2, maxd/1.8);
    }
}

void draw_demo()
{
    int i;
    for (i = 0; i < 500; i+=25)
    {
        srand(6503);
        npr_line(50, 25 + i, WIDTH - 50, 25 + i, i/2.0);
    }

}

void draw_square()
{
    npr_line(20, 20, 200, 20, 10);
    npr_line(200, 20, 200, 200, 10);
    npr_line(20, 200, 200, 200, 10);
    npr_line(20, 200, 20, 20, 10);
}

void draw_diamond()
{
#define W 50
    npr_line(60 - W, 160, 60, 160 - W, 10);
    npr_line(60, 160 - W, 60 + W, 160, 10);
    npr_line(60 + W , 160, 60, 160 + W, 10);
    npr_line(60, 160 + W, 60 - W, 160, 10);
#undef W
}

void draw_star()
{
#define STEP 5
    int i;
    float x1, y1, x2, y2;
    for (i=0; i<360; i+=360/STEP)
    {
        x1 = 200.0*cos(i*M_PI/180.0);
        y1 = 200.0*sin(i*M_PI/180.0);
        x2 = 200.0*cos((i+3*360/STEP)*M_PI/180.0);
        y2 = 200.0*sin((i+3*360/STEP)*M_PI/180.0);
        npr_line(400+x1, 220+y1, 400+x2, 220+y2, 10);
    }
#undef STEP
}

void draw_lines()
{
    draw_square();
    draw_diamond();
    draw_star();
}

int main(void)
{
    puts("begin");
    clear_bitmap();
    draw_lines();
    write_pgm("out.pgm");
    puts("end");
    return 0;
}

