from django import forms

class CardForm(forms.Form):
    word = forms.CharField()
    image = forms.ImageField()