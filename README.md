# Line of Symmetry Detection
This Python project focuses on the detection of lines of symmetry within a set of 2D points. The core algorithm, encapsulated in the symmetry.py module, offers the capability to identify lines of symmetry based on the inherent symmetry properties of the input points.

## Algorithm Overview
The algorithm for finding lines of symmetry operates on the following principles:

### Midpoint Calculation: 
It starts by calculating the midpoint between pairs of distinct points in the input set. The midpoint serves as a pivotal element in defining symmetry.

### Slope Determination: 
The algorithm computes the slope of the line connecting two points. Special handling is applied for vertical and horizontal lines.

### Perpendicular Bisectors: 
For each pair of points, a perpendicular bisector line is constructed. This bisector line is represented by its slope and y-intercept (in the form y = mx + c).

### Symmetry Testing: 
The algorithm then proceeds to test whether a candidate bisector line represents a line of symmetry for the entire set of points. This involves checking if the reflected points across the candidate line exist within the original point set.

### Tolerance for Precision: 
To accommodate potential floating-point imprecision, the algorithm allows for near matches, controlled by an adjustable precision value.

## Features
### Customizable Tolerance: 
The solution provides a user-adjustable precision value for controlling the tolerance in point coordinate comparisons.

### Handling Duplicate Points: 
Duplicate points within the input set are treated as a single instance of the same point, simplifying analysis.

### Edge Cases Handling: 
The algorithm accounts for edge cases, such as scenarios where the line of symmetry doesn't pass through the midpoint of any two points or when all points are collinear.

### Near-Match Recognition: 
Near matches within the specified tolerance are recognized.
