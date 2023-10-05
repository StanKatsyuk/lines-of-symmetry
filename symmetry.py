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
