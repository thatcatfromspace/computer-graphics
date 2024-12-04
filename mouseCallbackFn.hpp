void mouse(int button, int state, int x, int y){
    if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN){
        arr[i].x = x;
        arr[i++].y = SCREEN_HEIGHT - y; // subtracted because height is inverted between mouse and screen
        std::cout << "mouse @ " << x << '\t' << y << '\n';
        glBegin(GL_POINTS);
        glVertex2f(x, SCREEN_HEIGHT - y);
        glEnd();
        glFlush();
    }
    else if (button == GLUT_RIGHT_BUTTON){
        glutPostRedisplay(); // cannot call display() as is b/c it is a callback
    }
}

// call glutMouseFunc(mouse) after init()
