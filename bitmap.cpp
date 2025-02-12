#include<windows.h>
#include <GL/glut.h>

void display() {
   glClear(GL_COLOR_BUFFER_BIT);
   GLubyte bitShape[20] = {
       0xfc, 0x00, 0x66, 0x00, 0x66, 0x00, 0x7c, 0x00, 0x66, 0x00,
       0x66, 0x00, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
   };
   glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
   glRasterPos2i(30, 40);
   glColor3f(1.0f, 1.0f, 1.0f);
   glBitmap(9, 10, 0.0, 0.0, 0.0, 0.0, bitShape);
   glFlush();
}
void init() {
   glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
   glMatrixMode(GL_PROJECTION);
   glLoadIdentity();
   gluOrtho2D(0, 200, 0, 100);
}
int main(int argc, char** argv) {
   glutInit(&argc, argv);
   glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
   glutInitWindowSize(200, 100);
   glutCreateWindow("Bitmap Letter B");
   init();
   glutDisplayFunc(display);
   glutMainLoop();
   return 0;
}
