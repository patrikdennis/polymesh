from django.urls import path
from .views import draw_polygon, index, generate_mesh

urlpatterns = [
    path("", index, name="home"),
    path("draw/", draw_polygon, name="draw"),
    path("generate-mesh/", generate_mesh, name="generate_mesh"),
]
