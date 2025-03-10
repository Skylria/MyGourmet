from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Restaurante, Avaliacao, Comentario

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
        fields = ['nome', 'endereco', 'latitude', 'longitude']


# Formulário de Avaliação
class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota']
        widgets = {
            'nota': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'placeholder': 'Nota (1 a 5)'
            })
        }


# Formulário de Comentário
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Deixe seu comentário...'
            })
        }