from django import forms
from ga.jobs.models import DownloadUser

class LoginForm(forms.ModelForm):
    class Meta:
        model = DownloadUser
        fields = ['name', 'email']
        
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        
