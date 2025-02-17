from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import logging

# Configuração de log
logger = logging.getLogger(__name__)

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Log para verificar quando o método é chamado
        logger.debug(f"Tentando autenticar com e-mail: {username} e senha: {password}")

        try:
            # Procura o usuário pelo e-mail
            user = get_user_model().objects.get(email=username)
            logger.debug(f"Usuário encontrado: {user}")

            # Verifica se a senha está correta
            if user.check_password(password):
                logger.debug(f"Senha correta para o usuário: {user.email}")
                return user  # Retorna o usuário se a senha estiver correta
            else:
                logger.debug(f"Senha incorreta para o usuário: {user.email}")
                return None  # Retorna None se a senha estiver incorreta

        except get_user_model().DoesNotExist:
            logger.debug(f"Usuário não encontrado com o e-mail: {username}")
            return None  # Retorna None se o usuário não existir

    def get_user(self, user_id):
        try:
            # Tenta recuperar o usuário pelo ID
            user = get_user_model().objects.get(pk=user_id)
            logger.debug(f"Usuário recuperado com ID {user_id}: {user}")
            return user
        except get_user_model().DoesNotExist:
            logger.debug(f"Usuário não encontrado com ID {user_id}")
            return None
