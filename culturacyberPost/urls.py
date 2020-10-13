from django.urls import path
from . import views

urlpatterns = [
    path('crear_post', views.add_post, name='add_post'),
    path('detalle_post/<uuid:post_uuid>', views.post_detail, name='post_detail'),
    path('añadir_material/<uuid:post_uuid>', views.add_attached, name='add_attached'),
    path('modulo/', views.module_detail, name='module_detail'),
]
