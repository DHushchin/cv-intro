import matplotlib.colors as colors
import numpy as np
from graphics import GraphWin, Point, Polygon

WINDOW_WEIGHT = 600
WINDOW_HEIGHT = 600

CANTOR_MAX_LEVEL = 4
KOCH_MAX_LEVEL = 4

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


def draw_koch(p1, p2, level=0):
    if level >= KOCH_MAX_LEVEL:
        draw_line_pixel_color(p1[0], p1[1], p2[0], p2[1], (0, 0, 1))
        return

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    angle = np.pi / 3
    x = p1[0] + dx / 3
    y = p1[1] + dy / 3
    p = np.array([x, y])

    x = p1[0] + 2 * dx / 3
    y = p1[1] + 2 * dy / 3
    q = np.array([x, y])

    x = p[0] + (q[0] - p[0]) * np.cos(angle) - (q[1] - p[1]) * np.sin(angle)
    y = p[1] + (q[0] - p[0]) * np.sin(angle) + (q[1] - p[1]) * np.cos(angle)
    r = np.array([x, y])

    draw_koch(p1, p, level + 1)
    draw_koch(p, r, level + 1)
    draw_koch(r, q, level + 1)
    draw_koch(q, p2, level + 1)

def draw_cantor(x, y, length, level=0):
    if level >= CANTOR_MAX_LEVEL:
        draw_line_pixel_color(x, y, x + length, y, (1, 0.5, 0))
        return

    draw_line_pixel_color(x, y, x + length, y, (1, 0.5, 0))

    y += 30

    new_length = length / 3

    draw_cantor(x, y, new_length, level + 1)
    draw_cantor(x + 2 * new_length, y, new_length, level + 1)


if __name__ == '__main__':
    vertices = np.array([
        [150, 150, 0, 1],
        [450, 150, 0, 1],
        [300, 450, 0, 1],
        [300, 300, 300, 1]
    ])

    edges_color = (1.0, 0, 0)

    win = GraphWin("Піраміда, Фрактал Коха, Фрактал Кантора", WINDOW_WEIGHT, WINDOW_HEIGHT)
    win.setBackground('white')

    triangular_pyramid_edges_points = draw_triangular_pyramid(triangular_pyramid_edges(vertices), edges_color)

    koch_p1 = np.array([100, 400])
    koch_p2 = np.array([500, 400])
    draw_koch(koch_p1, koch_p2)

    cantor_x = 100
    cantor_y = 500
    cantor_length = 400
    draw_cantor(cantor_x, cantor_y, cantor_length)

    win.getMouse()
    win.close()
