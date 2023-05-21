import time
import numpy as np
from graphics import GraphWin, Point, Polygon
import matplotlib.colors as colors

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CENTER = np.array((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

TETA = 0.5

Tx = np.array([
    [1, 0, 0, 0],
    [0, np.cos(TETA), np.sin(TETA), 0],
    [0, -np.sin(TETA), np.cos(TETA), 0],
    [0, 0, 0, 1],
])
Ty = np.array([
    [np.cos(TETA), 0, -np.sin(TETA), 0],
    [0, 1, 0, 0],
    [np.sin(TETA), 0, np.cos(TETA), 0],
    [0, 0, 0, 1],
])

win = GraphWin("Трьохкутна піраміда", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground('white')

def draw_line_pixel_color(x1, y1, x2, y2, rgb):
    red, green, blue = rgb
    dx = x2 - x1
    dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y = x1, y1
    error, t = el / 2, 0

    obj = Point(x, y)
    obj.setFill('' + colors.rgb2hex((red, green, blue)))
    obj.draw(win)

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1

        grad = 0.01
        red = red + grad if red < 0.99 else 1
        green = green + grad if green < 0.99 else 1
        blue = blue + grad if blue < 0.99 else 1

        obj = Point(x, y)
        col16 = colors.rgb2hex((red, green, blue))
        obj.setFill('' + col16)
        obj.draw(win)


def triangular_pyramid_edges(vertices):
    return [
        (vertices[0], vertices[1]),
        (vertices[1], vertices[2]),
        (vertices[2], vertices[0]),
        (vertices[0], vertices[3]),
        (vertices[1], vertices[3]),
        (vertices[2], vertices[3]),
    ]


def clear_window(window):
    polygon = Polygon(
        Point(0, 0),
        Point(0, WINDOW_HEIGHT),
        Point(WINDOW_WIDTH, WINDOW_HEIGHT),
        Point(WINDOW_WIDTH, 0)
    )
    polygon.setFill("white")
    polygon.draw(window)


def draw_triangular_pyramid(edges, color):
    for edge in edges:
        draw_line_pixel_color(edge[0][0], edge[0][1], edge[1][0], edge[1][1], color)


vertices = np.array([
    [0, 0, 0, 1],
    [0, 100, 0, 1],
    [100, 100, 0, 1],
    [50, 50, 200, 1],  # вершина піраміди
])

vectors = [
    [200, 200, 0],
    [200, 200, 0],
    [0, -300, 0],
    [-300, 100, 0],
]

edges_colors = [
    (1.0, 0, 0),
    (0, 1.0, 0),
    (0, 0, 1.0),
    (1.0, 1.0, 0),
]

pyramid_center = np.array([50, 50, 100, 0])

vertices = (vertices - pyramid_center) @ Tx + pyramid_center
vertices = (vertices - pyramid_center) @ Ty + pyramid_center

for (m, l, n), c in zip(vectors, edges_colors):
    A = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [m, l, n, 1],
    ])
    vertices = (vertices - pyramid_center) @ A + pyramid_center
    clear_window(win)
    draw_triangular_pyramid(triangular_pyramid_edges(vertices), c)
    time.sleep(2)

win.getMouse()
win.close()
