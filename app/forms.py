from django import forms

class URLInputForm(forms.Form):
    url = forms.URLField(label='Enter the URL of the Etsy shop')
