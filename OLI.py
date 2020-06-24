import numpy as np
import turtle


def calc_intersection(x, x_1, y_1, x_2, y_2, x__1, y__1, x__2, y__2):

    if x_1 != x_2:
        y = (((y_2 - y_1) * (x - x_1)) / (x_2 - x_1)) + y_1

        if x == x__1:
            return True, int(y)
        else:
            return False, 0

    if x__1 != x__2:
        y = (((y__2 - y__1) * (x - x__1)) / (x__2 - x__1)) + y__1

        if x == x_1:
            return True, int(y)
        else:
            return False, 0

    return False, 0


def draw_lines():

    vertical = []
    for i in range(25):

        x = np.random.randint(-300, 300 + 1)

        y1 = -350
        while y1 <= -330:
            y1 = np.random.randint(-300, 300 + 1)

        y2 = 350
        while y2 >= 330:
            y2 = np.random.randint(-300, 300 + 1)

        if y1 <= y2:
            vertical.append((x, y1, x, y2))
        else:
            vertical.append((x, y2, x, y1))

    horizontal = []
    for i in range(25):
        x1 = -350
        while x1 <= -330:
            x1 = np.random.randint(-300, 300 + 1)

        x2 = 350
        while x2 >= 330:
            x2 = np.random.randint(-300, 300 + 1)

        y = np.random.randint(-300, 300 + 1)

        if x1 <= x2:
            horizontal.append((x1, y, x2, y))
        else:
            horizontal.append((x2, y, x1, y))

    lst = vertical + horizontal

    bob.color("red")
    for x1, y1, x2, y2 in horizontal:
        bob.penup()
        bob.goto(x1, y1)
        bob.pendown()
        bob.goto(x2, y2)

    bob.color('blue')
    for x1, y1, x2, y2 in vertical:
        bob.penup()
        bob.goto(x1, y1)
        bob.pendown()
        bob.goto(x2, y2)

    return lst


def orth_line_inter(lst: list):

    bob.color('green')

    AS = []

    lst.sort(key=lambda x: x[0])

    x = lst[0][0]

    while x != 350:

        for x1, y1, x2, y2 in lst:

            if (x1 <= x and x <= x2):
                if (x1, y1, x2, y2) not in AS:
                    AS.append((x1, y1, x2, y2))

            else:
                if (x1, y1, x2, y2) in AS:
                    AS.remove((x1, y1, x2, y2))

        if len(AS) >= 1:

            for x_1, y_1, x_2, y_2 in AS:
                for x__1, y__1, x__2, y__2 in AS:

                    # if not the same segments.
                    if (x_1, y_1, x_2, y_2) != (x__1, y__1, x__2, y__2):

                        # check if intersecting segments
                        if (y_1 >= y__1 and y_2 <= y__2):

                            boolean, y = calc_intersection(
                                x, x_1, y_1, x_2, y_2, x__1, y__1, x__2, y__2)

                            if boolean:
                                bob.penup()
                                bob.goto(x, y)
                                bob.dot()
                                bob.pendown()

        x += 1


window = turtle.Screen()
window.title("Orthogonal Line Intersection")

bob = turtle.Turtle()
bob.shape('circle')
bob.resizemode("user")
bob.shapesize(0.2, 0.2, 1)
bob.speed(0)

lst = draw_lines()

orth_line_inter(lst)
print('done')

bob.hideturtle()
turtle.done()
