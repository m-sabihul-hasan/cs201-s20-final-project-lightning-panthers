import numpy as np
import turtle

window = turtle.Screen()
window.title("Orthoginal line segment")

vertical = []
for i in range(20):
    x = np.random.randint(-300, 300 + 1)
    
    y1 = -350
    while y1 <= -330:
        y1 = np.random.randint(-300, 300 + 1)
    
    y2 = 350
    while y2 >= 330:
        y2 = np.random.randint(-300, 300 + 1)

    vertical.append((x, y1, x, y2))

horizontal = []
for i in range(20):
    x1 = -350
    while x1 <= -330:
        x1 = np.random.randint(-300, 300 + 1)
    
    x2 = 350
    while x2 >= 330:
        x2 = np.random.randint(-300, 300 + 1)

    y = np.random.randint(-300, 300 + 1)

    horizontal.append((x1, y, x2, y))

lst = vertical + horizontal

bob = turtle.Turtle()
bob.shape('circle')
bob.resizemode("user")
bob.shapesize(0.2,0.2,1)
bob.speed(0)

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



bob.hideturtle()
turtle.done()
