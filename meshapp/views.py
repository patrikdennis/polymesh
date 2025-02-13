from django.shortcuts import render
from django.http import JsonResponse
import json
from .mesh import Mesh  
from .domain2 import Domain2  

def index(request):
    return render(request, "meshapp/index.html")

def draw_polygon(request):
    return render(request, "meshapp/draw_polygon.html")

def generate_mesh(request):
    if request.method == "POST":
        try:
            # Get JSON data from request
            data = json.loads(request.body)
            points = data.get("points", [])
            num_points = int(data.get("num_points", 100))  # Default to 100 points if not specified

            # Validate input
            if not points or len(points) < 3:
                return JsonResponse({"success": False, "error": "Invalid polygon. At least 3 points required."}, status=400)

            # Create domain using the points from the frontend
            domain = Domain2(boundary_points=points, num_boundary_points=100)

            # Generate the mesh
            mesh = Mesh(domain, num_points_inside=num_points)
            mesh.generate_mesh()

            # Extract mesh edges
            edges = []
            for triangle in mesh.triangles:
                edges.append([mesh.points[triangle[0]].tolist(), mesh.points[triangle[1]].tolist()])
                edges.append([mesh.points[triangle[1]].tolist(), mesh.points[triangle[2]].tolist()])
                edges.append([mesh.points[triangle[2]].tolist(), mesh.points[triangle[0]].tolist()])

            return JsonResponse({"success": True, "message": "Mesh successfully generated!", "edges": edges})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
