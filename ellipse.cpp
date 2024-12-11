#include <windows.h>
#include <GL/glut.h>
#include <vector>
#include <cmath>
#define PI 3.14

using namespace std;

int clicks = 0;
vector<vector<float>> points;
pair<int, int> P1, P2, P3;
float a, b;


float calculateRadius(pair<int, int> point1, pair<int, int> point2){
    return sqrt(pow(point1.first - point2.first, 2) + pow(point1.second - point2.second, 2));
}

void findPoints(){
    points.clear();
    for (float t = 0; t <= 2*PI; t+=0.1){
        float x = P1.first + a*cos(t);
        float y = P1.second + b*sin(t);
        points.push_back({x, y, 0});
    }
}


void display(){
    glClear(GL_COLOR_BUFFER_BIT);
    glBegin(GL_POINTS);
    for (auto& point: points){
        glColor3f(0, 0, 0);
        glVertex3f(point[0], point[1], point[2]);
    }
    glEnd();
    glFlush();
}

void mouse(int button, int state, int x, int y){
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN){
        if (clicks == 0){
            P1 = {x, 480 - y};
        }
        else if (clicks == 1){
            P2 = {x, 480 - y};
        }
        else if (clicks == 2){
            P3 = {x, 480 - y};
            a = max(calculateRadius(P1, P2), calculateRadius(P1, P3));
            b = min(calculateRadius(P1, P2), calculateRadius(P1, P3));
            findPoints();
            glutPostRedisplay();
        }
        else
            clicks = -1;

        clicks++;
    }
}

void init(){
    glClearColor(1.0, 1.0, 1.0, 0);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, 640, 0, 480);
}


int main(int argc, char **argv){
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE);
    glutInitWindowSize(400, 300);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Ellipse");
    glutDisplayFunc(display);
    init();
    glutMouseFunc(mouse);
    glutMainLoop();
    return 0;
}
