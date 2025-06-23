from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Favourite
from django.contrib import messages
from django.contrib.auth.models import User

def registrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            messages.error(request, 'Se requiere de usuario y contraseña.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login')
    return render(request, 'registro.html')


def index_page(request):
    return render(request, 'index.html')


def home(request):
    images = services.getAllImages()
    filtro_tipos = [
        {'tipo': 'fire', 'btn': 'danger', 'emoji': '🔥'},
        {'tipo': 'water', 'btn': 'primary', 'emoji': '💧'},
        {'tipo': 'grass', 'btn': 'success', 'emoji': '🌿'}
    ]

    if request.user.is_authenticated:
        favourite_list = Favourite.objects.filter(user=request.user)
        favourite_ids = [str(fav.poke_id) for fav in favourite_list]
        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list,
            'favourite_ids': favourite_ids,
            'filtro_tipos': filtro_tipos
        })

    return render(request, 'home.html', {
        'images': images,
        'filtro_tipos': filtro_tipos
    })


def search(request):
    if request.method == 'POST':
        name = request.POST.get('query', '').strip()
        if name:
            images = services.filterByCharacter(name)
            favourite_list = []
            favourite_ids = []
            if request.user.is_authenticated:
                favourite_list = Favourite.objects.filter(user=request.user)
                favourite_ids = [str(fav.id) for fav in favourite_list]
            return render(request, 'home.html', {
                'images': images,
                'favourite_list': favourite_list,
                'favourite_ids': favourite_ids,
            })
    return redirect('home')


def filter_by_type(request):
    if request.method == "POST":
        tipo = request.POST.get("type")
        images = services.filterByType(tipo)
        favourite_list = []
        favourite_ids = []
        if request.user.is_authenticated:
            favourite_list = Favourite.objects.filter(user=request.user)
            favourite_ids = [str(fav.id) for fav in favourite_list]
        return render(request, "home.html", {
            "images": images,
            "favourite_list": favourite_list,
            "favourite_ids": favourite_ids,
        })
    else:
        return redirect("home")


@login_required
def getAllFavouritesByUser(request):
    favourite_list = Favourite.objects.filter(user=request.user)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    if request.method == 'POST':
        poke_id_str = request.POST.get('id')
        try:
            poke_id = int(poke_id_str)
        except (TypeError, ValueError):
            messages.error(request, "ID de Pokémon inválido.")
            return redirect('buscar')

        exists = Favourite.objects.filter(user=request.user, poke_id=poke_id).exists()
        if not exists:
            Favourite.objects.create(
                poke_id=poke_id,
                name=request.POST.get('name'),
                height=request.POST.get('height'),
                weight=request.POST.get('weight'),
                types=request.POST.get('types'), 
                image=request.POST.get('image'),
                user=request.user
            )
            nombre = request.POST.get('name')
            messages.success(request, f"✔️ Se agregó el pokemon {nombre} a tus favoritos.")
        else:
            messages.info(request, f"El pokemon ya está en tus favoritos.")
    return redirect('buscar')


@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        poke_id = request.POST.get('id')
        favourite = Favourite.objects.filter(user=request.user, id=poke_id).first()
        if favourite:
            nombre = favourite.name
            favourite.delete()
            messages.success(request, f"❌ Se eliminó el pokemon {nombre} de tus favoritos.")
        else:
            messages.error(request, "No se encontró ese favorito.")
    return redirect('favoritos')


@login_required
def exit(request):
    logout(request)
    return redirect('home')

