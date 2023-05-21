import matplotlib.colors as colors
import numpy as np

from graphics import GraphWin, Point, Polygon

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

    edge_points = [(x, y)]
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

        edge_points.append((x, y))
        obj = Point(x, y)
        col16 = colors.rgb2hex((red, green, blue))
        obj.setFill('' + col16)
        obj.draw(win)
    return np.array(edge_points)


def triangular_pyramid_edges(vertices):
    return [
        (vertices[0], vertices[1]),
        (vertices[1], vertices[2]),
        (vertices[2], vertices[0]),
        (vertices[0], vertices[3]),
        (vertices[1], vertices[3]),
        (vertices[2], vertices[3]),
    ]


def draw_triangular_pyramid(edges, color):
    edges_points = []
    for edge in edges:
        edge_points = draw_line_pixel_color(edge[0][0], edge[0][1],
                                            edge[1][0], edge[1][1], color)
        edges_points.append(edge_points)
    return edges_points


def mnk(edges_points):
    for edge_points in edges_points:
        t = len(edge_points)
        stopt = t

        Yin = np.zeros((stopt, 1))
        F = np.ones((stopt, 2))
        FX = np.ones((stopt, 2))

        for i in range(len(edge_points)):
            Yin[i, 0] = float(edge_points[i][1])
            F[i, 1] = float(edge_points[i][0])
            FX[i, 1] = float(edge_points[i][0])

        for i in range(0, stopt):
            F[i, 1] = i

        FT = F.T
        FFT = FT.dot(F)
        FFTI = np.linalg.inv(FFT)
        FFTIFT = FFTI.dot(FT)
        C = FFTIFT.dot(Yin)
        Yout = F.dot(C)

        for i in range(0, stopt):
            XMNK = FX[i, 1]
            YMNK = Yout[i, 0]
            obj = Point(XMNK, YMNK)
            obj.setFill('violet')
            obj.draw(win)


vertices = np.array([
    [0, 0, 0, 1],
    [0, 100, 0, 1],
    [100, 100, 0, 1],
    [50, 50, 200, 1],  # вершина піраміди
])

vector = [200, 200, 0]

edges_color = (1.0, 0, 0)

pyramid_center = np.array([50, 50, 100, 0])

vertices = (vertices - pyramid_center) @ Tx + pyramid_center
vertices = (vertices - pyramid_center) @ Ty + pyramid_center

(m, l, n), c = vector, edges_color
A = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [m, l, n, 1],
])
vertices = (vertices - pyramid_center) @ A + pyramid_center

win = GraphWin("Растрова трікутна піраміда", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground('white')
edges_points = draw_triangular_pyramid(triangular_pyramid_edges(vertices), c)
win.getMouse()
win.close()

win = GraphWin("Векторний паралелепіпед за МНК", WINDOW_WIDTH, WINDOW_HEIGHT)
win.setBackground('white')
mnk(edges_points)
win.getMouse()
win.close()
