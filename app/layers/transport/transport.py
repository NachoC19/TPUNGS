# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config

# comunicación con la REST API.
# este método se encarga de "pegarle" a la API y traer una lista de objetos JSON.
def getAllImages():
    json_collection = []
    for id in range(1, 30):
        try:
            response = requests.get(config.STUDENTS_REST_API_URL + str(id), timeout=5)
            if not response.ok:
                print(f"[transport.py]: error al obtener datos para el id {id}")
                continue

            raw_data = response.json()

            if 'detail' in raw_data and raw_data['detail'] == 'Not found.':
                print(f"[transport.py]: Pokémon con id {id} no encontrado.")
                continue

            json_collection.append(raw_data)

        except requests.exceptions.RequestException as e:
            print(f"[transport.py]: Error al conectar con la API (ID {id}): {e}")
            continue

    return json_collection
# obtiene la imagen correspodiente para un type_id especifico 
def get_type_icon_url_by_id(type_id):
    base_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/'
    return f"{base_url}{type_id}.png"