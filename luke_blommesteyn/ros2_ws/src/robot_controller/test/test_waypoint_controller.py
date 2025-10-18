import math

from robot_controller.waypoint_controller import shortest_angular_distance


def test_shortest_angular_distance_wraps_positive():
    current = math.radians(10.0)
    target = math.radians(190.0)
    error = shortest_angular_distance(current, target)
    assert math.isclose(error, math.radians(180.0), abs_tol=1e-6)


def test_shortest_angular_distance_wraps_negative():
    current = math.radians(-170.0)
    target = math.radians(170.0)
    error = shortest_angular_distance(current, target)
    assert math.isclose(error, math.radians(-20.0), abs_tol=1e-6)


def test_shortest_angular_distance_small_delta():
    current = math.radians(45.0)
    target = math.radians(60.0)
    error = shortest_angular_distance(current, target)
    assert math.isclose(error, math.radians(15.0), abs_tol=1e-6)
