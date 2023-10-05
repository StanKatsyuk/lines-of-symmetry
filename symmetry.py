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
