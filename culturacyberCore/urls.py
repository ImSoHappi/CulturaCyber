from django.urls import path
from . import views_organizer as organizer
from . import views_culture as culture
from . import views_user as users
from . import views_generic as generic

urlpatterns = [
    #Generic views
    path('', generic.login_view, name='login'),
    path('logout/', generic.logout_view, name='logout'),
    path('redirector/', generic.redirector, name="redirector"),

    #Organizer views
    path('home/', organizer.home, name='organizer_home'),
    path('home/mi_modulo/<str:module>/', organizer.module_detail, name='module_detail'),

    #Culture views
    path('home_cultura/', culture.home, name='culture_home'),
    path('administracion_clientes/', culture.client_admin, name='client_admin'),
    path('administracion_modulos/', culture.module_admin, name='module_admin'),
    path('administracion_clientes/editar_cliente/<str:client>/', culture.client_edit, name='client_edit'),
    path('home/clientes_modulo/<str:module>/', culture.module_client_list, name='module_client_list'),
    path('home/modulo_cliente/<str:module>/<str:client>/', culture.module_client, name='module_client'),
    path('home/modulo_cliente/<str:module>/<str:client>/añadir_actividad', culture.add_activity, name='add_activity'),

    #User views


    # path('listado_encuestas', views.survey_list, name='survey_list'),
    # path('crear_encuestas', views.add_survey, name='add_survey'),
    # path('detalle_encuesta', views.survey_detail, name='survey_detail'),
    # path('module', views.module, name='module'),
]
