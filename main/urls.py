from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', LogoutView.as_view(next_page='login_view'), name='home'),
    path('login/', views.login_view, name='login_view'),

    path('registro/', views.registro, name='registro'),
    path('menu_turista/', views.menu_turista, name='menu_turista'),
    path('menu_morador_local/', views.menu_morador_local, name='menu_morador_local'),

    path('restaurantes/', views.restaurantes_view, name='restaurantes_view'),
    path('mudar-senha/', views.mudar_senha, name='mudar_senha'),
    path('senha-mudada-com-sucesso/', views.senha_mudada_com_sucesso, name='senha_mudada_com_sucesso'),

    path('gerenciar_restaurantes/', views.gerenciar_restaurantes, name='gerenciar_restaurantes'),
    path('adicionar_restaurante/', views.adicionar_restaurante, name='adicionar_restaurante'),
    path('editar_restaurante/<int:id>/', views.editar_restaurante, name='editar_restaurante'),
    path('remover_restaurante/<int:id>/', views.remover_restaurante, name='remover_restaurante'),

    # Novas URLs para avaliações e comentários
    path('adicionar_avaliacao/<int:restaurante_id>/', views.adicionar_avaliacao, name='adicionar_avaliacao'),
    path('adicionar_comentario/<int:restaurante_id>/', views.adicionar_comentario, name='adicionar_comentario'),
    path('ver_avaliacoes_comentarios/<int:restaurante_id>/', views.ver_avaliacoes_comentarios, name='ver_avaliacoes_comentarios'),

    # Nova URL para adicionar restaurantes externos
    path(
        'adicionar_restaurante_externo/<str:nome>/<str:endereco>/<str:latitude>/<str:longitude>/',
        views.adicionar_restaurante_externo,
        name='adicionar_restaurante_externo'
    ),

    path('logout/', LogoutView.as_view(next_page='login_view'), name='logout'),
]