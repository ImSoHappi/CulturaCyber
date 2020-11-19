from django.forms import ModelForm, Form
from django import forms
from .models import userModel

class loginForm(Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class userForm(forms.ModelForm):
    class Meta:
        model = userModel
        fields = ('client', 'is_cultureteam', 'is_organizer',)
        labels = {
            'client': 'Empresa',
            'is_cultureteam': 'Miembro de cultura',
            'is_organizer': 'Usuario organizador'
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'is_cultureteam': forms.CheckboxInput(attrs={'class': 'form-check-input mb-3'}),
            'is_organizer': forms.CheckboxInput(attrs={'class': 'form-check-input mb-3'}),
        }

