from django.forms import ModelForm, Form
from django import forms
from .models import userModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class loginForm(Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class userForm(forms.ModelForm):
    class Meta:
        model = userModel
        fields = ('client', 'is_cultureteam', 'is_organizer',)
        labels = {
            'client': 'Cliente',
            'is_cultureteam': 'Miembro de cultura',
            'is_organizer': 'Usuario organizador'
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'is_cultureteam': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_organizer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class mainuserForm(forms.ModelForm):
    username = forms.EmailInput()

    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Correo electrónico',
        }
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(mainuserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None


class UpdateProfile(forms.ModelForm):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class Completeprofile(forms.ModelForm):

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1', 'password2')
