from django import forms
from culturacyberAuth.models import clientModel

class clientForm(forms.ModelForm):
    class Meta:
        model = clientModel
        fields = ('name', 'description',)
        labels = {
            'name': 'Nombre del cliente',
            'description': 'Descripción'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }