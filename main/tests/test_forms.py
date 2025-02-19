# Teste de unidade do forms

from django.test import TestCase
from main.forms import RegistroUsuarioForm, RestauranteForm
from main.models import Usuario, Restaurante

class RegistroUsuarioFormTest(TestCase):
    def test_formulario_usuario_valido(self):
        form_data = {
            'nome': 'Usuário Teste',
            'telefone': '11999999999',
            'email': 'teste@exemplo.com',
            'morador_local': True,
            'cpf': '12345678901',
            'password1': 'senhaSegura123',
            'password2': 'senhaSegura123',
            'senha_confirmacao': 'senhaSegura123',  # Adicionado
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_formulario_usuario_senhas_diferentes(self):
        form_data = {
            'nome': 'Usuário Teste',
            'telefone': '11999999999',
            'email': 'teste@exemplo.com',
            'morador_local': True,
            'cpf': '12345678901',
            'password1': 'senhaSegura123',
            'password2': 'senhaErrada456',
        }
        form = RegistroUsuarioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('senha_confirmacao', form.errors)

class RestauranteFormTest(TestCase):
    def test_formulario_restaurante_valido(self):
        form_data = {
            'nome': 'Restaurante Exemplo',
            'endereco': 'Rua Exemplo, 123',
            'latitude': -23.550520,
            'longitude': -46.633308,
        }
        form = RestauranteForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_formulario_restaurante_campos_obrigatorios(self):
        form = RestauranteForm(data={})  # Dados vazios
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('endereco', form.errors)
        self.assertIn('latitude', form.errors)
        self.assertIn('longitude', form.errors)
