from django.urls import path
from .views import clean_feed, home, CreateDisplayView

urlpatterns = [
    path('', home, name="home"),
    path('clean_feed', clean_feed, name="clean_feed"),
    path('', CreateDisplayView.as_view(), name='')

]