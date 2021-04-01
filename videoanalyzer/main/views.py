from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from videoanalyzer.video import VideoCamera, gen

@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")

    except:  # This is bad! replace it with proper handling
        pass


def home(request):
    return render(request, "main/base.html")