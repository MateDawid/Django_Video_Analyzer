from django.urls import path
from .views import clean_feed,shape_feed, home

urlpatterns = [
    path('', home, name="home"),
    path('clean_feed', clean_feed, name="clean_feed"),
    path('shape_feed', shape_feed, name="shape_feed"),

]