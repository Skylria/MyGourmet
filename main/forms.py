from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Restaurante

# Formulário de Registro do Usuário
class RegistroUsuarioForm(UserCreationForm):
    senha_confirmacao = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Senha'}),
        label="Confirmar Senha"
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'telefone', 'email', 'morador_local', 'cpf']  # Não inclui 'senha' porque o UserCreationForm já faz isso

    def clean_senha_confirmacao(self):
        senha = self.cleaned_data.get("password1")  # O campo 'password1' é gerenciado pelo UserCreationForm
        senha_confirmacao = self.cleaned_data.get("senha_confirmacao")

        if senha != senha_confirmacao:
            raise forms.ValidationError("As senhas não coincidem")
        return senha_confirmacao


# Formulário de Adição de Restaurante
class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        # Remover o campo 'foto' da lista de campos
        fields = ['nome', 'endereco', 'latitude', 'longitude']