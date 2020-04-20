#include <GL/glut.h>

#include <stdio.h>
#include <string.h>
#include <math.h>

#define WINDOW_WIDTH 640
#define WINDOW_HEIGHT 480

#define WINDOW_TITLE "npr lines"

#define ABS(a) ((a)<0 ? -(a) : (a) )
#define MAX(a,b) ((a)>(b) ? (a) : (b))
#define MIN(a,b) ((a)<(b) ? (a) : (b))



//-----------------------------------------------------------------------------
// Funkce volana pro inicializaci vykreslovani
//-----------------------------------------------------------------------------
void onInit(void)
{
    glClearColor(1.0f, 1.0f, 1.0f, 0.0f);       // barva pozadi
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);      // mod ulozeni pixelu
    glDisable(GL_POINT_SMOOTH);
    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}



//-----------------------------------------------------------------------------
// Nastaveni souradneho systemu v zavislosti na velikosti okna
//-----------------------------------------------------------------------------
void onResize(int w, int h)                     // argumenty w a h reprezentuji novou velikost okna
{
    glViewport(0, 0, w, h);                     // viditelna oblast pres cele okno
    glMatrixMode(GL_PROJECTION);                // zacatek modifikace projekcni matice
    glLoadIdentity();                           // vymazani projekcni matice (=identita)
    glOrtho(0, w, 0, h, -1, 1);                 // mapovani abstraktnich souradnic do souradnic okna
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();                           // vymazani projekcni matice (=identita)
    //glTranslatef(0, h, 0);
    //glScalef(1, -1, 1);
}


void line(int x1, int y1, int x2, int y2)
{
    glVertex2i(x1, y1);
    glVertex2i(x2, y2);
}

void npr_line(int x1, int y1, int x2, int y2, double maxd)
{
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
        glBegin(GL_LINE_STRIP);
        srand(6503);
        npr_line(50, 25 + i, WINDOW_WIDTH - 50, 25 + i, i/2.0);
        glEnd();
    }

}

void draw_square()
{
    glBegin(GL_LINES);
    npr_line(20, 20, 200, 20, 10);
    npr_line(200, 20, 200, 200, 10);
    npr_line(20, 200, 200, 200, 10);
    npr_line(20, 200, 20, 20, 10);
    glEnd();
}

void draw_diamond()
{
#define W 50
        glBegin(GL_LINES);
    npr_line(60 - W, 160, 60, 160 - W, 10);
    npr_line(60, 160 - W, 60 + W, 160, 10);
    npr_line(60 + W , 160, 60, 160 + W, 10);
    npr_line(60, 160 + W, 60 - W, 160, 10);
        glEnd();
#undef W
}

void draw_star()
{
    puts("draw star");
#define STEP 5
    int i;
    float x1, y1, x2, y2;
    glBegin(GL_LINES);
    for (i=0; i<360; i+=360/STEP)
    {
        x1 = 200.0*cos(i*M_PI/180.0);
        y1 = 200.0*sin(i*M_PI/180.0);
        x2 = 200.0*cos((i+3*360/STEP)*M_PI/180.0);
        y2 = 200.0*sin((i+3*360/STEP)*M_PI/180.0);
        npr_line(400+x1, 220+y1, 400+x2, 220+y2, 10);
    }
    glEnd();
#undef STEP
}

void drawLines()
{
    puts("draw lines");
    draw_demo();
    glColor3f(0.5f, 0.0f, 0.0f);
    draw_square();
    glColor3f(0.0f, 0.5f, 0.0f);
    draw_diamond();
    glColor3f(0.0f, 0.0f, 0.5f);
    draw_star();
}


//-----------------------------------------------------------------------------
// Callback funkce zavolana pri kazdem prekresleni okna
//-----------------------------------------------------------------------------
void onDisplay(void)
{
    glClear(GL_COLOR_BUFFER_BIT);               // vymazani vsech bitovych rovin barvoveho bufferu
    glDrawBuffer(GL_BACK);                      // pixmapa se bude kreslit do zadniho barvoveho bufferu

    glColor3f(0.0f, 0.0f, 0.0f);
    glBegin(GL_TRIANGLES);
    glVertex2i(0,0);
    glVertex2i(100,0);
    glVertex2i(100,100);
    glEnd();
    //drawLines();
    glFlush();                                  // provedeni a vykresleni vsech zmen

    glutSwapBuffers();
}

void onKeyboard(unsigned char key, int x, int y)
{
    switch (key)
    {
        case 'q':
        case 'Q':
        case 27:  exit(0);  break;// pokud byla stlacena klavesa ESC, konec programu
        default:  break; 
    }
}



//-----------------------------------------------------------------------------
// Hlavni funkce konzolove aplikace
//-----------------------------------------------------------------------------
int main(int argc, char **argv)
{
    glutInit(&argc, argv);                      // inicializace knihovny GLUT
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE);
    glutCreateWindow(WINDOW_TITLE);             // vytvoreni okna pro kresleni
    glutReshapeWindow(WINDOW_WIDTH, WINDOW_HEIGHT);// zmena velikosti okna
    glutPositionWindow(100, 100);               // pozice leveho horniho rohu okna
    glutDisplayFunc(onDisplay);                 // registrace funkce volane pri prekreslovani okna
    glutReshapeFunc(onResize);                  // registrace funkce volane pri zmene velikosti okna
    glutKeyboardFunc(onKeyboard);               // registrace funkce volane pri stlaceni klavesy
 //   glutIdleFunc(onIdle);
    onInit();                                   // inicializace vykreslovani
    glutMainLoop();                             // nekonecna smycka, kde se volaji zaregistrovane funkce
    return 0;                                   // navratova hodnota vracena operacnimu systemu
}



//-----------------------------------------------------------------------------
// finito
//-----------------------------------------------------------------------------
