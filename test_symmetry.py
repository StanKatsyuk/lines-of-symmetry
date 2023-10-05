import pytest
from symmetry import Point, find_symmetry_lines


def generate_large_input(num_points: int, symmetric: bool = True) -> list[Point]:
    """Generate a large input set of points."""
    points = [Point(i, i) for i in range(num_points)]
    if symmetric:
        points.extend([Point(-i, -i) for i in range(num_points)])
    return points


@pytest.mark.parametrize("points, expected, shape", [
    ([Point(0, 2), Point(-1, 0), Point(0, -2), Point(1, 0)], 2, 'Rhombus'),
    ([Point(1, 1), Point(-1, 1), Point(1, -1), Point(-1, -1)], 4, 'Square'),
    ([Point(0, 2), Point(-1, 0), Point(0, -1), Point(1, 0)], 1, 'Kite'),
    ([Point(-2, 1), Point(2, 1), Point(1, -1), Point(-1, -1)], 1, 'Isosceles Trapezoid'),
    ([Point(-2, 1), Point(2, 1), Point(1.5, -1), Point(-1.5, -1)], 0, 'Trapezoid'),
    ([Point(2, 1), Point(0, 2), Point(-2, -1), Point(0, -2)], 0, 'Parallelogram'),
    ([Point(0, 1.73), Point(-1, -0.87), Point(1, -0.87)], 3, 'Equilateral Triangle'),
    ([Point(0, 2), Point(-1, 0), Point(1, 0)], 1, 'Isosceles Triangle')
])
def test_symmetry_of_shapes(points, expected, shape):
    lines = find_symmetry_lines(points)
    assert len(lines) == expected, f"{shape} - lines expected: {expected} actual: {len(lines)}"


@pytest.mark.parametrize("num_points", [30, 60, 100])
def test_large_input_symmetric(num_points):
    _test_symmetry(num_points, expected_lines=1)


@pytest.mark.parametrize("num_points", [30, 60, 100])
def test_large_input_non_symmetric(num_points):
    _test_symmetry(num_points, expected_lines=0)


def _test_symmetry(num_points, expected_lines):
    points = generate_large_input(num_points, symmetric=(expected_lines > 0))
    result = len(find_symmetry_lines(points))
    assert result == expected_lines, f"Expected {expected_lines} lines of symmetry for {num_points} points, but got {result}."
