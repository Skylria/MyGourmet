from main.models import Usuario
from geopy.geocoders import Nominatim
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurante
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import render
from .location import buscar_restaurantes_banco, obter_localizacao, obter_restaurantes_proximos
from .forms import RestauranteForm, AvaliacaoForm, ComentarioForm
from django.contrib.auth.models import User


geolocator = Nominatim(user_agent="MyGourmet")

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Tente autenticar o usuário
        print(f"Tentando autenticar com email: {email} e senha: {senha}")  # Depuração do email e senha

        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)  # Realiza o login
            print(f"Usuário autenticado: {request.user}")  # Confirma o usuário após o login

            request.session.save()  # Garante que a sessão seja salva imediatamente
            print(f"Dados da sessão após login: {request.session.items()}")  # Depuração da sessão

            # Pega o parâmetro 'next' da URL (se presente)
            next_page = request.GET.get('next', None)
            print(f"Parâmetro 'next' da URL: {next_page}")  # Depuração do 'next'

            if next_page:
                print(f"Redirecionando para: {next_page}")
                return redirect(next_page)  # Redireciona para a página do parâmetro 'next'
            else:
                # Caso o 'next' não seja encontrado, redireciona para o menu do usuário
                if user.morador_local:
                    print(f"Redirecionando para o menu de morador local.")
                    return redirect('menu_morador_local')  # Se for morador local, redireciona para o menu do morador
                else:
                    print(f"Redirecionando para o menu de turista.")
                    return redirect('menu_turista')  # Se não for, redireciona para o menu do turista
        else:
            print(f"Falha na autenticação. Usuário não encontrado.")  # Depuração de falha de autenticação
            messages.error(request, "Credenciais inválidas. Tente novamente.")  # Mensagem de erro caso as credenciais estejam erradas

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

        # Verificar se o email já está em uso
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'registro.html', {'erro': 'Este email já está em uso'})

        # Verificar se o CPF já está em uso (somente para moradores locais)
        if morador_local and Usuario.objects.filter(cpf=cpf).exists():
            return render(request, 'registro.html', {'erro': 'Este CPF já está cadastrado'})

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

@login_required
def menu_turista(request):
    # Depuração: Verificar se o usuário está autenticado
    if request.user.is_authenticated:
        print(f"O usuário {request.user.username} está autenticado.")
    else:
        print("O usuário NÃO está autenticado.")

    return render(request, 'menu_turista.html')

@login_required
def menu_morador_local(request):
    # Depuração: Verificar se o usuário está autenticado
    if request.user.is_authenticated:
        print(f"O usuário {request.user.username} está autenticado.")
    else:
        print("O usuário NÃO está autenticado.")

    return render(request, 'menu_morador_local.html')

@login_required
def mudar_senha(request):
    if request.user.morador_local:
        menu_url = 'menu_morador_local'
    else:
        menu_url = 'menu_turista'

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Atualiza a sessão do usuário para manter o login após a mudança de senha
            update_session_auth_hash(request, form.user)
            # Redireciona para uma página de sucesso ou de confirmação
            return redirect('senha_mudada_com_sucesso')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'mudar_senha.html', {'form': form, 'menu_url':menu_url})

@login_required
def senha_mudada_com_sucesso(request):
    return render(request, 'senha_mudada_com_sucesso.html')

@login_required
def gerenciar_restaurantes(request):
    # Pegando todos os restaurantes que o usuário logado criou
    user_restaurants = Restaurante.objects.filter(owner=request.user)

    # Se não houver restaurantes, podemos exibir uma mensagem informativa
    if not user_restaurants:
        messages.info(request, "Você ainda não cadastrou nenhum restaurante.")

    return render(request, 'gerenciar_restaurantes.html', {'user_restaurants': user_restaurants})

@login_required
def adicionar_restaurante(request):
    if request.method == 'POST':
        form = RestauranteForm(request.POST)

        if form.is_valid():
            # Associando o restaurante ao usuário logado
            restaurante = form.save(commit=False)
            restaurante.owner = request.user  # O usuário logado será o dono do restaurante
            restaurante.save()
            messages.success(request, "Restaurante adicionado com sucesso!")
            return redirect('gerenciar_restaurantes')  # Redireciona para a página de gerenciamento de restaurantes
        else:
            messages.error(request, "Houve um erro ao adicionar o restaurante. Verifique os dados.")
    else:
        form = RestauranteForm()  # Quando o método for GET, cria um formulário vazio

    return render(request, 'adicionar_restaurante.html', {'form': form})

