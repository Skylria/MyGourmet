import requests
from math import radians, sin, cos, sqrt, atan2
from .models import Restaurante

def calcular_distancia(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    raio_terra_km = 6371.0
    distancia_km = raio_terra_km * c
    distancia_metros = distancia_km * 1000
    return distancia_metros

def buscar_restaurantes_banco(latitude, longitude, raio_maximo=5000):
    todos_restaurantes = Restaurante.objects.all()
    restaurantes_proximos = []

    for restaurante in todos_restaurantes:
        restaurante_lat = restaurante.latitude
        restaurante_lon = restaurante.longitude
        distancia = calcular_distancia(latitude, longitude, restaurante_lat, restaurante_lon)

        if distancia <= raio_maximo:
            restaurante_dict = {
                'id': restaurante.id,  # ID do banco de dados
                'name': restaurante.nome,
                'address': restaurante.endereco,
                'latitude': restaurante.latitude,
                'longitude': restaurante.longitude,
                'media_avaliacoes': restaurante.media_avaliacoes(),  # Média das avaliações
                'total_comentarios': restaurante.total_comentarios(),  # Total de comentários
                'pode_avaliar_comentar': True  # Indica que este restaurante pode ser avaliado/comentado
            }
            restaurantes_proximos.append(restaurante_dict)

    return restaurantes_proximos

def obter_localizacao():
    try:
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        latitude = data.get('lat')
        longitude = data.get('lon')
        return latitude, longitude
    except Exception as e:
        print(f"Erro ao obter localização: {e}")
        return None, None

def obter_restaurantes_proximos(latitude, longitude, raio):
    try:
        query = f"""
        [out:json];
        node["amenity"="restaurant"](around:{raio},{latitude},{longitude});
        out body;
        """
        overpass_url = "http://overpass-api.de/api/interpreter"
        response = requests.get(overpass_url, params={'data': query})
        restaurants = response.json().get('elements', [])

        restaurant_list = []
        for res in restaurants:
            name = res.get('tags', {}).get('name', 'Desconhecido')
            address = res.get('tags', {}).get('addr:street', 'Endereço desconhecido')
            lat = res['lat']
            lon = res['lon']
            if name != 'Desconhecido' and address != 'Endereço desconhecido':
                restaurant_list.append({
                    'id': None,  # Restaurantes da API externa não têm ID
                    'name': name,
                    'address': address,
                    'latitude': lat,
                    'longitude': lon,
                    'media_avaliacoes': None,  # Não há avaliações para restaurantes externos
                    'total_comentarios': 0,  # Não há comentários para restaurantes externos
                    'pode_avaliar_comentar': False  # Indica que este restaurante não pode ser avaliado/comentado
                })

        return restaurant_list
    except Exception as e:
        print(f"Erro ao buscar restaurantes: {e}")
        return []