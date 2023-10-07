import math

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

    if len(points) == 1:
        return {points[0]}  # Return a set containing the single point

    if len(points) > 100:
        print('too many')
        raise ValueError('Algorithm is not optimized to run with more than 100 points')


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
            return (float('inf'), round(mid.x, int(-math.log10(PRECISION))))
        if m == float('inf'):  # vertical line
            return (0, round(mid.y, int(-math.log10(PRECISION))))
        
        # Calculate the slope of the perpendicular bisector line.
        m_perpendicular = -1 / m

        # Calculate the y-intercept (c) of the perpendicular bisector line using its midpoint.
        c = mid.y - m_perpendicular * mid.x
        
        return (round(m_perpendicular, int(-math.log10(PRECISION))), round(c, int(-math.log10(PRECISION))))


    # Using a set avoids duplicates and ensures that each unique bisector is considered.
    potential_bisectors = set()

    # Calculate potential bisectors between pairs of points in the input list.
    # Iterate through all combinations of points, ensuring that each unique bisector is added to the set.
    # TODO: This nested loop results in O(n^2) time complexity and should probably be optimized later on.
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            bisector = perpendicular_bisector(points[i], points[j])
            potential_bisectors.add(bisector)

    def is_close(p1: Point, p2: Point, tol=PRECISION) -> bool:
        """
        Check if two points are close enough within the given fixed tolerance.

        :param p1: The first point.
        :param p2: The second point.
        :param tol: The fixed tolerance value for point closeness. This is necessary due to potential floating-point imprecision in calculations.
        :return: True if the points are close within the tolerance; otherwise, False.
        """
        return abs(p1.x - p2.x) < tol and abs(p1.y - p2.y) < tol

    def is_symmetry_line(m: float, c: float, points: list[Point]) -> bool:
        if m == float('inf'):  # Check for a vertical line
            for p in points:
                # Calculate the x-coordinate of the reflected point for a vertical line
                # When the line of symmetry is vertical (m == float('inf')), calculate the x-coordinate
                # of the reflected point by reflecting the point p.x across the vertical line defined by x = c,
                # where 'c' is twice the y-intercept of the line and represents the x-coordinate of the
                # reflected point.
                reflected_x = round(2 * c - p.x, 6)
                reflected_y = round(p.y, 6)
                
                # Check if the reflected point exists in the original set of points
                if not any(is_close(Point(reflected_x, reflected_y), orig) for orig in points):
                    return False
        else:
            for p in points:
                # Calculate the coordinates of the reflected point across the line y = mx + c.
                # To do this, we first find the perpendicular distance 'd' from the original
                # point (p.x, p.y) to the line. Then, we move the point by '2d' units in the
                # direction perpendicular to the line to obtain the reflected coordinates.
                # 'numerator_x' corresponds to the x-coordinate, and 'numerator_y' corresponds
                # to the y-coordinate of the reflected point.
                numerator_x = p.x + (p.y - c) * m
                numerator_y = (p.y - c) - m * p.x

                # Calculate the coordinates of the reflected point using the formula for
                # reflection across a line. 'denominator' represents a constant value, and
                # we use it to adjust the movement of the point to obtain the reflected
                # coordinates 'reflected_x' and 'reflected_y'. Rounding is applied to ensure
                # precision up to 6 decimal places.
                denominator = 1 + m**2
                reflected_x = round(p.x - 2 * numerator_x / denominator, 6)
                reflected_y = round(p.y - 2 * numerator_y / denominator, 6)
                
                # Check if the reflected point exists in the original set of points
                if not any(is_close(Point(reflected_x, reflected_y), orig) for orig in points):
                    return False
            
        return True

    # Initialize a set to store the identified symmetry lines.
    symmetry_lines = set()

    # Iterate through the potential bisectors and check if they are symmetry lines.
    for m, c in potential_bisectors:
        if is_symmetry_line(m, c, points):
            symmetry_lines.add((m, c))

    # Return the set of identified symmetry lines.
    return symmetry_lines