@login_required
def editar_restaurante(request, id):
    # Buscando o restaurante pelo ID
    restaurante = get_object_or_404(Restaurante, pk=id)

    # Se o método da requisição for POST, significa que o formulário foi enviado
    if request.method == 'POST':
        form = RestauranteForm(request.POST, instance=restaurante)

        if form.is_valid():
            form.save()  # Salva as mudanças feitas no restaurante
            return redirect('gerenciar_restaurantes')  # Redireciona para a página de gerenciamento de restaurantes
    else:
        # Se não for uma requisição POST, apenas renderiza o formulário de edição
        form = RestauranteForm(instance=restaurante)

    return render(request, 'editar_restaurante.html', {'form': form, 'restaurante': restaurante})

@login_required
def remover_restaurante(request, id):
    # Busca o restaurante pelo id
    restaurante = get_object_or_404(Restaurante, pk=id)

    # Exclui o restaurante
    restaurante.delete()

    # Redireciona para a página de gerenciamento de restaurantes após a remoção
    return redirect('gerenciar_restaurantes')

@login_required
def restaurantes_view(request):
    # Obter a localização do usuário
    latitude, longitude = obter_localizacao()

    if request.user.morador_local:
        menu_url = 'menu_morador_local'
    else:
        menu_url = 'menu_turista'

    if latitude is not None and longitude is not None:
        # Obter restaurantes próximos à localização
        restaurants = obter_restaurantes_proximos(latitude, longitude, 5000)
        restaurants_banco = buscar_restaurantes_banco(latitude, longitude, 5000)

        # Criar uma lista com os nomes dos restaurantes do banco de dados
        restaurantes_banco_nomes = [restaurante['name'] for restaurante in restaurants_banco]

        # Passar a localização, restaurantes e URL para o template
        return render(request, 'restaurantes_list.html', {
            'latitude': latitude,
            'longitude': longitude,
            'restaurants': restaurants + restaurants_banco,  # Combina as duas listas
            'restaurantes_banco_nomes': restaurantes_banco_nomes,  # Passa a lista de nomes
            'menu_url': menu_url
        })
    else:
        return JsonResponse({"error": "Não foi possível obter a localização."})

@login_required
def adicionar_avaliacao(request, restaurante_id):
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.restaurante = restaurante
            avaliacao.save()
            messages.success(request, "Avaliação adicionada com sucesso!")
            return redirect('restaurantes_view')
    else:
        form = AvaliacaoForm()

    return render(request, 'adicionar_avaliacao.html', {'form': form, 'restaurante': restaurante})

@login_required
def adicionar_comentario(request, restaurante_id):
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.restaurante = restaurante
            comentario.save()
            messages.success(request, "Comentário adicionado com sucesso!")
            return redirect('restaurantes_view')
    else:
        form = ComentarioForm()

    return render(request, 'adicionar_comentario.html', {'form': form, 'restaurante': restaurante})

@login_required
def ver_avaliacoes_comentarios(request, restaurante_id):
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)
    avaliacoes = restaurante.avaliacoes.all()
    comentarios = restaurante.comentarios.all()

    return render(request, 'ver_avaliacoes_comentarios.html', {
        'restaurante': restaurante,
        'avaliacoes': avaliacoes,
        'comentarios': comentarios
    })

def adicionar_restaurante_externo(request, nome, endereco, latitude, longitude):
    # Obtém o usuário restaurante externo = rex
    rex = Usuario.objects.get(email='rex@email.com')

    # Verifica se o restaurante já existe no banco de dados
    restaurante = Restaurante.objects.filter(
        nome=nome,
        endereco=endereco,
        latitude=latitude,
        longitude=longitude
    ).first()

    # Se não existir, cria um novo restaurante
    if not restaurante:
        restaurante = Restaurante.objects.create(
            nome=nome,
            endereco=endereco,
            latitude=latitude,
            longitude=longitude,
            owner= rex  # Define o dono como o usuário "rex"
        )

    # Redireciona para a página de avaliação
    return redirect('adicionar_avaliacao', restaurante_id=restaurante.id)