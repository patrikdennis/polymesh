import numpy as np 
class Domain2:
    """
    Represents a general domain that supports polygon and circular boundaries.
    """
    def __init__(self, boundary_points, num_boundary_points=100):
        """
        Initialize the domain.

        Parameters:
        - boundary_points: List of (x, y) tuples defining the boundary vertices.
        - num_boundary_points: Total number of points to generate uniformly on the boundary.
        """
        self.original_boundary = np.array(boundary_points)
        self.num_boundary_points = num_boundary_points
        
        num_vertices = len(self.original_boundary)
        if num_boundary_points == num_vertices:
            self.boundary = self.original_boundary
        elif num_boundary_points < num_vertices:
            print(f"The number of boundary points needs to be higher than the number of of vertices {num_vertices}")
            return None
        else:
            self.boundary = self._generate_uniform_boundary()

    def _generate_uniform_boundary(self):
        """
        Generates a uniform set of points along the boundary.

        Returns:
        - Array of uniformly spaced boundary points.
        """
        # Compute the total length of the boundary (polygon perimeter)
        perimeter = 0
        for i in range(len(self.original_boundary)):
            p1 = self.original_boundary[i]
            p2 = self.original_boundary[(i + 1) % len(self.original_boundary)]
            perimeter += np.linalg.norm(p2 - p1)

        # Length of each segment based on the desired number of boundary points
        segment_length = perimeter / self.num_boundary_points

        # Generate uniform points along each segment
        uniform_points = []
        for i in range(len(self.original_boundary)):
            p1 = self.original_boundary[i]
            p2 = self.original_boundary[(i + 1) % len(self.original_boundary)]
            segment_distance = np.linalg.norm(p2 - p1)
            num_points = max(2, int(np.round(segment_distance / segment_length)))

            # Generate points between p1 and p2
            for t in np.linspace(0, 1, num_points, endpoint=False):
                point = (1 - t) * p1 + t * p2
                uniform_points.append(point)

        # Add the final point to close the loop
        uniform_points.append(self.original_boundary[0])
        return np.array(uniform_points)

    def is_inside(self, point):
        """
        Check if a point is inside the domain using ray-casting for polygons.
        """
        x, y = point
        n = len(self.original_boundary)
        inside = False

        px, py = self.original_boundary[0]
        for i in range(1, n + 1):
            vx, vy = self.original_boundary[i % n]
            if (py > y) != (vy > y):
                intersect = (vx - px) * (y - py) / (vy - py) + px
                if x < intersect:
                    inside = not inside
            px, py = vx, vy

        return inside

    def get_bounding_box(self):
        """
        Get the bounding box of the domain.

        Returns:
        - (xmin, xmax, ymin, ymax)
        """
        xmin = np.min(self.original_boundary[:, 0])
        xmax = np.max(self.original_boundary[:, 0])
        ymin = np.min(self.original_boundary[:, 1])
        ymax = np.max(self.original_boundary[:, 1])
        return xmin, xmax, ymin, ymax
