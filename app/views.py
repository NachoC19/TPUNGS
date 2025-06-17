# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from .layers.services.services import getAllImages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages() 
    favourite_list = []

    grupos_evolutivos = []
    nombres_agregados = set()

    for poke in images:
        if poke.name in nombres_agregados:
            continue

        grupo = services.get_evolution_chain(poke.name)
        grupo_cards = [p for p in images if p.name in grupo]
        if grupo_cards:
            grupos_evolutivos.append(grupo_cards)
            nombres_agregados.update(grupo)

    return render(request, 'home.html', {
        'evoluciones': grupos_evolutivos,
        'favourite_list': favourite_list
    })
# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    if name != '':
        images=services.filterByCharacter(name)
        favourite_list=[]

        return render(request,'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = []
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
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
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')