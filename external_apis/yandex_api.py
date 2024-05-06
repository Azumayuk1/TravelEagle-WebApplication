from api_keys_yandex import api_key_yandex_orgs
import requests as req
import json


def parse_response(json_data):
    response_data = json.loads(json_data)

    # Получаем метаданные запроса и ответа
    response_metadata = response_data['properties']['ResponseMetaData']['SearchResponse']

    # Получаем информацию о найденных объектах
    found_objects = response_data['features']

    # Возвращаем нужные данные в удобной форме
    return {
        'found': response_metadata['found'],
        'boundedBy': response_metadata['boundedBy'],
        'display': response_metadata['display'],
        'objects': found_objects
    }


def yandex_find_places(search_query: str, longitude: str, latitude: str):
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": api_key_yandex_orgs,
        "text": search_query,
        "lang": "ru_RU",
        "ll": latitude + ',' + longitude,
        "spn": "0.09,0.09", # 1 kilometer ~~ 0.009
        "results": '10'
    }

    response = req.get(url, params=params)
    return response.json()


def yandex_find_eateries(longitude: str, latitude: str):
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": api_key_yandex_orgs,
        "text": 'Где поесть',
        "lang": "ru_RU",
        "ll": latitude + ',' + longitude,
        "spn": "0.009,0.009",  # 1 kilometer ~~ 0.009
        "results": '10'
    }

    response = req.get(url, params=params)
    return response.json()


def yandex_get_distances_matrix():
    pass


def yandex_get_weather_alert(date: str):
    pass
