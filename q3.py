import time
from typing import NamedTuple, Dict, Tuple


class Point(NamedTuple):
    x: int
    y: int


def manhattan_distance_from_origin(point: Point) -> int:
    return abs(point.x) + abs(point.y)


class Wire:
    def __init__(self) -> None:
        self.current_position = Point(0, 0)
        self.points: Dict[Point, int] = dict()
        self.num_steps: int = 0
        self.directional_offsets: Dict[str, Tuple] = {
            "U": (0, 1),
            "D": (0, -1),
            "R": (1, 0),
            "L": (-1, 0),
        }

    def add_points(self, segment: str) -> None:
        # Direction information is in the first position (e.g. "R421")
        direction = segment[0]
        # Get x and y offsets for that direction
        x_off, y_off = self.directional_offsets[direction]
        length = int(segment[1:])
        for _ in range(length):
            self.num_steps += 1
            new_point = Point(
                self.current_position.x + x_off, self.current_position.y + y_off
            )
            # If point already exists, don't re-add it as we only care about
            # the shortest path to a given point
            if new_point not in self.points:
                self.points[new_point] = self.num_steps
            self.current_position = new_point


def solve2(wire_segments: list[list[str]]) -> int:
    wire1 = Wire()
    for wire_segment in wire_segments[0]:
        wire1.add_points(wire_segment)

    wire2 = Wire()
    for wire_segment in wire_segments[1]:
        wire2.add_points(wire_segment)

    common_points = set(wire1.points.keys()).intersection(set(wire2.points.keys()))
    signal_delays = []
    for point in common_points:
        sig_delay_1 = wire1.points[point]
        sig_delay_2 = wire2.points[point]
        sig_delay = sig_delay_1 + sig_delay_2
        signal_delays.append(sig_delay)

    return min(signal_delays)


def main() -> None:
    start_time = time.time()
    wire_segment_list: list[list[str]] = []

    with open("input3.txt") as f:
        for line in f:
            wire_segments: list[str] = line.strip().split(",")
            wire_segment_list.append(wire_segments)

    ans2 = solve2(wire_segment_list)
    print(ans2)

    end_time = time.time()
    print(end_time - start_time)


if __name__ == "__main__":
    main()
