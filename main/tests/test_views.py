# Esse arquivo testa as views (ou seja, as páginas e ações da aplicação web) relacionadas aos usuários.

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class UsuarioViewsTest(TestCase): # Essa classe testa funcionalidades das views que lidam com os usuários.
    def setUp(self): # Cria um cliente (self.client) para simular requisições HTTP no Django e cria um usuário de teste no banco de dados.
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='teste@exemplo.com',
            nome='Usuário Teste',
            senha='senha123'
        )

    def test_registro_view(self): # Verifica se a view de registro de usuário está funcionando corretamente.
        response = self.client.post(reverse('registro'), {
            'nome': 'Novo Usuário',
            'telefone': '11999999999',
            'email': 'novo@exemplo.com',
            'senha': 'senha123',
            'senha_confirmacao': 'senha123',
            'morador_local': True,
            'cpf': '12345678901'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado
        self.assertTrue(get_user_model().objects.filter(email='novo@exemplo.com').exists())

    def test_login_view(self): # Verifica se a view de login está funcionando corretamente.
        self.user.set_password('senha123')  # Define a senha corretamente
        self.user.save()

        response = self.client.post(reverse('login_view'), {
            'email': 'teste@exemplo.com',
            'senha': 'senha123'
        })

        self.assertEqual(response.status_code, 302)  # Redirecionamento esperado após login
