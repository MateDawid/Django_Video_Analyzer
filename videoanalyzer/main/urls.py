from django.urls import path
from .views import feed, home, shape, color, face, detect_circle, detect_triangle, detect_square, \
    detect_color_by_hsv, detect_color_by_rgb, detect_face, detect_face_with_eyes

urlpatterns = [
    path('', home, name="home"),
    path('shape/', shape, name="shape"),
    path('shape/circle/', detect_circle, name="circle"),
    path('shape/triangle/', detect_triangle, name="triangle"),
    path('shape/square/', detect_square, name="square"),
    path('color/', color, name="color"),
    path('color/hsv', detect_color_by_hsv, name="color_hsv"),
    path('color/rgb', detect_color_by_rgb, name="color_rgb"),
    path('face/', face, name="face"),
    path('face/face', detect_face, name="face_only"),
    path('face/eyes', detect_face_with_eyes, name="face_with_eyes"),
    path('feed', feed, name="feed"),
]