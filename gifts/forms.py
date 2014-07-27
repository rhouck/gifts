from django import forms
from django.forms import widgets

class SplashForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your Email Address'}))
