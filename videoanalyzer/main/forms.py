from django import forms
from .models import CircleDetectionModel, TriangleAndSquareDetectionModel


# class DisplayForm(forms.ModelForm):
#     class Meta:
#         model = DisplayModel
#         fields = ['display_mode']

class CircleDetectionForm(forms.ModelForm):
    class Meta:
        model = CircleDetectionModel
        fields = '__all__'

class TriangleAndSquareCDetectionForm(forms.ModelForm):
    class Meta:
        model = TriangleAndSquareDetectionModel
        fields = '__all__'
