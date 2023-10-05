

PRECISION = .001

class Point:
    """
    Represents a 2D point with x and y coordinates.

    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.

    Methods:
        __eq__(self, other: 'Point') -> bool:
            Checks if this point is equal to another point.

        __hash__(self) -> int:
            Computes a hash value for the point.

    Example:
        p1 = Point(1.0, 2.0)
        p2 = Point(1.0, 2.0)
        if p1 == p2:
            print("The points are equal.")
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def find_symmetry_lines(points: list[Point]) -> set[tuple[float, float]]:
    if not points:
        return set()

    def midpoint(p1, p2):
        """
        Calculate the midpoint between two points.

        :param p1: The first point.
        :param p2: The second point.
        :return: A new Point object representing the midpoint.
        """
        return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)

    def slope(p1, p2):
        """
        Calculate the slope of the line passing through two points.

        :param p1: The first point.
        :param p2: The second point.
        :return: The slope of the line or 'float('inf')' for a vertical line.
        """
        if p2.x - p1.x == 0:  # vertical line
            return float('inf')
        return (p2.y - p1.y) / (p2.x - p1.x)

    def perpendicular_bisector(p1: Point, p2: Point) -> tuple[float, float]:
        """
        Calculate the equation of the perpendicular bisector line between two points.

        This function calculates the slope and midpoint of the line segment
        defined by two points, and then computes the equation of the perpendicular
        bisector line passing through the midpoint.

        :param p1: The first point.
        :param p2: The second point.
        :return: A tuple (m, c) representing the equation of the perpendicular bisector line
                in the form 'y = mx + c'. The tuple values are rounded to the global
                precision defined as 'PRECISION' (default: 0.001).
                For vertical lines, it returns (float('inf'), round(mid.x, PRECISION)).
                For horizontal lines, it returns (0, round(mid.y, PRECISION)).
        """
        # Calculate the slope of the line passing through two points, p1 and p2.
        m = slope(p1, p2)

        # Calculate the midpoint between points p1 and p2.
        mid = midpoint(p1, p2)

        if m == 0:  # horizontal line
            return (float('inf'), round(mid.x, PRECISION))
        if m == float('inf'):  # vertical line
            return (0, round(mid.y, PRECISION))
        
        # Calculate the slope of the perpendicular bisector line.
        m_perpendicular = -1 / m

        # Calculate the y-intercept (c) of the perpendicular bisector line using its midpoint.
        c = mid.y - m_perpendicular * mid.x
        
        return (round(m_perpendicular, PRECISION), round(c, PRECISION))

    # Using a set avoids duplicates and ensures that each unique bisector is considered.
    potential_bisectors = set()

    # Calculate potential bisectors between pairs of points in the input list.
    # Iterate through all combinations of points, ensuring that each unique bisector is added to the set.
    # TODO: This nested loop results in O(n^2) time complexity and should probably be optimized later on.
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            bisector = perpendicular_bisector(points[i], points[j])
            potential_bisectors.add(bisector)
