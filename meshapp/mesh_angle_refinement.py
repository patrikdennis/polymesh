import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

class Mesh:
    def __init__(self, domain, num_points_inside=100):
        self.domain = domain
        self.num_points_inside = num_points_inside
        self.points = None
        self.triangles = None

    def generate_mesh(self):
        """
        Generates a constrained mesh where triangles respect the domain boundary.
        """
        # Collect boundary points
        boundary_points = self.domain.boundary.tolist()

        # Generate internal points
        internal_points = self.generate_internal_points()

        # Combine all points
        all_points = np.array(boundary_points + internal_points)

        # Perform Delaunay triangulation
        delaunay = Delaunay(all_points)
        triangles = delaunay.simplices

        # Ensure at least some triangles are retained
        filtered_triangles = [t for t in triangles if self.is_triangle_inside(all_points[t])]
        if len(filtered_triangles) == 0:
            print("Warning: No triangles were retained! Keeping at least one for visualization.")
            filtered_triangles = [triangles[0]]  # Keep at least one triangle

        self.points = all_points
        self.triangles = np.array(filtered_triangles)

    def generate_internal_points(self):
        """
        Generates random points inside the polygon to improve triangulation quality.
        """
        min_x, min_y = np.min(self.domain.boundary, axis=0)
        max_x, max_y = np.max(self.domain.boundary, axis=0)
        points_inside = []

        while len(points_inside) < self.num_points_inside:
            p = np.array([np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)])
            if self.is_inside_polygon(p):
                points_inside.append(p.tolist())

        return points_inside

    def is_triangle_inside(self, triangle_points):
        """
        Checks if a triangle is inside the polygon by testing its centroid.
        """
        centroid = np.mean(triangle_points, axis=0)
        return self.is_inside_polygon(centroid)

    def is_inside_polygon(self, point):
        """
        Determines if a point is inside the polygon using the ray-casting algorithm.
        """
        x, y = point
        inside = False
        n = len(self.domain.boundary)
        px, py = self.domain.boundary[:, 0], self.domain.boundary[:, 1]

        j = n - 1
        for i in range(n):
            if ((py[i] > y) != (py[j] > y)) and (x < (px[j] - px[i]) * (y - py[i]) / (py[j] - py[i]) + px[i]):
                inside = not inside
            j = i

        return inside

    def plot_mesh(self):
        """
        Plots the mesh with edges only (no fill colors).
        """
        if self.points is None or self.triangles is None:
            raise ValueError("Mesh not generated. Call generate_mesh() first.")

        plt.style.use("dark_background")
        fig, ax = plt.subplots()
        ax.set_aspect("equal", adjustable="box")

        # Plot the triangulation
        for t in self.triangles:
            polygon = self.points[t]
            for i in range(3):
                x1, y1 = polygon[i]
                x2, y2 = polygon[(i + 1) % 3]
                ax.plot([x1, x2], [y1, y2], "b-", linewidth=0.5)  # Blue edges

        # Plot the boundary
        ax.plot(self.domain.boundary[:, 0], self.domain.boundary[:, 1], "r-", linewidth=1.5, label="Boundary")

        ax.set_title("Refined Constrained Mesh", color="white")
        plt.legend()
        plt.show()
