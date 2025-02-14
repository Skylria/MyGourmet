from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        print(f"Tentando autenticar com o e-mail: {username}")

        try:
            # Procura o usuário com o e-mail
            user = get_user_model().objects.get(email=username)
            print(f"Usuário encontrado: {user}")
            print(f"Senha fornecida: {password}")
            print(f"Senha criptografada no banco: {user.password}")

            # Verifica a senha com a senha criptografada
            if user.check_password(password):
                print(f"Senha correta para o usuário {username}")
                return user
            else:
                print("Senha incorreta")
                return None  # Retorna None se a senha estiver incorreta
        except get_user_model().DoesNotExist:
            print("Usuário não encontrado")
            return None  # Retorna None se o usuário não existir
