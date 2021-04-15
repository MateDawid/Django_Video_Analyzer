from django import forms
from .models import CircleDetectionModel, TriangleDetectionModel


# class DisplayForm(forms.ModelForm):
#     class Meta:
#         model = DisplayModel
#         fields = ['display_mode']

class CircleDetectionForm(forms.ModelForm):
    class Meta:
        model = CircleDetectionModel
        fields = '__all__'

class TriangleDetectionForm(forms.ModelForm):
    class Meta:
        model = TriangleDetectionModel
        fields = '__all__'
