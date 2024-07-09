from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=150)
    data_nascimento = models.DateField(null=True)
    nacionalidade = models.CharField(max_length=100)
    genero = models.CharField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=9, blank=True, null=True)
    localidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Filme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='filmes')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ano_lancamento = models.PositiveIntegerField(blank=True, null=True)
    duracao_minutos = models.PositiveIntegerField(blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    imagem = models.ImageField(upload_to='filmes/', blank=True, null=True)
    liked = models.ManyToManyField(User, related_name='filmes_liked', blank=True)
    data_adicao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

    @property
    def total_likes_filme(self):
        return self.liked.count()


class Serie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='series')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ano_lancamento = models.PositiveIntegerField(blank=True, null=True)
    temporadas = models.PositiveIntegerField(blank=True, null=True)
    episodios = models.PositiveIntegerField(blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    imagem = models.ImageField(upload_to='series/', blank=True, null=True)
    liked = models.ManyToManyField(User, related_name='series_liked', blank=True)
    data_adicao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

    @property
    def total_likes_serie(self):
        return self.liked.count()


LIKE_CHOICES = (
    ('Like', 'Like'), ('Unlike', 'Unlike'),
)


class Like_serie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True)
    valor = models.CharField(choices=LIKE_CHOICES, default='like_serie', max_length=10)

    def __str__(self):
        return f"{self.user.username} liked {self.serie}"


class Like_filme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, null=True, blank=True)
    valor = models.CharField(choices=LIKE_CHOICES, default='like_serie', max_length=10)

    def __str__(self):
        return f"{self.user.username} liked {self.filme}"


User
class Comentarios_filme(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(default=timezone.now)
    comentario = models.TextField()

    def __str__(self):
        return self.comentario

class Comentarios_serie(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(default=timezone.now)
    comentario = models.TextField()

    def __str__(self):
        return self.comentario