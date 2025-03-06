#include <windows.h>
#include <GL/glut.h>
#include <vector>
#include <iostream>

std::vector<std::pair<float, float>> polygon;

bool oddParityFill(const std::vector<std::pair<float, float>>& polygon, std::pair<float, float> point) {
    float x = point.first, y = point.second;
    int crossings = 0;

    for (int i = 0, j = polygon.size() - 1; i < polygon.size(); j = i++) {
        float xi = polygon[i].first, yi = polygon[i].second;
        float xj = polygon[j].first, yj = polygon[j].second;


        if ((yi > y) != (yj > y)) {  // Edge crosses y-level
            if (x < (xj - xi) * (y - yi) / (yj - yi) + xi) {  // Point is left of intersection
                crossings++;
            }
        }
    }
    return (crossings % 2) == 1;
}

bool windingNumberFill(const std::vector<std::pair<float, float>>& polygon, std::pair<float, float> point) {
    float x = point.first, y = point.second;
    int winding = 0;

    for (int i = 0, j = polygon.size() - 1; i < polygon.size(); j = i++) {
        float xi = polygon[i].first, yi = polygon[i].second;
        float xj = polygon[j].first, yj = polygon[j].second;

        if (yi <= y) {  // Upward crossing
            if (yj > y && (xj - xi) * (y - yi) - (x - xi) * (yj - yi) > 0) {
                winding++;
            }
        } else {  // Downward crossing
            if (yj <= y && (xj - xi) * (y - yi) - (x - xi) * (yj - yi) < 0) {
                winding--;
            }
        }
    }
    return winding != 0;
}

int rightClicks = 0;

void mouse(int button, int state, int x, int y) {
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {
        if (rightClicks == 0) {
            polygon.push_back({x, 360 - y});
        }
    }
    else if (button == GLUT_RIGHT_BUTTON && state == GLUT_DOWN) {
        rightClicks++;
        glutPostRedisplay();
    }
}

void init() {
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, 480, 0, 360);
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT);

    std::pair<float, float> point = {200, 200};

    // Draw Polygon
    glColor3f(1.0, 0.0, 0.0);  // Red color for polygon
    glBegin(GL_LINE_LOOP);
    for (const auto& vertex : polygon) {
        glVertex2f(vertex.first, vertex.second);
    }
    glEnd();

    // Draw Test Point
    glColor3f(0.0, 1.0, 0.0);  // Green color for point
    glPointSize(5);
    glBegin(GL_POINTS);
    glVertex2f(point.first, point.second);
    glEnd();

    bool oddParity = oddParityFill(polygon, point);
    bool winding = windingNumberFill(polygon, point);

    std::cout << "Odd Parity: " << (oddParity ? "Inside" : "Outside") << std::endl;
    std::cout << "Winding Number: " << (winding ? "Inside" : "Outside") << std::endl;
    std::cout << "------------------------" << std::endl;

    glFlush();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(480, 360);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Polygon Fill Test");
    glClearColor(0.0, 0.0, 0.0, 0.0);
    init();
    glutDisplayFunc(display);
    glutMouseFunc(mouse);
    glutMainLoop();
    return 0;
}

	
