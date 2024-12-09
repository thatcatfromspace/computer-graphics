#include <GL/glut.h>
#include <vector>
#include <cmath>
#define PI 3.14

using namespace std;

vector<vector<float>> points;
int clicks = 0;
int X1 = 0, Y1 = 0;
int X2 = 0, Y2 = 0;
float radius;

void calculateRadius(){
    radius = sqrt(pow(X1 - X2, 2) + pow(Y1 - Y2, 2));
}

void circlePoints() {
    for (float t = 0; t <= PI * 2; t += 0.01) {
        float x = X1 + (radius * cos(t));
        float y = X2 + (radius * sin(t));
        points.push_back({x, y, 0.0});
    }
}

void display(void) {
    glClear(GL_COLOR_BUFFER_BIT);
    // glPointSize(4);
    glBegin(GL_POINTS);
    for (auto& point : points) {
        glColor3f(0, 0, 0);
        glVertex3f(point[0], point[1], point[2]);
    }
    glEnd();
    glFlush();
}

void mouse(int button, int state, int x, int y){
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN && clicks == 0){
        X1 = x;
        Y1 = y;
        clicks++;
    }
    else if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN && clicks == 1){
        X2 = x;
        Y2 = y;
        clicks++;
    }
}

void init() {
    glClearColor(1.0, 1.0, 1.0, 0.0);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, 640, 0, 480); // follow aspect ratio of screen
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE);
    glutInitWindowSize(400, 300);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Circle");
    calculateRadius();
    circlePoints();
    glutDisplayFunc(display);
    init();
    glutMainLoop();
    return 0;
}