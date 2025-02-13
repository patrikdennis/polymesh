import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

class Mesh:
    """
    Represents the triangular mesh of a domain.
    """
    def __init__(self, domain, num_points_inside):
        """
        Initializes the mesh with a given domain.

        Parameters:
        - domain: An instance of the Domain class.
        - num_points_inside: Number of interior points to generate.
        """
        self.domain = domain
        self.num_points_inside = num_points_inside
        self.points = None
        self.triangles = None

    def generate_interior_points(self):
        """
        Generates structured grid points inside the domain.
        """
        xmin, xmax, ymin, ymax = self.domain.get_bounding_box()
        resolution = int(np.sqrt(self.num_points_inside))
        x = np.linspace(xmin, xmax, resolution)
        y = np.linspace(ymin, ymax, resolution)
        grid_points = np.array([[xi, yi] for xi in x for yi in y])
        interior_points = [point for point in grid_points if self.domain.is_inside(point)]
        return np.array(interior_points[:self.num_points_inside])

    def refine_mesh(self, points, simplices):
        """
        Refines the triangulation to ensure good triangle quality.
        Also removes triangles outside the polygon.

        Parameters:
        - points: Array of points in the mesh.
        - simplices: Array of triangles (indices of points).

        Returns:
        - Refined points and triangles.
        """
        def triangle_quality(triangle):
            """
            Computes the quality of a triangle (aspect ratio).
            """
            a = np.linalg.norm(triangle[0] - triangle[1])
            b = np.linalg.norm(triangle[1] - triangle[2])
            c = np.linalg.norm(triangle[2] - triangle[0])
            s = (a + b + c) / 2
            area = np.sqrt(s * (s - a) * (s - b) * (s - c))
            if area == 0:
                return 0
            circumradius = (a * b * c) / (4 * area)
            inradius = area / s
            return circumradius / inradius  # Aspect ratio

        refined_points = points.tolist()
        refined_triangles = []
        for simplex in simplices:
            triangle = points[simplex]
            quality = triangle_quality(triangle)

            # Compute centroid and check if it's inside the domain
            centroid = np.mean(triangle, axis=0)
            inside_domain = self.domain.is_inside(centroid)

            if quality > 2.0 and inside_domain:  # Ensure refinement only happens inside
                midpoint = np.mean(triangle, axis=0)
                if not any(np.allclose(midpoint, p) for p in refined_points):
                    refined_points.append(midpoint)
            elif inside_domain:
                refined_triangles.append(simplex)

        # Perform a new Delaunay triangulation on the refined points
        refined_points = np.array(refined_points)
        new_triangulation = Delaunay(refined_points)

        # **Filter out triangles that are outside the domain again**
        final_triangles = [t for t in new_triangulation.simplices if self.is_triangle_inside(refined_points[t])]

        return refined_points, np.array(final_triangles)

    def generate_mesh(self):
        """
        Generates the triangular mesh.
        """
        interior_points = self.generate_interior_points()
        points = np.vstack([self.domain.boundary, interior_points])
        triangulation = Delaunay(points)

        # Refine the mesh and filter invalid triangles
        self.points, self.triangles = self.refine_mesh(points, triangulation.simplices)

    def is_triangle_inside(self, triangle_points):
        """
        Checks if a triangle is inside the polygon by testing its centroid.
        """
        centroid = np.mean(triangle_points, axis=0)
        return self.domain.is_inside(centroid)

    def plot_mesh(self):
        """
        Plots only the mesh outlines (no face colors).
        """
        if self.points is None or self.triangles is None:
            raise ValueError("Mesh not generated. Call generate_mesh() first.")

        fig, ax = plt.subplots()
        ax.set_aspect("equal", adjustable="box")

        # Plot the triangulation
        ax.triplot(
            self.points[:, 0], self.points[:, 1], self.triangles,
            color="blue",  # Only edges, no fill
            linewidth=0.5
        )

        # Plot the boundary only (No interior points)
        ax.plot(self.domain.boundary[:, 0], self.domain.boundary[:, 1], "r-", linewidth=1.5, label="Boundary")

        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        ax.set_title("Polygon Outline (No Face Colors)", color="black")
        plt.show()
