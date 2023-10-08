import math
import random

import pytest

from symmetry import Point, find_symmetry_lines

# Expected error messages
EXPECTED_INPUT_LENGTH_MESSAGE = "Please provide at least two points"
EXPECTED_LIST_ERROR = "points must be a list"
EXPECTED_ITEM_ERROR = "Each item in the points list must be an instance of Point"


def generate_large_input(num_points: int, symmetric: bool = True) -> list[Point]:
    """
    Generate a set of points. If symmetric is True, half of the points are generated in the
    positive quadrant (first quadrant) and the other half are their symmetric counterparts in
    the negative quadrant (third quadrant). If symmetric is False, all points are generated in
    the positive quadrant.

    :param num_points: Total number of points to be generated.
    :param symmetric: Flag to determine if generated points should be symmetric. Defaults to True.
    :return: A list of generated points.
    """
    half_num_points = num_points // 2

    if symmetric:
        points = [Point(i, i) for i in range(half_num_points)]
        points.extend([Point(-i, -i) for i in range(half_num_points)])
        return points
    else:
        return [
            Point(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(num_points)
        ]


@pytest.mark.parametrize("input_points", [[], [Point(1, 1)]])
def test_num_points_conditions(input_points):
    with pytest.raises(ValueError, match=EXPECTED_INPUT_LENGTH_MESSAGE):
        find_symmetry_lines(input_points)


@pytest.mark.parametrize(
    "input_points, expected_error",
    [
        (tuple([Point(1, 1), Point(2, 2)]), EXPECTED_LIST_ERROR),  # tuple instead of list
        ({Point(1, 1), Point(2, 2)}, EXPECTED_LIST_ERROR),  # set instead of list
        ("string", EXPECTED_LIST_ERROR),  # string instead of list
        ([Point(1, 1), "not_a_point"], EXPECTED_ITEM_ERROR),  # one item is not a Point
        ([1, 2, 3], EXPECTED_ITEM_ERROR),  # none of the items are Points
    ],
)
def test_input_type_conditions(input_points, expected_error):
    with pytest.raises(TypeError, match=expected_error):
        find_symmetry_lines(input_points)


def test_exceed_max_points():
    points = generate_large_input(
        101, False
    )  # Generate 101 points which is above the limit
    print(len(points))
    with pytest.raises(
        ValueError, match="Algorithm is not optimized to run with more than 100 points"
    ):
        find_symmetry_lines(points)


@pytest.mark.parametrize(
    "points, expected, shape",
    [
        ([Point(0, 2), Point(-1, 0), Point(0, -2), Point(1, 0)], 2, "Rhombus"),
        ([Point(1, 1), Point(-1, 1), Point(1, -1), Point(-1, -1)], 4, "Square"),
        ([Point(0, 2), Point(-1, 0), Point(0, -1), Point(1, 0)], 1, "Kite"),
        ([Point(-2, 1), Point(2, 1), Point(1, -1), Point(-1, -1)], 1,"Isosceles Trapezoid",),
        ([Point(-2, 1), Point(2, 1), Point(1.5, -1), Point(-1.5, -1)], 1, "Trapezoid"),
        ([Point(2, 1), Point(0, 2), Point(-2, -1), Point(0, -2)], 0, "Parallelogram"),
        ([Point(0, math.sqrt(3)), Point(-1, 0), Point(1, -0)], 3, "Equilateral Triangle",),
        ([Point(0, 2), Point(-1, 0), Point(1, 0)], 1, "Isosceles Triangle"),
    ],
)
def test_symmetry_of_shapes(points, expected, shape):
    lines = find_symmetry_lines(points)
    assert (
        len(lines) == expected
    ), f"{shape} - Expected lines: {expected}, Actual: {len(lines)}"


@pytest.mark.parametrize(
    "num_points, symmetric, expected_lines",
    [
        (30, True, 1),
        (60, True, 1),
        (100, True, 1),
        (30, False, 0),
        (60, False, 0),
        (100, False, 0),
    ],
)
def test_large_input(num_points, symmetric, expected_lines):
    points = generate_large_input(num_points, symmetric)
    result = len(find_symmetry_lines(points))
    assert (
        result == expected_lines
    ), f"Expected {expected_lines} lines of symmetry for {num_points} points, but got {result}."


def test_collinear_points():
    collinear_points = [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)]
    expected_lines = 1
    lines = find_symmetry_lines(collinear_points)
    assert len(lines) == expected_lines
