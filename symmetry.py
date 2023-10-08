
PRECISION = .001

class Point:
    """
    Represents a 2D point with x and y coordinates.

    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def find_symmetry_lines(points: list[Point]) -> set[tuple[float, float]]:
    # Check if points is a list
    if not isinstance(points, list):
        raise TypeError("points must be a list")

    # Check if every item in points is an instance of Point
    for point in points:
        if not isinstance(point, Point):
            raise TypeError("Each item in the points list must be an instance of Point")

    points = list(set(points))

    num_points = len(points)
    if num_points <= 1 or not num_points:
        raise ValueError('Please provide at least two points')
    elif num_points > 100:
        raise ValueError('Algorithm is not optimized to run with more than 100 points')

    def midpoint(p1, p2):
        return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)

    def slope(p1, p2):
        if p2.x - p1.x == 0:  # vertical line
            return float('inf')
        return (p2.y - p1.y) / (p2.x - p1.x)

    def perpendicular_bisector(p1: Point, p2: Point) -> tuple[float, float]:
        m = slope(p1, p2)
        mid = midpoint(p1, p2)

        if m == 0:  # horizontal line
            return (float('inf'), mid.x)
        if m == float('inf'):  # vertical line
            return (0, mid.y)

        m_perpendicular = -1 / m
        c = mid.y - m_perpendicular * mid.x

        return (m_perpendicular, c)

    def are_collinear(points: list[Point]) -> bool:
        if len(points) <= 2:
            return True
        m = slope(points[0], points[1])
        for i in range(2, len(points)):
            if slope(points[0], points[i]) != m:
                return False
        return True

    # If all the points are collinear, return the perpendicular bisector 
    # of the line formed by the first and last points as the only line of symmetry.
    if are_collinear(points):
        return {perpendicular_bisector(points[0], points[-1])}

    potential_bisectors = set()

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            bisector = perpendicular_bisector(points[i], points[j])
            potential_bisectors.add(bisector)

    def is_close(p1: Point, p2: Point, tol=PRECISION) -> bool:
        return abs(p1.x - p2.x) < tol and abs(p1.y - p2.y) < tol
    
    def reflect_point(m: float, c: float, p: Point) -> Point:
        # For vertical lines (infinite slope):
        if m == float('inf'):
            # The x value of the reflected point will be symmetrically opposite
            # with respect to the line's x-intercept, which is the value 'c' here.
            x_reflected = 2*c - p.x
            return Point(x_reflected, p.y)
        
        A = m
        B = -1
        C = c
        
        x_prime = p.x - 2 * A * (A * p.x + B * p.y + C) / (A**2 + B**2)
        y_prime = p.y - 2 * B * (A * p.x + B * p.y + C) / (A**2 + B**2)
        
        return Point(x_prime, y_prime)

    # TODO(Stan): This should be optimized to avoid the present O(n^2) runtime
    def is_symmetry_line(m: float, c: float, points: list[Point]) -> bool:
        for p in points:
            reflected = reflect_point(m, c, p)
            if not any(is_close(reflected, orig) for orig in points):
                return False
        return True

    symmetry_lines = set()

    for m, c in potential_bisectors:
        if is_symmetry_line(m, c, points):
            symmetry_lines.add((m, c))

    return symmetry_lines
