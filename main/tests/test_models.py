# Contém testes para os modelos Usuario (provavelmente o modelo customizado de usuário) e Restaurante.

from django.test import TestCase
from django.contrib.auth import get_user_model
from main.models import Restaurante

class UsuarioModelTest(TestCase): # Essa classe testa o modelo de usuário.
    def setUp(self): # Cria um usuário de teste com email, nome, senha, telefone, se é morador local e CPF.
        self.user = get_user_model().objects.create_user(
            email='teste@exemplo.com',
            nome='Usuário Teste',
            senha='senha123',
            telefone='11999999999',
            morador_local=True,
            cpf='12345678901'
        )

    def test_usuario_criado_com_sucesso(self): # Verifica se o usuário foi criado corretamente, comparando os valores
        # armazenados no banco com os valores que foram passados na criação.
        self.assertEqual(self.user.email, 'teste@exemplo.com')
        self.assertEqual(self.user.nome, 'Usuário Teste')
        self.assertTrue(self.user.check_password('senha123')) # É usado para verificar se a senha foi armazenada corretamente no modelo.
        self.assertEqual(self.user.telefone, '11999999999')
        self.assertTrue(self.user.morador_local)
        self.assertEqual(self.user.cpf, '12345678901')

    def test_usuario_str_retorna_email(self): # Testa se a representação do objeto (__str__) retorna o email do usuário.
        self.assertEqual(str(self.user), 'teste@exemplo.com')

class RestauranteModelTest(TestCase): # Essa classe testa o modelo Restaurante.
    def setUp(self): # Cria um usuário para ser o dono do restaurante e cria um restaurante associado a esse usuário.
        self.user = get_user_model().objects.create_user(
            email='dono@restaurante.com',
            nome='Dono Restaurante',
            senha='senha123'
        )
        self.restaurante = Restaurante.objects.create(
            owner=self.user,
            nome='Restaurante Exemplo',
            endereco='Rua Exemplo, 123',
            latitude=-23.550520,
            longitude=-46.633308
        )

    def test_restaurante_criado_com_sucesso(self): # Verifica se o restaurante foi criado corretamente e se os valores do banco de dados batem com os valores passados na criação.
        self.assertEqual(self.restaurante.nome, 'Restaurante Exemplo')
        self.assertEqual(self.restaurante.endereco, 'Rua Exemplo, 123')
        self.assertEqual(self.restaurante.latitude, -23.550520)
        self.assertEqual(self.restaurante.longitude, -46.633308)
        self.assertEqual(self.restaurante.owner, self.user)

    def test_restaurante_str_retorna_nome(self): # Testa se a representação do objeto (__str__) retorna o nome do restaurante.
        self.assertEqual(str(self.restaurante), 'Restaurante Exemplo')
