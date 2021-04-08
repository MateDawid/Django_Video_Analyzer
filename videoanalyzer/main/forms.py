from django import forms
from .models import DisplayModel


class DisplayForm(forms.ModelForm):
    class Meta:
        model = DisplayModel
        fields = ['display_mode']



# class SearchForm(forms.Form):
#     city = forms.CharField(label="", help_text="",
#                            widget=forms.TextInput(attrs={'placeholder': 'Miasto (wymagane)', 'class': 'formField'}))
#     min_price = forms.CharField(label="", help_text="",
#                                 widget=forms.TextInput(attrs={'placeholder': 'Cena min.', 'class': 'formField'}),
#                                 required=False)
#     max_price = forms.CharField(label="", help_text="",
#                                 widget=forms.TextInput(attrs={'placeholder': 'Cena max.', 'class': 'formField'}),
#                                 required=False)
#     min_area = forms.CharField(label="", help_text="",
#                                widget=forms.TextInput(attrs={'placeholder': 'Powierzchnia min.', 'class': 'formField'}),
#                                required=False)
#     max_area = forms.CharField(label="", help_text="",
#                                widget=forms.TextInput(attrs={'placeholder': 'Powierzchnia max.', 'class': 'formField'}),
#                                required=False)
#     days_from_publication = forms.CharField(label="", help_text="", widget=forms.TextInput(
#         attrs={'placeholder': 'Dni od dodania', 'class': 'formField'}), required=False)
#
#     def clean_min_price(self):
#         min_price = self.cleaned_data['min_price']
#         if min_price.isnumeric() or min_price == "":
#             return min_price
#         else:
#             raise forms.ValidationError("Spróbuj wpisać liczbę!")
#
#     def clean_max_price(self):
#         max_price = self.cleaned_data['max_price']
#         if max_price.isnumeric() or max_price == "":
#             return max_price
#         else:
#             raise forms.ValidationError("Spróbuj wpisać liczbę!")
#
#     def clean_min_area(self):
#         min_area = self.cleaned_data['min_area']
#         if min_area.isnumeric() or min_area == "":
#             return min_area
#         else:
#             raise forms.ValidationError("Spróbuj wpisać liczbę!")
#
#     def clean_max_area(self):
#         max_area = self.cleaned_data['max_area']
#         if max_area.isnumeric() or max_area == "":
#             return max_area
#         else:
#             raise forms.ValidationError("Spróbuj wpisać liczbę!")
#
#     def clean_days_from_publication(self):
#         days_from_publication = self.cleaned_data['days_from_publication']
#         if days_from_publication.isnumeric() or days_from_publication == "":
#             return days_from_publication
#         else:
#             raise forms.ValidationError("Spróbuj wpisać liczbę!")