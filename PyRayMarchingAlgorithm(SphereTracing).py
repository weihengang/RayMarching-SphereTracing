import turtle as t
import math as m
tscreen = t.Screen()
tscreen.bgcolor("black")
tscreen.tracer(0)
t.colormode(255)
t.hideturtle()
t.color("white")
tscreen.screensize(10000, 10000)
render = t.Turtle()
render.up()
render.hideturtle()
original_x = -700
original_y = 0
mode = "change_point"
class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    def render(self, color):
        turtle = t
        if (color == (255, 255, 255)):
            turtle = render
        turtle.up()
        turtle.color(color)
        turtle.goto(self.x, self.y)
        turtle.dot(5, color)
        turtle.sety(self.y - self.r)
        turtle.down()
        turtle.circle(self.r, 360)
    def __repr__(self):
        return f"({self.x}, {self.y}) | {self.r}"
class Ray:
    def __init__(self, vector_x, vector_y, origin_x, origin_y):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.unit_x, self.unit_y = Ray.calculate_unit(vector_x, vector_y)
    @staticmethod
    def calculate_unit(vector_x, vector_y):
        magnitude = m.sqrt(pow(vector_x, 2) + pow(vector_y, 2))
        return (vector_x / magnitude, vector_y / magnitude)
    def ray_up(self):
        self.unit_x, self.unit_y = Ray.calculate_unit(self.unit_x, self.unit_y + 0.05)
    def ray_down(self):
        self.unit_x, self.unit_y = Ray.calculate_unit(self.unit_x, self.unit_y - 0.05)
    def __repr__(self):
        return f"({self.unit_x}, {self.unit_y}) | ({self.origin_x}, {self.origin_y})"
ray = Ray(1, 0, -700, 0)
list_Circle = [Circle(300, -250, 200), Circle(-500, 250, 50), Circle(-300, -300, 150), Circle(0, 200, 100), Circle(600, 250, 100)]
for i in list_Circle:
    i.render((255, 255, 255))
tscreen.update()
def change_mode():
    global mode
    if (mode == "change_ray"):
        mode = "change_point"
        return
    mode = "change_ray"
def find_closest(point):
    assert type(point) == Ray
    closest_distance = 1000000
    for i in list_Circle:
        distance = m.sqrt(pow(point.origin_x - i.x, 2) + pow(point.origin_y - i.y, 2))
        true_distance = distance - i.r
        if (true_distance < closest_distance):
            closest_distance = true_distance
    return closest_distance
def generate_points(point_ray, list_points):
    assert type(point_ray) == Ray
    distance = find_closest(point_ray)
    list_points.append(Circle(point_ray.origin_x, point_ray.origin_y, distance))
    x = point_ray.origin_x + point_ray.unit_x * distance
    y = point_ray.origin_y + point_ray.unit_y * distance
    point_ray.origin_x = x; point_ray.origin_y = y
    if (distance < 1):
        return (list_points, (0, 255, 0))
    if (distance > 1000):
        return (list_points, (255, 0, 0))
    return generate_points(point_ray, list_points)
def screen_onclick(x, y):
    global original_x, original_y, ray
    t.clear()
    if (mode == "change_ray"):
        new_ray = Ray(ray.unit_x, ray.unit_y, x, y)
        original_x = x
        original_y = y
    else:
        new_ray = Ray(x - original_x, y - original_y, original_x, original_y)
        ray = new_ray
    #new_ray.render()
    points, color = generate_points(new_ray, [])
    if (len(points) == 1):
        color = (0, 0, 255)
    for i in points:
        i.render(color)
    t.color(color)
    t.up()
    t.goto(original_x, original_y)
    t.down()
    last_point = points[len(points) - 1]
    t.goto(last_point.x, last_point.y)
    tscreen.update()
tscreen.onkey(change_mode, "space")
tscreen.listen()
tscreen.onclick(screen_onclick)
tscreen.mainloop()