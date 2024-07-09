from django.urls import include, path
from . import views

app_name = 'siteY'
urlpatterns = [
    path("login/", views.loginview, name="login"),
    path("criarconta/", views.criarconta, name="criarconta"),
    path("homepage/", views.homepage, name="homepage"),
    path("perfil/", views.perfil, name="perfil"),
    path("addfilme/", views.adicionarfilme, name="addfilme"),
    path("addserie/", views.adicionarserie, name="addserie"),
    path("terminarsessao/", views.terminarsessao, name="terminarsessao"),
    path("listar_filmes/", views.listar_filmes, name="listar_filmes"),
    path("listar_series/", views.listar_series, name="listar_series"),
    path('detalhes_filme/<int:filme_id>/', views.detalhes_filme, name='detalhes_filme'),
    path('detalhes_serie/<int:serie_id>/', views.detalhes_serie, name='detalhes_serie'),
    path('<int:serie_id>/like_serie', views.likepost_serie, name="likepost_serie"),
    path('<int:filme_id>/like_filme', views.likepost_filme, name="likepost_filme"),
    path('serie/<int:serie_id>/adicionar_comentario_serie/', views.adicionar_comentario_serie, name="adicionar_comentario_serie"),
    path('filme/<int:filme_id>/adicionar_comentario_filme/', views.adicionar_comentario_filme, name="adicionar_comentario_filme"),
    path("pesquisar/", views.pesquisar, name="pesquisar"),
    path("meus_dados/", views.meus_dados, name="meus_dados"),
    path("meus_gostos/", views.meus_gostos, name="meus_gostos"),
    path("recuperarPassword", views.recuperarPassword, name='recuperarPassword'),
    path("mudarPass", views.mudarPass, name='mudarPass'),
    path("admin/", views.admin, name="admin"),
    path('apagaruser/<int:user_id>/', views.apagaruser, name='apagaruser'),
    path('editar_user/<int:user_id>/', views.editar_user, name='editar_user'),
    path('<int:filme_id>/editar_filme/', views.editar_filme, name='editar_filme'),
    path('<int:serie_id>/editar_serie/', views.editar_serie, name='editar_serie'),
    path('apagar_filme/<int:filme_id>/', views.apagar_filme, name='apagar_filme'),
    path('apagar_serie/<int:serie_id>/', views.apagar_serie, name='apagar_serie'),
]
