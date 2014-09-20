from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        required = True,
        widget = forms.TextInput({'class': 'form-control'})
    )
    email = forms.CharField(
        required = True,
        widget = forms.EmailInput({'class': 'form-control'})
    )
    message = forms.CharField(
        required = False,
        widget=forms.Textarea({'class': 'form-control'}),
    )
    
