from django.shortcuts import render
from django.views.decorators import gzip
from django.views.generic import CreateView
from django.http import StreamingHttpResponse
from videoanalyzer.video import VideoCamera, gen

from .models import DisplayModel
from .forms import DisplayForm

@gzip.gzip_page
def circle_feed(request):
    try:
        cam = VideoCamera(shapeDetection="circle")
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


def home(request):
    return render(request, "main/index.html")

def shape(request):
    return render(request, "main/shape.html")

def detect_circle(request):
    return render(request, "main/circle.html")

