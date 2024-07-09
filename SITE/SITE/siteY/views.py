from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from .models import Perfil, Filme, Serie, Like_filme, Like_serie, Comentarios_filme, Comentarios_serie


# Create your views here.
def loginview(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('siteY:homepage'))
        else:
            context = {
                'error_message': "Email ou senha incorretos!",
            }
            return render(request, 'siteY/oi.html', context)
    else:
        return render(request, 'siteY/oi.html')



def criarconta(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Email = request.POST['Email']
        Password = request.POST['Password']
        PrimeiroNome = request.POST['PrimeiroNome']
        UltimoNome = request.POST['UltimoNome']
        Nacionalidade = request.POST['Nacionalidade']
        Genero = request.POST['Genero']
        DataNascimento = request.POST['DataNascimento']


        try:
            user = User.objects.create_user(username=Username, email=Email, password=Password, first_name=PrimeiroNome,
                                            last_name=UltimoNome)
            p = Perfil(user=user, nacionalidade=Nacionalidade, genero=Genero, data_nascimento=DataNascimento)
            p.save()
            return HttpResponseRedirect(reverse('siteY:login'))
        except IntegrityError:
            messages.error(request, 'O Email escolhido já está a ser utilizado. Por favor escolha outro Email')
            return render(request, 'siteY/criarconta.html')

    else:
        return render(request, 'siteY/criarconta.html')



def homepage(request):
    last_added_movies = Filme.objects.order_by('-data_adicao')[:6]
    last_added_series = Serie.objects.order_by('-data_adicao')[:6]
    return render(request, 'siteY/homepage.html', {'last_added_movies': last_added_movies, 'last_added_series': last_added_series})

@login_required(login_url='/siteY/login')
def perfil(request):
    user = request.user
    filmes = Filme.objects.filter(user=user)
    series = Serie.objects.filter(user=user)
    return render(request, 'siteY/perfil.html', {'user': user, 'filmes': filmes, 'series': series})


@login_required(login_url='/siteY/login')
def meus_dados(request):
    user = request.user
    pessoa = user.perfil  # Supondo que o perfil esteja associado ao usuário dessa maneira

    if request.method == 'POST':
        user.email = request.POST.get('Email')
        user.first_name = request.POST.get('PrimeiroNome')
        user.last_name = request.POST.get('UltimoNome')

        password = request.POST.get('Password')
        if password:
            user.set_password(password)
        user.save()

        pessoa.nacionalidade = request.POST.get('Nacionalidade')
        pessoa.contacto = request.POST.get('Contacto')
        pessoa.localidade = request.POST.get('Localidade')
        pessoa.save()

        messages.success(request, 'Alterações gravadas com sucesso!')
        return redirect('siteY:meus_dados')

    return render(request, 'siteY/meus_dados.html', {'user': user, 'pessoa': pessoa})


def meus_gostos(request):
    user = request.user
    filmes_curtidos = Filme.objects.filter(liked=user)
    series_curtidas = Serie.objects.filter(liked=user)
    return render(request, 'siteY/meus_gostos.html', {'filmes_curtidos': filmes_curtidos, 'series_curtidas': series_curtidas})

@login_required(login_url='/siteY/login')
def adicionarfilme(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        ano = request.POST.get('ano')
        duracao = request.POST.get('duracao')
        genero = request.POST.get('genero')
        img = request.FILES['imagem']
        filme = Filme(titulo=titulo, descricao=descricao, ano_lancamento=ano, duracao_minutos=duracao, genero=genero, imagem=img)
        filme.user = request.user
        filme.save()

        return render(request, 'siteY/homepage.html')

    return render(request, 'siteY/addfilme.html')

@login_required(login_url='/siteY/login')
def adicionarserie(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        ano = request.POST.get('ano')
        temporadas = request.POST.get('temporadas')
        episodios = request.POST.get('episodios')
        genero = request.POST.get('genero')
        img = request.FILES['imagem']
        serie = Serie(titulo=titulo, descricao=descricao, ano_lancamento=ano, temporadas=temporadas, episodios=episodios, genero=genero, imagem=img)
        serie.user = request.user
        serie.save()

        return render(request, 'siteY/homepage.html')

    return render(request, 'siteY/addserie.html')

def terminarsessao(request):
    logout(request)
    return HttpResponseRedirect(reverse('siteY:login'))

def listar_filmes(request):
    filmes = Filme.objects.all().order_by('-data_adicao')
    return render(request, 'siteY/listar_filmes.html', {'filmes': filmes})

def listar_series(request):
    series = Serie.objects.all().order_by('-data_adicao')
    return render(request, 'siteY/listar_series.html', {'series': series})


def detalhes_filme(request, filme_id):
    filme = get_object_or_404(Filme, pk=filme_id)
    return render(request, 'siteY/detalhes_filme.html', {'filme': filme})

def detalhes_serie(request, serie_id):
    serie = get_object_or_404(Serie, pk=serie_id)
    return render(request, 'siteY/detalhes_serie.html', {'serie': serie})

@login_required
def likepost_serie(request, serie_id):
    try:
        serie_selecionada = Serie.objects.get(pk=serie_id)
    except Serie.DoesNotExist:
        return HttpResponseNotFound("Série não encontrada.")

    if request.method == 'POST':
        user = request.user
        if user in serie_selecionada.liked.all():
            serie_selecionada.liked.remove(user)
        else:
            serie_selecionada.liked.add(user)
        like_serie, created = Like_serie.objects.get_or_create(user=user, serie_id=serie_id)
        if not created:
            if like_serie.valor == 'Like':
                like_serie.valor = 'Unlike'
            else:
                like_serie.valor = 'Like'
            like_serie.save()
        return HttpResponseRedirect(reverse('siteY:detalhes_serie', args=[serie_id]))


@login_required
def likepost_filme(request, filme_id):
    try:
        filme_selecionado = Filme.objects.get(pk=filme_id)
    except Filme.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado.")

    if request.method == 'POST':
        user = request.user
        if user in filme_selecionado.liked.all():
            filme_selecionado.liked.remove(user)
        else:
            filme_selecionado.liked.add(user)
        like_filme, created = Like_filme.objects.get_or_create(user=user, filme_id=filme_id)
        if not created:
            if like_filme.valor == 'Like':
                like_filme.valor = 'Unlike'
            else:
                like_filme.valor = 'Like'
            like_filme.save()
        return HttpResponseRedirect(reverse('siteY:detalhes_filme', args=[filme_id]))


@login_required
def adicionar_comentario_filme(request, filme_id):
    filme = get_object_or_404(Filme, pk=filme_id)

    if request.method == 'POST':
        com = request.POST['comentario']

        if com.strip():  # Verifica se o campo de comentário contém algum texto
            comentario = Comentarios_filme(user=request.user, filme=filme, comentario=com)
            comentario.save()
        else:
            messages.error(request, 'Digite pelo menos uma letra antes de comentar.')

    return HttpResponseRedirect(reverse('siteY:detalhes_filme', args=[filme_id]))

@login_required
def adicionar_comentario_serie(request, serie_id):
    serie = get_object_or_404(Serie, pk=serie_id)

    if request.method == 'POST':
        com = request.POST['comentario']

        if com.strip():  # Verifica se o campo de comentário contém algum texto
            comentario = Comentarios_serie(user=request.user, serie=serie, comentario=com)
            comentario.save()
        else:
            messages.error(request, 'Digite pelo menos uma letra antes de comentar.')

    return HttpResponseRedirect(reverse('siteY:detalhes_serie', args=[serie_id]))

def pesquisar(request):
    query = request.GET.get('q')
    filmes = Filme.objects.filter(titulo__icontains=query)
    series = Serie.objects.filter(titulo__icontains=query)
    return render(request, 'siteY/pesquisar.html', {'filmes': filmes, 'series': series})

def recuperarPassword(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Email = request.POST['Email']

        user = User.objects.filter(username=Username, email=Email).first()
        if user:
            if User.objects.filter(username=Username).exists():

                html_message = render_to_string('siteY/mudarPassmail.html', {'username': Username})
                plain_message = strip_tags(html_message)

                send_mail(
                    'Mudança de Password',
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [Email],
                    html_message=html_message,
                    fail_silently=False,
                )
                messages.success(request, 'E-mail de recuperação enviado com sucesso!')
                return HttpResponseRedirect(reverse('siteY:recuperarPassword'))
            else:
                messages.error(request, 'O utilizador que inseriu não existe!')
                return HttpResponseRedirect(reverse('siteY:recuperarPassword'))
        else:
            messages.error(request, 'O utilizador e o email introduzidos não correspondem!')
            return HttpResponseRedirect(reverse('siteY:recuperarPassword'))
    else:
        return render(request, 'siteY/recuperarPassword.html')

def mudarPass(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Password = request.POST['Password']
        try:
            user = User.objects.get(username=Username)
            user.set_password(Password)
            user.save()
            messages.success(request, 'Password atualizada com sucesso!')
            return HttpResponseRedirect(reverse('siteY:login'))
        except User.DoesNotExist:
            messages.error(request, 'Utilizador não existe!')
            return HttpResponseRedirect(reverse('popaction:mudarPass'))
    return render(request, 'siteY/mudarPass.html')


def admin(request):
    if not request.user.is_superuser:
        # Se o usuário não for um superusuário, redirecione para outra página ou retorne um erro.
        return HttpResponseForbidden("Apenas administradores podem acessar esta página.")

    # Obtenha todos os usuários e suas publicações
    users = User.objects.all()
    filmes = Filme.objects.all()
    series = Serie.objects.all()

    return render(request, 'siteY/admin.html', {'users': users, 'filmes': filmes, 'series': series})

@login_required
def apagaruser(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, 'Utilizador eliminado com sucesso!')
        return HttpResponseRedirect(reverse('siteY:admin'))
    else:
        # Se a solicitação não for POST, redirecione para algum lugar adequado ou retorne um erro
        return HttpResponseNotAllowed(['POST'])



def editar_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    pessoa = user.perfil

    if request.method == 'POST':
        if 'username' in request.POST and 'email' in request.POST:
            user.username = request.POST['Username']
            user.email = request.POST['Email']
            user.first_name = request.POST.get('PrimeiroNome')
            user.last_name = request.POST.get('UltimoNome', '')  # Valor padrão vazio se não estiver presente

            password = request.POST.get('Password')
            if password:
                user.set_password(password)
            user.save()

            # Se houver outros campos a serem salvos, faça o mesmo para eles

            pessoa.nacionalidade = request.POST.get('Nacionalidade', '')  # Valor padrão vazio se não estiver presente
            pessoa.save()

            messages.success(request, 'Alterações gravadas com sucesso!')
            return redirect('siteY:admin', user_id=user_id)

    return render(request, 'siteY/editar_user.html', {'user': user, 'pessoa': pessoa})

def editar_filme(request, filme_id):
    filme = get_object_or_404(Filme, pk=filme_id)
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        ano = request.POST['ano']
        duracao = request.POST['duracao']
        genero = request.POST['genero']
        img = request.FILES.get('imagem')

        filme.titulo = titulo
        filme.descricao = descricao
        filme.ano_lancamento = ano
        filme.duracao_minutos = duracao
        filme.genero = genero
        if img:
            filme.imagem = img

        filme.save()
        return HttpResponseRedirect(reverse('siteY:editar_filme', args=[filme_id]))
    else:
        return render(request, 'siteY/editar_filme.html', {'filme': filme})

def editar_serie(request, serie_id):
    serie = get_object_or_404(Serie, pk=serie_id)
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        ano = request.POST['ano']
        temporadas = request.POST['temporadas']
        episodios = request.POST['episodios']
        genero = request.POST['genero']
        img = request.FILES.get('imagem')

        serie.titulo = titulo
        serie.descricao = descricao
        serie.ano_lancamento = ano
        serie.temporadas = temporadas
        serie.episodios = episodios
        serie.genero = genero
        if img:
            serie.imagem = img

        serie.save()
        return HttpResponseRedirect(reverse('siteY:editar_serie', args=[serie_id]))
    else:
        return render(request, 'siteY/editar_serie.html', {'serie': serie})


def apagar_filme(request, filme_id):
    filme = get_object_or_404(Filme, pk=filme_id)

    if request.method == 'POST':
        filme.delete()
        return redirect('siteY:admin')

    return render(request, 'SiteY/admin.html', {'filme': filme})


def apagar_serie(request, serie_id):
    serie = get_object_or_404(Serie, pk=serie_id)

    if request.method == 'POST':
        serie.delete()
        return redirect('siteY:admin')

    return render(request, 'SiteY/admin.html', {'serie': serie})