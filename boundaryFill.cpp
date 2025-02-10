#include <GL/glut.h>
#include <vector>
#include <iostream>

class Point {
public:
    int x, y;
    Point(int x, int y): x(x), y(y) {};
    Point() {};
};

std::vector<Point> points;
bool drawPolygonFlag = false;
int rightClicks = 0;
std::vector<std::pair<int, int>> dirs = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};


void getPixelColor(int x, int y, unsigned char* color) {
    glReadPixels(x, y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE, color);
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    
    if (drawPolygonFlag && !points.empty()) {
        glColor3f(0.0, 0.0, 1.0);
        glBegin(GL_LINE_LOOP);
        rightClicks++;
        for (auto point : points) {
            glVertex2i(point.x, point.y);
            unsigned char buf[3];
            getPixelColor(point.x, point.y, buf);
            std::cout << (int)buf[0] << " " << (int)buf[1] << " " << (int)buf[2] << std::endl;
        }
        glEnd();
    }
    glFlush();
}

bool equalColors(unsigned char* curr){
    return (int)curr[0] == 0 && (int)curr[1] == 0 && (int)curr[2] == 127;
}

void boundaryFill(int x, int y){
    unsigned char curr[3];
    getPixelColor(x, y, curr);
    std::cout << (int)curr[0] << " " << (int)curr[1] << " " << (int)curr[2] << "\n";
    if (equalColors(curr)) return;

    glColor3f(0, 0, 1);
    glBegin(GL_POINTS);
    glVertex2i(x, y);
    glEnd();
    glFlush();

    for (auto [dx, dy]: dirs){
        int sx = x + dx;
        int sy = y + dy;
        std::cout << "Visitting " << sx << ", " << sy << std::endl;
        boundaryFill(sx, sy);
    }
}

void mouse(int button, int state, int x, int y) {
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {
        points.push_back(Point(x, 360 - y));
    } else if (button == GLUT_RIGHT_BUTTON && state == GLUT_DOWN && rightClicks < 1) {
        drawPolygonFlag = true;
        glutPostRedisplay();
    } else if (button == GLUT_RIGHT_BUTTON && state == GLUT_DOWN && rightClicks >= 1){
        boundaryFill(x, 360 - y);
    }
}

void init() {
    glClearColor(0.2, 0, 0.3, 1.0);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, 480, 0, 360);
}

int main(int argc, char* argv[]) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(480, 360);
    glutInitWindowPosition(400, 400);
    glutCreateWindow("Coloring");
    glutDisplayFunc(display);
    glutMouseFunc(mouse);
    init();
    glutMainLoop();
    return 0;
}
