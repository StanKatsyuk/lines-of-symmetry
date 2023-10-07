import pytest
from symmetry import Point, find_symmetry_lines


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
        return [Point(i, i) for i in range(num_points)]


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


@pytest.mark.parametrize("num_points, symmetric, expected_lines", [
    (30, True, 1),
    (60, True, 1),
    (100, True, 1),
    (30, False, 0),
    (60, False, 0),
    (100, False, 0),
])
def test_large_input(num_points, symmetric, expected_lines):
    points = generate_large_input(num_points, symmetric)
    result = len(find_symmetry_lines(points))
    assert result == expected_lines, f"Expected {expected_lines} lines of symmetry for {num_points} points, but got {result}."


def _test_symmetry(num_points, expected_lines):
    points = generate_large_input(num_points, symmetric=(expected_lines > 0))
    result = len(find_symmetry_lines(points))
    assert result == expected_lines, f"Expected {expected_lines} lines of symmetry for {num_points} points, but got {result}."


def test_exceed_max_points():
    points = generate_large_input(101, False)  # Generate 101 points which is above the limit
    print(len(points))
    with pytest.raises(ValueError, match='Algorithm is not optimized to run with more than 100 points'):
        find_symmetry_lines(points)
