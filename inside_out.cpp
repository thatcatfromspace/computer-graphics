#include <GL/glut.h>
#include <vector>
#include <iostream>

std::vector<std::pair<float, float>> polygon;

bool isPointInsidePolygon(const std::vector<std::pair<float, float>>& polygon, std::pair<float, float> point) {
    float x = point.first, y = point.second;
    int n = polygon.size();
    bool inside = false;
    
    for (int i = 0, j = n - 1; i < n; j = i++) {
        float xi = polygon[i].first, yi = polygon[i].second;
        float xj = polygon[j].first, yj = polygon[j].second;
        
        bool intersect = ((yi > y) != (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) {
            inside = !inside;
        }
    }
    return inside;
}

int rightClicks = 0;

void mouse(int button, int state, int x, int y){
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN){
        if (rightClicks == 0){
            polygon.push_back({x, 360 - y});
        }
    }
    else if (button == GLUT_RIGHT_BUTTON && state == GLUT_DOWN){
        rightClicks++;
        glutPostRedisplay();
    }
}

void init(){
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, 480, 0, 360);
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT);

    std::pair<float, float> point = {200, 200};
    
    // Draw Polygon
    glColor3f(1.0, 0.0, 0.0);  // Red color for the polygon
    glBegin(GL_LINE_LOOP);
    for (const auto& vertex : polygon) {
        glVertex2f(vertex.first, vertex.second);
    }
    glEnd();
    
    // Test Point
    glColor3f(0.0, 1.0, 0.0);  // Green color for the point
    glPointSize(3);
    glBegin(GL_POINTS);
    glVertex2f(point.first, point.second);
    glEnd();
    
    if (isPointInsidePolygon(polygon, point)) {
        std::cout << "Point is inside the polygon" << std::endl;
    } else {
        std::cout << "Point is outside the polygon" << std::endl;
    }

    glFlush();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(480, 360);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Inside-Outside Test");
    glClearColor(0.0, 0.0, 0.0, 0.0);
    init();
    glutDisplayFunc(display);
    glutMouseFunc(mouse);
    glutMainLoop();
    return 0;
}
