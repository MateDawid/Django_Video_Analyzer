from django import forms
from .models import CircleDetectionModel


# class DisplayForm(forms.ModelForm):
#     class Meta:
#         model = DisplayModel
#         fields = ['display_mode']

class CircleDetectionForm(forms.ModelForm):
    class Meta:
        model = CircleDetectionModel
        fields = '__all__'
