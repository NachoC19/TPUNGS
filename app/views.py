# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from .layers.services.services import getAllImages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Favourite
from django.contrib import messages #SE importa para enviar el mensaje de ya esta en favoritos

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    # Definir favoritos del usuario en una lista convertida en id para poder mostrar el boton de que el favorito ya existe (modificado en home.html tambien)
    favourite_list = Favourite.objects.filter(user=request.user)
    favourite_ids = [str(fav.id) for fav in favourite_list]
    filtro_tipos = [
    {'tipo': 'fire', 'btn': 'danger', 'emoji': '🔥'},
    {'tipo': 'water', 'btn': 'primary', 'emoji': '💧'},
    {'tipo': 'grass', 'btn': 'success', 'emoji': '🌿'}
]

    return render(request, 'home.html', {
    'images': images,
    'favourite_list': favourite_list,
    'favourite_ids': favourite_ids,
    'filtro_tipos': filtro_tipos
})
# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    if name != '':
        images = services.filterByCharacter(name)
        favourite_list = Favourite.objects.filter(user=request.user)
        favourite_ids = [str(fav.id) for fav in favourite_list]
        return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list,
        'favourite_ids': favourite_ids,  
        })
    return redirect('home')
# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    if request.method == "POST":
        type = request.POST.get("type")
        images = services.filterByType(type)
        favourite_list = []

        return render(request, "home.html", { "images": images, "favourite_list": favourite_list })
    else:
        return redirect("home")

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
# Aca desarrolle la funcion de getallfavouritesbyuser, use el if porque a veces encontraba errores con el tema del objeto favourite , tambien se anadio el import .models favourite
#ya que mostraba error de favourite no esta definido
def getAllFavouritesByUser(request):
    if request.method=='GET': 
        favourite_list = Favourite.objects.filter(user=request.user)
        return render(request, 'favourites.html', {'favourite_list': favourite_list})
    else:
        return redirect('home')
#desarrollo de la funcion guardar un favorito para la cual ya hay un boton, se uso el import message para dar el mensaje de favorito agregado y favorito pre existente 
#Luego de desarrollar el boton dinamico, ya no es necesario el mensaje de favorito pre existente y se elimino el messages.warning
@login_required
def saveFavourite(request):
    if request.method == 'POST':
        Favourite.objects.create(
            id=request.POST.get('id'),
            name=request.POST.get('name'),
            height=request.POST.get('height'),
            weight=request.POST.get('weight'),
            types=request.POST.getlist('types[]'),  
            image=request.POST.get('image'),
            user=request.user
        )
        nombre=request.POST.get('name')
        messages.success(request, f"✔️ Se agrego el pokemon {nombre} a tus favoritos.")
    return redirect('buscar')
@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        poke_id = request.POST.get('id')  
        favourite = Favourite.objects.filter(user=request.user, id=poke_id).first()
        nombre = favourite.name  
        Favourite.objects.filter(user=request.user, id=poke_id).delete()
        messages.success(request, f"❌ Se elimino el pokemon {nombre} de tus favoritos.")
    return redirect('favoritos')  
@login_required
def exit(request):
    logout(request)
    return redirect('home')