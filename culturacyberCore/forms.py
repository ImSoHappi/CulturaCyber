from django import forms
from culturacyberAuth.models import clientModel, moduleModel, activityModel, taskModel
from .models import client_module_Model

class EditclientForm(forms.ModelForm):
    class Meta:
        model = clientModel
        fields = ('name', 'teamslink', 'description', 'disabled',)
        labels = {
            'name': 'Nombre del cliente',
            'teamslink': 'Link carpeta teams',
            'description': 'Descripción',
            'disabled': 'Deshabilitar cliente'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'teamslink': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'disabled': forms.CheckboxInput(attrs={'class': 'form-check-input mb-3'}),
        }

class AddclientForm(forms.ModelForm):
    class Meta:
        model = clientModel
        fields = ('name', 'teamslink', 'description',)
        labels = {
            'name': 'Nombre del cliente',
            'teamslink': 'Link carpeta principal teams',
            'description': 'Descripción',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'teamslink': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
        }

class moduleForm(forms.ModelForm):
    class Meta:
        model = moduleModel
        fields = ('name', 'icon', 'description',)
        labels = {
            'name': 'Nombre del modulo',
            'icon': 'Icono',
            'description': 'Descripción'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class activityForm(forms.ModelForm):
    class Meta:
        model = activityModel
        fields = ('name', 'programmed_date', 'description',)
        labels = {
            'name': 'Nombre de la actividad',
            'programmed_date': 'Fecha de programación',
            'description': 'Descripción'
        }
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'programmed_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class taskForm(forms.ModelForm):
    class Meta:
        model = taskModel
        fields = ('name', 'teamslink',)
        labels = {
            'name': 'Nombre de la tarea',
            'teamslink': 'Link del archivo en teams'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'teamslink': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

class add_teamslinkForm(forms.ModelForm):
    class Meta:
        model = client_module_Model
        fields = ('teamslink',)
        labels = {
            'teamslink': 'Link a la carpeta del modulo en teams',
        }
        widgets = {
            'teamslink': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }