import time
from typing import NamedTuple

start_time = time.time()

class Point(NamedTuple):
    x: int
    y: int


def manhattan_distance_from_origin(point: Point) -> int:
    return abs(point.x) + abs(point.y)



class Wire:
    def __init__(self) -> None:
        self.current_position = Point(0, 0)
        self.points = set()
    
    def add_points(self, segment: str) -> None:
        direction = segment[0]
        length = int(segment[1:])
        if direction == "U":
            for _ in range(length):
                _new_point = Point(self.current_position.x, self.current_position.y + 1)
                self.points.add(_new_point)
                self.current_position = _new_point
        elif direction == "D":
            for _ in range(length):
                _new_point = Point(self.current_position.x, self.current_position.y - 1)
                self.points.add(_new_point)
                self.current_position = _new_point
        elif direction == "R":
            for _ in range(length):
                _new_point = Point(self.current_position.x + 1, self.current_position.y)
                self.points.add(_new_point)
                self.current_position = _new_point
        elif direction == "L":
            for _ in range(length):
                _new_point = Point(self.current_position.x - 1, self.current_position.y)
                self.points.add(_new_point)
                self.current_position = _new_point
        else:
            raise ValueError("Invalid direction")



wire_segment_groups = []
# test1a = ["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
# test1b = ["U62","R66","U55","R34","D71","R55","D58","R83"]

with open("input3.txt") as f:
    for wire_segments in f:
        wire_segments = wire_segments.strip().split(",")
        wire_segment_groups.append(wire_segments)


wire1 = Wire()
for wire_segment in wire_segment_groups[0]:
    wire1.add_points(wire_segment)

wire2 = Wire()
for wire_segment in wire_segment_groups[1]:
    wire2.add_points(wire_segment)

common_points = wire1.points.intersection(wire2.points)
common_point_distances_from_origin = []
for point in common_points:
    distance = manhattan_distance_from_origin(point)
    common_point_distances_from_origin.append(distance)

print(min(common_point_distances_from_origin))

end_time = time.time()

print(end_time - start_time)
