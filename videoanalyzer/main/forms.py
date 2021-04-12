from django import forms
from .models import DisplayModel


class DisplayForm(forms.ModelForm):
    class Meta:
        model = DisplayModel
        fields = ['display_mode']
