import time
import numpy as np
import graphics as gr

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CENTER = np.array((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

ONES = np.ones((4, 1))

TETA = 3
T_SPEED = 1.1

M = np.array([[1, 0, 0], [0, 1, 0], [5, 10, 1]])

R = np.array([
    [np.cos(TETA), np.sin(TETA), 0],
    [-np.sin(TETA), np.cos(TETA), 0],
    [0, 0, 1],
])

T = np.array([
    [T_SPEED, 0, 0],
    [0, T_SPEED, 0],
    [0, 0, 1],
])

M1 = np.copy(M)
M2 = np.copy(M)

def remove_shape(shape):
    shape.setOutline("red")

def redraw_shape(points, shape):
    if shape:
        remove_shape(shape)
    shape = gr.Polygon(*[gr.Point(int(x), int(y)) for (x, y) in points])
    shape.draw(win)
    return shape

def shape_center(points):
    return np.array(((points[0][0] + points[2][0]) / 2,
                     (points[0][1] + points[2][1]) / 2))

def transform(points, transformation):
    P = np.concatenate((points - shape_center(points), ONES), axis=1)
    P_stroke = P @ transformation
    return P_stroke[:, :2] + shape_center(points)

def apply_transformations(diamond_points, transformations, diamond):
    for i in range(100):
        for transformation in transformations:
            diamond_points = transform(diamond_points, transformation)
        
        diamond = redraw_shape(diamond_points, diamond)

        if (i // 20) % 2 == 0:
            transformations[2][0, 0] = T_SPEED
            transformations[2][1, 1] = T_SPEED
            transformations[0][2, 0], transformations[0][2, 1] = M[0, 0], M[1, 0]
            transformations[1][2, 0], transformations[1][2, 1] = M[0, 1], M[1, 1]
        else:
            transformations[2][0, 0] = 1 / T_SPEED
            transformations[2][1, 1] = 1 / T_SPEED
            transformations[0][2, 0], transformations[0][2, 1] = -M[0, 0], -M[1, 0]
            transformations[1][2, 0], transformations[1][2, 1] = -M[0, 1], -M[1, 1]
        
        time.sleep(0.3)
        
    remove_shape(diamond)

diamond_points = np.array([
    [CENTER[0], CENTER[1] - 50],
    [CENTER[0] + 25, CENTER[1]],
    [CENTER[0], CENTER[1] + 50],
    [CENTER[0] - 25, CENTER[1]],
])

win = gr.GraphWin("Diamond", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground('light blue')

diamond1 = None
diamond2 = None

apply_transformations(diamond_points, [M1, R, T], diamond1)
apply_transformations(diamond_points, [M2, T, R], diamond2)

win.getMouse()
win.close()
