from django import forms

class currency_form(forms.Form):
    currency_note = forms.FileField(widget=forms.FileInput(attrs={'class': "form-control", 'type' : 'file', 'placeholder' : 'Select Image'}), required=True)