from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('listado_encuestas', views.survey_list, name='survey_list'),
    path('crear_encuestas', views.add_survey, name='add_survey'),
    path('detalle_encuesta', views.survey_detail, name='survey_detail'),
    path('module', views.module, name='module'),
]
