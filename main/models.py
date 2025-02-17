from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings

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
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, null=True, blank=True)

    username = None
    email = models.EmailField(unique=True)

    morador_local = models.BooleanField(default=False)
    cpf = models.CharField(max_length=11, null=True, blank=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']  # Outros campos obrigatórios

    def __str__(self):
        return self.email


class RestauranteManager(models.Manager):
    def create_restaurante(self, nome, endereco, latitude, longitude, owner):
        if not nome or not endereco:
            raise ValueError(_('O restaurante deve ter um nome e endereço válidos.'))

        restaurante = self.model(
            nome=nome,
            endereco=endereco,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )
        restaurante.save(using=self._db)
        return restaurante

class Restaurante(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurantes")
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    data_adicao = models.DateTimeField(auto_now_add=True)

    objects = RestauranteManager()

    def __str__(self):
        return self.nome
