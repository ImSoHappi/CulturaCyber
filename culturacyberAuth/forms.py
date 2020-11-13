from django.forms import ModelForm, Form
from django import forms

class FormLogin(Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())