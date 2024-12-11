// #include <windows.h> 
#include <GL/glut.h>

void display() {
    glClear(GL_COLOR_BUFFER_BIT); 
    glFlush(); // Render now
}

void init() {
    glClearColor(1.0, 1.0, 1.0, 0.0); 
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, 640, 0, 480); 
}

int main(int argc, char **argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(640, 480);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("OpenGL Template");
    init();
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}
