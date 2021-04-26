from django.shortcuts import render
from django.views.decorators import gzip
from django.views.generic import CreateView
from django.http import StreamingHttpResponse
from videoanalyzer.video import VideoCamera, gen

from .forms import CircleDetectionForm, TriangleAndSquareCDetectionForm

@gzip.gzip_page
def feed(request):
    print(dict(request.session))
    if request.session['circle_detection'] != {}:
        try:
            data = request.session['circle_detection']
            cam = VideoCamera(shapeDetection="circle",
                                dp=float(data['dp']),
                                minDist=float(data['minDist']),
                                param1=float(data['param1']),
                                param2=float(data['param2']),
                                minRadius=int(data['minRadius']),
                                maxRadius=int(data['maxRadius']))
            request.session['circle_detection'] = {}
            return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
        except:  # This is bad! replace it with proper handling
            print("Circle = Lack of camera")
    elif request.session['triangle_detection'] != {}:
        try:
            data = request.session['triangle_detection']
            cam = VideoCamera(shapeDetection="triangle",
                              kernelShape=int(data['kernelShape']),
                              approximation=float(data['approximation']),
                              maxArea=float(data['maxArea']))
            return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
            request.session['triangle_detection'] = {}
        except:  # This is bad! replace it with proper handling
            print("Triangle = Lack of camera")
    elif request.session['square_detection'] != {}:
        try:
            data = request.session['square_detection']
            cam = VideoCamera(shapeDetection="square",
                              kernelShape=int(data['kernelShape']),
                              approximation=float(data['approximation']),
                              maxArea=float(data['maxArea']))
            return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
            request.session['square_detection'] = {}
        except:  # This is bad! replace it with proper handling
            print("Square = Lack of camera")

    else:
        try:
            cam = VideoCamera(colorDetection="HSV")
            return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
        except:  # This is bad! replace it with proper handling
            print("Lack of camera")


def home(request):
    return render(request, "main/index.html")


def shape(request):
    return render(request, "main/shape.html")

def color(request):
    return render(request, "main/colors.html")


def reset_session(request):
    request.session["circle_detection"] = {}
    request.session["triangle_detection"] = {}
    request.session["square_detection"] = {}
    request.session["color_detection"] = {}
    request.session["color_detection_hsv"] = {}
    request.session["color_detection_rgb"] = {}


def detect_circle(request):
    reset_session(request)
    circle_form = CircleDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["circle_detection"] = request.POST
    return render(request, "main/circle.html", {"circle_form": circle_form})


def detect_triangle(request):
    reset_session(request)
    triangle_form = TriangleAndSquareCDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["triangle_detection"] = request.POST
    else:
        request.session["triangle_detection"] = {}
    return render(request, "main/triangle.html", {"triangle_form": triangle_form})


def detect_square(request):
    reset_session(request)
    square_form = TriangleAndSquareCDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["square_detection"] = request.POST
    else:
        request.session["square_detection"] = {}
    return render(request, "main/square.html", {"square_form": square_form})


def detect_color_by_hsv(request):
    reset_session(request)
    # colors_form = HSVColorsDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["color_detection_hsv"] = request.POST
    else:
        request.session["color_detection_hsv"] = {}
    return render(request, "main/colors_hsv.html")  # , {"colors_form_hsv": colors_form_hsv})


def detect_color_by_rgb(request):
    reset_session(request)
    # colors_form = RGBColorsDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["color_detection_rgb"] = request.POST
    else:
        request.session["color_detection_rgb"] = {}
    return render(request, "main/colors_rgb.html")  # , {"colors_form_rgb": colors_form_rgb})
