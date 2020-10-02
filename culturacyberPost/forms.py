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