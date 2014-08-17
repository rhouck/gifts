from django import forms
from django.forms import widgets

class SubscribeForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your Email Address'}))
    #city = forms.CharField(initial="San Francisco")
class ContactForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your Email Address'}))
	message = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Let us know right here...', 'rows': 4}))