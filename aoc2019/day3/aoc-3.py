class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __add__(self, other):
        if type(other) == Point:
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("can't add type '{0}' to point".format(type(other)))

    def __sub__(self, other):
        if type(other) == Point:
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("can't subtract type '{0}' from point".format(type(other)))

    def __mul__(self, other):
        if type(other) == Point:
            return Point(self.x * other.x, self.y * other.y)
        elif type(other) == int or type(other) == float:
            return Point(self.x * other, self.y * other)
        else:
            raise TypeError("can't multiply type '{0}' by point".format(type(other)))

    def __truediv__(self, other):
        if type(other) == Point:
            return Point(self.x / other.x, self.y / other.y)
        elif type(other) == int:
            return Point(self.x / other, self.y / other)
        else:
            raise TypeError("can't divide type '{0}' by point".format(type(other)))

    def __eq__(self, other):
        if type(other) == Point:
            return self.x == other.x and self.y == other.y
        return False


def parse_movement_instructions(movements):
    """ return list of points of wire vertices from string input """
    movements = movements.split(',')
    vertices = []
    x = y = 0  # start at (0, 0)
    vertices.append(Point(x, y))  # include start point
    for m in movements:
        x, y = move_coords_this_much(x, y, m)
        vertices.append(Point(x, y))
    return vertices


def move_coords_this_much(x, y, mvmt):
    """ moves a point that much, movement as string (eg L15) """
    direction = mvmt[0].upper()
    amount = int(mvmt[1:])
    if direction == 'L':
        x -= amount
    elif direction == 'R':
        x += amount
    elif direction == 'U':
        y += amount
    elif direction == 'D':
        y -= amount
    else:
        raise ValueError("invalid movement direction: '{0}'".format(direction))
    return x, y


def find_point_of_intersection(seg1, seg2):
    """ return point of intersection of segments, None if no intersection or lines are collinear """
    p1, p2 = seg1
    p3, p4 = seg2
    ta = calc_ta(p1, p2, p3, p4)  # offset of the intersection in first line (starting from p1)
    tb = calc_tb(p1, p2, p3, p4)  # offset of the intersection in second line (starting from p3)
    if ta is None or tb is None:  # collinear
        poi = None
    elif 0 <= ta <= 1 and 0 <= tb <= 1:  # intersect! find where
        poi = p1 + ((p2 - p1) * ta)
    else:  # don't intersect anywhere
        poi = None
    return poi


def calc_ta(p1, p2, p3, p4):
    numerator = ((p3.y - p4.y) * (p1.x - p3.x)) + ((p4.x - p3.x) * (p1.y - p3.y))
    denominator = ((p4.x - p3.x) * (p1.y - p2.y)) - ((p1.x - p2.x) * (p4.y - p3.y))
    if denominator == 0:
        return None  # collinear
    return numerator / denominator


def calc_tb(p1, p2, p3, p4):
    numerator = ((p1.y - p2.y) * (p1.x - p3.x)) + ((p2.x - p1.x) * (p1.y - p3.y))
    denominator = ((p4.x - p3.x) * (p1.y - p2.y)) - ((p1.x - p2.x) * (p4.y - p3.y))
    if denominator == 0:
        return None  # collinear
    return numerator / denominator


def calculate_manhattan_distance(p1, p2):
    """ return int man dist between p1 and p2 """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def do_pt1(wire1, wire2):
    """ return manhattan distance of intersection closest to start point """
    intersections = []  # list of points of intersection
    wire1 = parse_movement_instructions(wire1)
    wire2 = parse_movement_instructions(wire2)
    for c1 in range(1, len(wire1) - 1):  # cursor for wire1: start at second segment ([1] -> [2]), cause first one ([0] -> [1]) will always 'intersect' at the start point (0,0)
        for c2 in range(1, len(wire2) - 1):  # cursor for wire2
            segment1 = (wire1[c1], wire1[c1 + 1])  # a line segments is two adjacent points
            segment2 = (wire2[c2], wire2[c2 + 1])
            poi = find_point_of_intersection(segment1, segment2)
            if poi is not None:
                intersections.append(poi)
    return min([calculate_manhattan_distance(Point(0,0), i) for i in intersections])


def do_pt2(wire1, wire2):
    """ return fewest combined steps of both wires to an intersection """
    steps_to_intersections = []  # list of combined steps to get to an intersection
    wire1 = parse_movement_instructions(wire1)
    wire2 = parse_movement_instructions(wire2)
    step1 = step2 = 0  # current length of each wire
    for c1 in range(0, len(wire1) - 1):  # cursor for wire1: start at first segment to accurately record number of steps
        segment1 = (wire1[c1], wire1[c1 + 1])  # just a tuple of two adjacent points
        for c2 in range(0, len(wire2) - 1):  # cursor for wire2
            segment2 = (wire2[c2], wire2[c2 + 1])
            poi = find_point_of_intersection(segment1, segment2)
            if poi is not None and poi != Point(0, 0):
                partial_step1 = calculate_manhattan_distance(segment1[0], poi)  # want to note the steps from the start of that segment to the point of intersection
                partial_step2 = calculate_manhattan_distance(segment2[0], poi)
                steps_to_intersections.append(step1 + partial_step1 + step2 + partial_step2)
            step2 += calculate_manhattan_distance(*segment2)  # calculate step count after checking for poi cause it only matters for the next line segment
        step1 += calculate_manhattan_distance(*segment1)
        step2 = 0  # reset cause we're starting from another seg from wire 1
    return min(steps_to_intersections)  # fewest steps


def test_pt1():
    print(do_pt1('R8,U5,L5,D3', 'U7,R6,D4,L4') == 6)
    print(do_pt1('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 159)
    print(do_pt1('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135)


def test_pt2():
    print(do_pt2('R8,U5,L5,D3', 'U7,R6,D4,L4') == 30)
    print(do_pt2('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 610)
    print(do_pt2('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 410)


if __name__ == '__main__':
    with open('input') as f:
        wire1 = f.readline().strip()
        wire2 = f.readline().strip()
    print(do_pt2(wire1, wire2))
