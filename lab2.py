import time
import numpy as np
from graphics import GraphWin, Polygon, Point

WINDOW_WEIGHT = 600
WINDOW_HEIGHT = 600
CENTER = np.array((WINDOW_WEIGHT // 2, WINDOW_HEIGHT // 2))

TETA = 0.5

# матрицы поворота для оси X
Tx = np.array([
    [1, 0, 0, 0],
    [0, np.cos(TETA), np.sin(TETA), 0],
    [0, -np.sin(TETA), np.cos(TETA), 0],
    [0, 0, 0, 1],
])

# матрицы поворота для оси Y
Ty = np.array([
    [np.cos(TETA), 0, -np.sin(TETA), 0],
    [0, 1, 0, 0],
    [np.sin(TETA), 0, np.cos(TETA), 0],
    [0, 0, 0, 1],
])

# матрица поворота для оси Z
Tz = np.array([
    [np.cos(TETA), np.sin(TETA), 0, 0],
    [-np.sin(TETA), np.cos(TETA), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])

win = GraphWin("Triangle pyramid", WINDOW_WEIGHT, WINDOW_HEIGHT)
win.setBackground('white')

def remove_pyramid(pyramid):
    for p in pyramid:
        p.setOutline("white")
        p.undraw()


def create_polygons(points):
    polygons_points = [
        [points[0], points[1], points[2]],
        [points[0], points[1], points[3]],
        [points[0], points[3], points[2]],
        [points[1], points[2], points[3]],
    ]
    return [Polygon(*[Point(int(x), int(y)) for (x, y, _, _) in p_points])
            for p_points in polygons_points]


def redraw_pyramid(points, pyramid, colors):
    if pyramid:
        remove_pyramid(pyramid)

    polygons = create_polygons(points)
    for polygon, color in zip(polygons, colors):
        polygon.setFill(color)
        polygon.draw(win)
    return polygons


pyramid_points = np.array([
    [0, 0, 0, 1],
    [100, 0, 0, 1],
    [50, 100, 0, 1],
    [50, 50, 100, 1],
])

vectors = [
    np.array([0, 0, 0, 0]),
    np.array([100, 0, 0, 0]),
    np.array([100, 100, 0, 0]),
    np.array([0, 100, 0, 0]),
]

colors = [
    ["#F3C300", "#875692", "#F38400", "#A1CAF1"],
    ["#BE0032", "#C2B280", "#848482", "#008856"],
    ["#E68FAC", "#0067A5", "#F99379", "#604E97"],
    ["#F6A600", "#B3446C", "#DCD300", "#882D17"],
]


pyramid = redraw_pyramid(pyramid_points, None, colors[0])

for i, vector in enumerate(vectors):
    pyramid_points = pyramid_points @ Tx
    pyramid_points = pyramid_points @ Ty
    pyramid_points = pyramid_points @ Tz
    pyramid_points = pyramid_points + vector
    pyramid = redraw_pyramid(pyramid_points, pyramid, colors[i])
    
    win.getMouse()
        
win.close()
