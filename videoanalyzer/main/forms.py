from django import forms
from .models import CircleDetectionModel, TriangleAndSquareDetectionModel, ColorHSVDetectionModel, \
                    ColorRGBDetectionModel, FaceDetectionModel, EyesDetectionModel


class CircleDetectionForm(forms.ModelForm):
    class Meta:
        model = CircleDetectionModel
        fields = '__all__'


class TriangleAndSquareCDetectionForm(forms.ModelForm):
    class Meta:
        model = TriangleAndSquareDetectionModel
        fields = '__all__'


class ColorHSVDetectionForm(forms.ModelForm):
    class Meta:
        model = ColorHSVDetectionModel
        fields = '__all__'


class ColorRGBDetectionForm(forms.ModelForm):
    class Meta:
        model = ColorRGBDetectionModel
        fields = '__all__'


class FaceDetectionForm(forms.ModelForm):
    class Meta:
        model = FaceDetectionModel
        fields = '__all__'


class EyesDetectionForm(forms.ModelForm):
    class Meta:
        model = EyesDetectionModel
        fields = '__all__'
        widgets = {
            'face_scale_factor': forms.TextInput(attrs={'title': 'Face scale factor'})
        }
