from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, senha=None, telefone=None, morador_local=False, cpf=None):
        if not email:
            raise ValueError('O usuário deve ter um email válido.')
        usuario = self.model(
            email=email,
            nome=nome,
            telefone=telefone,
            morador_local=morador_local,
            cpf=cpf if morador_local else None
        )
        usuario.set_password(senha)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nome, senha=None, telefone=None, morador_local=False, cpf=None):
        usuario = self.create_user(
            email=email,
            nome=nome,
            senha=senha,
            telefone=telefone,
            morador_local=morador_local,
            cpf=cpf
        )
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, null=True, blank=True)  # Para telefone
    morador_local = models.BooleanField(default=False)  # Indica se é morador local
    cpf = models.CharField(max_length=11, null=True, blank=True)  # CPF, opcional para turistas
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']  # Outros campos obrigatórios

    def __str__(self):
        return self.email
