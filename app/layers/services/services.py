# capa de servicio/lógica de negocio

from ..transport import transport
from app.layers.transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import requests

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    cards=[]
    result=transport.getAllImages()

    if result is None:
        return[]
    
    for p in result:
        card = translator.fromRequestIntoCard(p)
        cards.append(card)
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    return cards

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if name.lower() in card.name.lower():
            filtered_cards.append(card)
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        if type_filter.lower() in [t.lower() for t in card.types]:
            filtered_cards.append(card)
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
def get_evolution_chain(pokemon_name):
    #Obtener species
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/"
    response = requests.get(species_url)
    if not response.ok:
        return []

    species_data = response.json()

    #Obtener URL de la cadena evolutiva
    evo_chain_url = species_data['evolution_chain']['url']
    response = requests.get(evo_chain_url)
    if not response.ok:
        return []

    evo_data = response.json()
    
    #Recorrer la cadena
    chain = evo_data['chain']
    evolution_names = []

    while chain:
        name = chain['species']['name']
        evolution_names.append(name)
        if chain['evolves_to']:
            chain = chain['evolves_to'][0]
        else:
            chain = None

    return evolution_names