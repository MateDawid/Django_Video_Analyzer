import numpy as np
import cv2
from PIL import Image
import base64
from io import BytesIO

from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse

from videoanalyzer.video import VideoCamera, gen
from .forms import CircleDetectionForm, TriangleAndSquareCDetectionForm, ColorHSVDetectionForm, \
    ColorRGBDetectionForm, FaceDetectionForm, EyesDetectionForm


@gzip.gzip_page
def feed(request):
    if request.session['circle_detection'] != {}:
        data = request.session['circle_detection']
        cam = VideoCamera(shape_detection="circle",
                          dp=float(data['dp']),
                          min_dist=float(data['min_dist']),
                          param1=float(data['param1']),
                          param2=float(data['param2']),
                          min_radius=int(data['min_radius']),
                          max_radius=int(data['max_radius']))
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    elif request.session['triangle_detection'] != {}:
        data = request.session['triangle_detection']
        cam = VideoCamera(shape_detection="triangle",
                          kernel_shape=int(data['kernel_shape']),
                          approximation=float(data['approximation']),
                          max_area=float(data['max_area']))
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    elif request.session['square_detection'] != {}:
        data = request.session['square_detection']
        cam = VideoCamera(shape_detection="square",
                          kernel_shape=int(data['kernel_shape']),
                          approximation=float(data['approximation']),
                          max_area=float(data['max_area']))
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    elif request.session['color_detection_hsv'] != {}:
        data = request.session['color_detection_hsv']
        cam = VideoCamera(color_detection="HSV",
                          hue_min=int(data['min_hue']),
                          saturation_min=int(data['min_saturation']),
                          value_min=int(data['min_value']),
                          hue_max=int(data['max_hue']),
                          saturation_max=int(data['max_saturation']),
                          value_max=int(data['max_value']))
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    elif request.session['color_detection_rgb'] != {}:
        data = request.session['color_detection_rgb']
        cam = VideoCamera(color_detection="RGB",
                          red_min=int(data['red_min']),
                          green_min=int(data['green_min']),
                          blue_min=int(data['blue_min']),
                          red_max=int(data['red_max']),
                          green_max=int(data['green_max']),
                          blue_max=int(data['blue_max']))
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    elif request.session['face_detection'] != {}:
        data = request.session['face_detection']
        cam = VideoCamera(face_detection="face",
                          face_scale_factor=float(data['face_scale_factor']),
                          face_min_neighbors=int(data['face_min_neighbors']),
                          face_min_size=None if data['face_min_size'] == "" else int(data['face_min_size']),
                          face_max_size=None if data['face_max_size'] == "" else int(data['face_max_size']))
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")

    elif request.session['face_with_eyes_detection'] != {}:
        data = request.session['face_with_eyes_detection']
        cam = VideoCamera(face_detection="eyes",
                          face_scale_factor=float(data['face_scale_factor']),
                          face_min_neighbors=int(data['face_min_neighbors']),
                          face_min_size=None if data['face_min_size'] == "" else int(data['face_min_size']),
                          face_max_size=None if data['face_max_size'] == "" else int(data['face_max_size']),
                          eye_scale_factor=float(data['eye_scale_factor']),
                          eye_min_neighbors=int(data['eye_min_neighbors']),
                          eye_min_size=None if data['eye_min_size'] == "" else int(data['eye_min_size']),
                          eye_max_size=None if data['eye_max_size'] == "" else int(data['eye_max_size']))
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    else:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")


def home(request):
    return render(request, "main/index.html")


def shape(request):
    return render(request, "main/shape.html")


def color(request):
    return render(request, "main/colors.html")


def face(request):
    return render(request, "main/face.html")


def reset_session(request):
    request.session["circle_detection"] = {}
    request.session["triangle_detection"] = {}
    request.session["square_detection"] = {}
    request.session["color_detection"] = {}
    request.session["color_detection_hsv"] = {}
    request.session["color_detection_rgb"] = {}
    request.session["face_detection"] = {}
    request.session["face_with_eyes_detection"] = {}


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
    return render(request, "main/triangle.html", {"triangle_form": triangle_form})


def detect_square(request):
    reset_session(request)
    square_form = TriangleAndSquareCDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["square_detection"] = request.POST
    return render(request, "main/square.html", {"square_form": square_form})


def detect_color_by_hsv(request):
    reset_session(request)
    colors_form_hsv = ColorHSVDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["color_detection_hsv"] = request.POST
        data = request.POST
        hsv_min = VideoCamera.count_hsv_values(int(data['min_hue']), int(data['min_saturation']),
                                               int(data['min_value']))
        hsv_max = VideoCamera.count_hsv_values(int(data['max_hue']), int(data['max_saturation']),
                                               int(data['max_value']))
        converted_min = convert_hsv_to_rgb(hsv_min[0], hsv_min[1], hsv_min[2])
        converted_max = convert_hsv_to_rgb(hsv_max[0], hsv_max[1], hsv_max[2])
        array_min = display_color(converted_min[2], converted_min[1], converted_min[0])
        array_max = display_color(converted_max[2], converted_max[1], converted_max[0])
    else:
        array_min = display_color(255, 255, 255)
        array_max = display_color(0, 0, 0)
    image_min = convert_array_to_image(array_min)
    image_max = convert_array_to_image(array_max)
    rgb_min = convert_image_to_data_uri(image_min)
    rgb_max = convert_image_to_data_uri(image_max)
    return render(request, "main/colors_hsv.html",
                  {"colors_form_hsv": colors_form_hsv, "rgb_min": rgb_min, "rgb_max": rgb_max})


def detect_color_by_rgb(request):
    reset_session(request)
    colors_form_rgb = ColorRGBDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["color_detection_rgb"] = request.POST
        data = request.POST
        print(data)
        array_min = display_color(int(data['blue_min']), int(data['green_min']), int(data['red_min']))
        array_max = display_color(int(data['blue_max']), int(data['green_max']), int(data['red_max']))
    else:
        array_min = display_color(255, 255, 255)
        array_max = display_color(0, 0, 0)
    image_min = convert_array_to_image(array_min)
    image_max = convert_array_to_image(array_max)
    rgb_min = convert_image_to_data_uri(image_min)
    rgb_max = convert_image_to_data_uri(image_max)
    return render(request, "main/colors_rgb.html",
                  {"colors_form_rgb": colors_form_rgb, "rgb_min": rgb_min, "rgb_max": rgb_max})


def detect_face(request):
    reset_session(request)
    face_form = FaceDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["face_detection"] = request.POST
    return render(request, "main/face_only.html", {"face_form": face_form})


def detect_face_with_eyes(request):
    reset_session(request)
    face_with_eyes_form = EyesDetectionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        request.session["face_with_eyes_detection"] = request.POST
    return render(request, "main/face_with_eyes.html", {"face_with_eyes_form": face_with_eyes_form})


def display_color(blue, green, red):
    # Create a blank 10x10 black image
    image = np.zeros((50, 50, 3), np.uint8)
    # Set each pixel to selected color
    image[:] = (red, green, blue)
    return image


def convert_array_to_image(numpy_img):
    img = Image.fromarray(numpy_img, 'RGB')
    return img


def convert_image_to_data_uri(pil_img):
    data = BytesIO()
    pil_img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,' + data64.decode('utf-8')


def convert_hsv_to_rgb(hue, saturation, value):
    hsv_color = np.uint8([[[hue, saturation, value]]])
    rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2RGB)
    return rgb_color[0][0]
