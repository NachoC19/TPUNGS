from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.index_page, name='index-page'),
    path('login/', views.index_page, name='login'),
    path('home/', views.home, name='home'),
    path('registro/', views.registrar_usuario, name='registro'),

    # Buscador y filtros
    path('buscar/', views.search, name='buscar'),
    path('filter_by_type/', views.filter_by_type, name='filter_by_type'),

    # Favoritos
    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    # Logout
    path('exit/', views.exit, name='exit'),
]