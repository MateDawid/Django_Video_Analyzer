from django.urls import path
from .views import feed, home

urlpatterns = [
    path('', home, name="home"),
    path('feed', feed, name="feed"),
]