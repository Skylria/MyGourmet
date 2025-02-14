
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import Usuario



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        print(f"Tentando autenticar com o e-mail: {email}")
        print(f"Senha fornecida: {senha}")

        # Tenta autenticar
        user = authenticate(request, username=email, password=senha)

        if user is not None:
            print(f"Usuário autenticado: {user}")
            login(request, user)

            # Verificar se o usuário é morador local
            if user.morador_local:
                return redirect('menu_morador_local')  # Redireciona para o menu de morador local
            else:
                return redirect('menu_turista')  # Redireciona para o menu de turista
        else:
            print("Autenticação falhou.")
            messages.error(request, "Credenciais inválidas. Tente novamente.")

    return render(request, 'login.html')

def registro(request):
    if request.method == 'POST':
        # Pegando os dados do formulário
        nome = request.POST['nome']
        telefone = request.POST['telefone']
        email = request.POST['email']
        senha = request.POST['senha']
        senha_confirmacao = request.POST['senha_confirmacao']
        morador_local = 'morador_local' in request.POST  # Verifica se morador_local foi marcado
        cpf = request.POST.get('cpf', '')  # Se for morador local, o CPF será preenchido

        # Validando se as senhas coincidem
        if senha != senha_confirmacao:
            return render(request, 'registro.html', {'erro': 'As senhas não coincidem'})

        # Criando o usuário com todos os dados
        usuario = Usuario(
            nome=nome,
            telefone=telefone,
            email=email,
            morador_local=morador_local,
            cpf=cpf if morador_local else None  # Atribui CPF somente se for morador local
        )

        # Criptografando a senha
        usuario.set_password(senha)  # Garante que a senha será criptografada

        # Salvando o usuário no banco de dados
        usuario.save()

        # Redirecionando para a página correspondente
        if morador_local:
            return redirect('menu_morador_local')
        else:
            return redirect('menu_turista')

    return render(request, 'registro.html')


# Funções para os menus
def menu_turista(request):
    return render(request, 'menu_turista.html')

def menu_morador_local(request):
    return render(request, 'menu_morador_local.html')
