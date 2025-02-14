from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('registro/', views.registro, name='registro'),
    path('menu_turista/', views.menu_turista, name='menu_turista'),
    path('menu_morador_local/', views.menu_morador_local, name='menu_morador_local'),
]