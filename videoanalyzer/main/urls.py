from django.urls import path
from .views import livefe, home

urlpatterns = [
    path('', home, name="home"),
    path('webcam', livefe, name="livefe"),
]