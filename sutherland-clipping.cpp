#include<windows.h>
#include <GL/glut.h>
#include <cmath>
#include <vector>

const int INSIDE = 0; // 0000
const int LEFT = 1;   // 0001
const int RIGHT = 2;  // 0010
const int BOTTOM = 4; // 0100
const int TOP = 8;    // 1000

float xmin, xmax, ymin, ymax;
bool isViewportSet = false;
std::vector<float> linePoints;

// Function to compute the region code for a point (x, y)
int computeCode(float x, float y) {
    int code = INSIDE;
    if (x < xmin)      // left
        code |= LEFT;
    else if (x > xmax) // right
        code |= RIGHT;
    if (y < ymin)      // bottom
        code |= BOTTOM;
    else if (y > ymax) // above
        code |= TOP;
    return code;
}

// Cohen-Sutherland clipping algorithm for line segment (x1, y1) to (x2, y2)
void cohenSutherlandClip(float x1, float y1, float x2, float y2) {
    int code1 = computeCode(x1, y1);
    int code2 = computeCode(x2, y2);
    bool accept = false;

    while (true) {
        if ((code1 | code2) == 0) {
            accept = true;
            break;
        } else if (code1 & code2) {
            break;
        } else {
            int codeOut;
            float x, y;

            if (code1 != 0)
                codeOut = code1;
            else
                codeOut = code2;

            if (codeOut & TOP) {
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1);
                y = ymax;
            } else if (codeOut & BOTTOM) {
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1);
                y = ymin;
            } else if (codeOut & RIGHT) {
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1);
                x = xmax;
            } else if (codeOut & LEFT) {
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1);
                x = xmin;
            }

            if (codeOut == code1) {
                x1 = x;
                y1 = y;
                code1 = computeCode(x1, y1);
            } else {
                x2 = x;
                y2 = y;
                code2 = computeCode(x2, y2);
            }
        }
    }

    if (accept) {
        glBegin(GL_LINES);
        glVertex2f(x1, y1);
        glVertex2f(x2, y2);
        glEnd();
    }
}

void drawClippingWindow() {
    glBegin(GL_LINE_LOOP);
    glVertex2f(xmin, ymin);
    glVertex2f(xmax, ymin);
    glVertex2f(xmax, ymax);
    glVertex2f(xmin, ymax);
    glEnd();
}


void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    if (isViewportSet) {
        drawClippingWindow();
    }
    glFlush();
}

// Mouse callback function
void mouseClick(int button, int state, int x, int y) {
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {
        if (!isViewportSet) {
            static bool firstClick = true;
            if (firstClick) {
                xmin = x;
                ymin = glutGet(GLUT_WINDOW_HEIGHT) - y;
                firstClick = false;
            } else {
                xmax = x;
                ymax = glutGet(GLUT_WINDOW_HEIGHT) - y;
                isViewportSet = true;
                firstClick = true;
                display(); 
            }
        } else {
            float wx = x;
            float wy = glutGet(GLUT_WINDOW_HEIGHT) - y;
            linePoints.push_back(wx);
            linePoints.push_back(wy);
            if (linePoints.size() == 4) {
                cohenSutherlandClip(linePoints[0], linePoints[1], linePoints[2], linePoints[3]);
                linePoints.clear();
                glFlush();
            }
        }
    }
}

void init() {
    glClearColor(1.0, 1.0, 1.0, 1.0);
    glColor3f(0.0, 0.0, 0.0);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, 800, 0, 600);
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowPosition(80, 80);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Clipped Window");
    init();
    glutDisplayFunc(display);
    glutMouseFunc(mouseClick);
    glutMainLoop();
    return 0;
}
