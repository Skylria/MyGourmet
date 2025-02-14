from django import forms
from .models import Usuario


class RegistroUsuarioForm(forms.ModelForm):
    senha_confirmacao = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = Usuario
        fields = ['nome', 'telefone', 'email', 'senha', 'morador_local', 'cpf']

    def clean_senha_confirmacao(self):
        senha = self.cleaned_data.get("senha")
        senha_confirmacao = self.cleaned_data.get("senha_confirmacao")

        if senha != senha_confirmacao:
            raise forms.ValidationError("As senhas não coincidem")
        return senha_confirmacao
