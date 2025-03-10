from django.core.management.base import BaseCommand
from main.models import Usuario  # Importe o modelo Usuario

class Command(BaseCommand):
    help = 'Cria o usuário "rex" para ser o dono padrão de restaurantes externos.'

    def handle(self, *args, **kwargs):
        if not Usuario.objects.filter(email='rex@email.com').exists():  # Verifica se o usuário já existe
            Usuario.objects.create_superuser(
                email='rex@email.com',  # Email do usuário
                nome='rex',  # Nome do usuário
                senha='@rex888@',  # Senha do usuário
                telefone='00000000000',  # Telefone do usuário (pode ser um valor padrão)
                morador_local=True,  # Define como morador local
                cpf='00000000000'  # CPF do usuário (pode ser um valor padrão)
            )
            self.stdout.write(self.style.SUCCESS('Usuário "rex" criado com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Usuário "rex" já existe.'))