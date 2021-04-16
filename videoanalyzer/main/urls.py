from django.urls import path
from .views import feed, home, shape, detect_circle, detect_triangle, detect_square

urlpatterns = [
    path('', home, name="home"),
    path('shape/', shape, name="shape"),
    path('shape/circle/', detect_circle, name="circle"),
    path('shape/triangle/', detect_triangle, name="triangle"),
    path('shape/square/', detect_square, name="square"),
    path('feed', feed, name="feed"),

]