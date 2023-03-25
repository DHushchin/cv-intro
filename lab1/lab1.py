import time
import numpy as np
from graphics import GraphWin, Polygon, Point

WINDOW_WEIGHT = 600
WINDOW_HEIGHT = 600
CENTER = np.array((WINDOW_WEIGHT // 2, WINDOW_HEIGHT // 2))

ONES = np.array([
    [1],
    [1],
    [1],
])

TETA = 3

R = np.array([
    [np.cos(TETA), np.sin(TETA), 0],
    [-np.sin(TETA), np.cos(TETA), 0],
    [0, 0, 1],
])

T = np.array([
    [1.05, 0, 0],
    [0, 1.05, 0],
    [0, 0, 1],
])

m = np.array([5, 10])

M = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [m[0], m[1], 1],
])

T_speed = 1.05

win = GraphWin("Triangle", WINDOW_WEIGHT, WINDOW_HEIGHT)
win.setBackground('light blue')


def remove_triangle(triangle):
    triangle.setFill("light blue")


def redraw_triangle(points, triangle):
    if triangle:
        remove_triangle(triangle)
    triangle = Polygon(*[Point(int(x), int(y)) for (x, y) in points])
    triangle.setFill('orange')
    triangle.draw(win)
    return triangle


def triangle_center(points):
    return np.array(((points[0][0] + points[1][0] + points[2][0]) / 3,
                     (points[0][1] + points[1][1] + points[2][1]) / 3))


def transform(points, A):
    P = np.concatenate(
        (points - triangle_center(points), ONES),
        axis=1
    )
    P_stroke = P @ A
    return P_stroke[:, :2] + triangle_center(points)


def compositional_transformations(triangle_points):
    triangle = None
    for i in range(100):
        triangle_points = transform(triangle_points, (R @ T @ M))
        triangle = redraw_triangle(triangle_points, triangle)

        # -----------Change direction-----------
        if (i // 20) % 2 == 0:
            T[0, 0], T[1, 1] = T_speed, T_speed
            M[2, 0], M[2, 1] = m[0], m[1]
        else:
            T[0, 0], T[1, 1] = 1 / T_speed, 1 / T_speed
            M[2, 0], M[2, 1] = -m[0], -m[1]
        time.sleep(0.3)
    remove_triangle(triangle)


def consecutive_transformations(triangle_points):
    triangle = None
    for i in range(100):
        triangle_points = transform(triangle_points, M)
        triangle_points = transform(triangle_points, R)
        triangle_points = transform(triangle_points, T)

        triangle = redraw_triangle(triangle_points, triangle)

        # -----------Change direction-----------
        if (i // 20) % 2 == 0:
            T[0, 0], T[1, 1] = T_speed, T_speed
            M[2, 0], M[2, 1] = m[0], m[1]
        else:
            T[0, 0], T[1, 1] = 1 / T_speed, 1 / T_speed
            M[2, 0], M[2, 1] = -m[0], -m[1]
        time.sleep(0.3)
        
    remove_triangle(triangle)
    

def main():
    triangle_points = np.array([
        [100, 100],
        [200, 100],
        [150, 200],
    ])

    compositional_transformations(triangle_points)
    consecutive_transformations(triangle_points)

    win.getMouse()
    win.close()
    
    
if __name__ == '__main__':
    main()