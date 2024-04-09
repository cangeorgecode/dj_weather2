from django import forms

class City(forms.Form):
    city = forms.CharField()