#include <windows.h>
#include <iostream>
#ifdef __APPLE_CC__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif // __APPLE_CC__

void display(){
    glClear(GL_COLOR_BUFFER_BIT); // buffers - color buffer (2D), color + depth buffer (3D)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE); // don't fill polygon

    glPointSize(4); // MUST be outside glBegin()
    glBegin(GL_POLYGON);
    glColor3f(1, 0, 0); glVertex3f(-0.6, -0.75, 0.5); // color - (R, G, B)
    glColor3f(1, 1, 0); glVertex3f(0.6, -0.75, 0);
    glColor3f(1, 0, 1); glVertex3f(0, 0.75, 0);
    //glColor3f(0, 1, 1); glVertex3f(0.2, -0.2, 0.5);
    glEnd();

    glFlush();
}

int main(int argc, char** argv){
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowPosition(80, 80);
    glutInitWindowSize(400, 300);
    glutCreateWindow("Simple Triangle");
   // glClearColor(1, 1, 1, 1); // sets background color

    glutDisplayFunc(display); // glutDisplayFunc --> callback fn

    glutMainLoop();
}
