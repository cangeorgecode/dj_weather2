from django import forms

class City(forms.Form):
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a city'}), label='')