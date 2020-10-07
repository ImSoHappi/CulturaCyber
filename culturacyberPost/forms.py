from django import forms
from .models import *

class postForm(forms.ModelForm):
    class Meta:
        model = postModel
        fields = ('title', 'contentbody', 'postimg',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-4', 'id': 'title', 'placeholder': 'Ingresa un titulo para tu post'}),
            'contentbody': forms.Textarea(attrs={'class': 'form-control', 'name': 'text', 'rows': '20'}),
            'postimg': forms.FileInput(attrs={'class': 'form-control mb-4'})
        }

class attachedForm(forms.ModelForm):
    class Meta:
        model = attachedModel
        fields = ('name', 'file',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Nombre del archivo'}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }