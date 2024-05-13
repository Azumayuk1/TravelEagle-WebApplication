import requests as req

from external_apis.api_keys_2gis import api_key_yandex_orgs, api_key_2gis


# Extracts info about features from API response.
# Feature can be any organization, like a cafe or a park.
def extract_features_info(response):
    try:
        # Parsing JSON-response
        data = response

        features = []

        print("Found features: ", data["properties"]["ResponseMetaData"]["SearchResponse"]["found"])

        for (index, feature) in enumerate(data["features"]):
            # Getting the required info
            company_info = {
                "id": feature["properties"]["CompanyMetaData"]["id"],
                "name": feature["properties"]["CompanyMetaData"]["name"],
                "address": feature["properties"]["CompanyMetaData"]["address"],
                "url": feature["properties"]["CompanyMetaData"].get("url", None),
                "categories": [category["name"] for category in
                               feature["properties"]["CompanyMetaData"]["Categories"]],
                "hours": feature["properties"]["CompanyMetaData"].get("Hours", None)
            }
            features.append(company_info)

        return features
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error while extracting info from JSON: {e}")
        return None


def yandex_find_places(search_query: str, longitude: str, latitude: str):
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": api_key_yandex_orgs,
        "text": search_query,
        "lang": "ru_RU",
        "ll": latitude + ',' + longitude,
        "spn": "0.09,0.09",  # 1 kilometer ~~ 0.009
        "results": '10',
        "rspn": "1"
    }

    response = req.get(url, params=params)
    return extract_features_info(response.json())


def yandex_find_eateries(longitude: str, latitude: str):
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": api_key_yandex_orgs,
        "text": 'Где поесть',
        "lang": "ru_RU",
        "ll": latitude + ',' + longitude,
        "spn": "0.009,0.009",  # 1 kilometer ~~ 0.009
        "results": '10',
        "rspn": "1"
    }

    response = req.get(url, params=params)
    return extract_features_info(response.json())


# Function that parses 2GIS JSON response
def parse_2gis_response(response):
    parsed_data = []
    items = response.get('result', {}).get('items', [])

    for item in items:
        parsed_item = {
            'address': item.get('address_name', ''),
            'image': item.get('external_content', [{}])[0].get('main_photo_url', ''),
            'name': item.get('name', ''),
            'id': item.get('id', ''),
            'purpose_name': item.get('purpose_name', ''),
            'general_rating': item.get('reviews', {}).get('general_rating', ''),
            'general_review_count': item.get('reviews', {}).get('general_review_count', ''),
            'description': item.get('full_name', ''),
            'latitude': item.get('point', {}).get('lat', None),
            'longitude': item.get('point', {}).get('lon', None),
        }
        parsed_data.append(parsed_item)

    return parsed_data


def api_2gis_find_places(city_name: str, query: str, page: int, results_per_page: int):
    # Getting id of a city
    url_city_id = 'https://catalog.api.2gis.com/3.0/items'
    params_city_id = {
        "q": city_name,
        "key": api_key_2gis
    }

    city_id = req.get(url_city_id, params=params_city_id).json()['result']['items'][0]['id']
    print('City ID for ', city_name, ' -> ', city_id)

    # Getting places in a city
    url_places = 'https://catalog.api.2gis.com/3.0/items'

    params_places = {
        'q': query,
        'city_id': city_id,
        'key': api_key_2gis,
        'sort': 'relevance',
        'page_size': results_per_page,
        'page': page,
        'fields': 'items.reviews,items.description,items.external_content,items.point',
    }

    places = req.get(url_places, params=params_places).json()
    print('--- Places ---')
    print(places)

    return parse_2gis_response(places)


def parse_distances_matrix_response(response):
    distances = {}
    for route in response.get('routes', []):
        source_id = route.get('source_id')
        target_id = route.get('target_id')
        distance = route.get('distance', 0)
        distances[source_id][target_id] = distance
    return distances


def api_2gis_get_distances_matrix(point_x, point_y, point_z):
    url = 'https://routing.api.2gis.com/get_dist_matrix'

    params = {
        'key': api_key_2gis,
        'version': '2.0'
    }

    # JSON with three points coordinates
    data = {
        "points": [
            {
                "lat": point_x['lat'],
                "lon": point_x['lon']
            },
            {
                "lat": point_y['lat'],
                "lon": point_y['lon']
            },
            {
                "lat": point_z['lat'],
                "lon": point_z['lon']
            },
        ],
        "sources": [0, 1, 2],
        "targets": [0, 1, 2]
    }

    # POST request
    response = req.post(url, json=data, params=params)

    data = response.json()
    routes = []

    for route in data['routes']:
        route_option = {
            'source_id': route.get('source_id'),
            'target_id': route.get('target_id'),
            'distance': route.get('distance', 0)
        }
        routes.append(route_option)

    if response.status_code == 200:
        print("Distance matrix success")
        return routes
    else:
        print("Error:", response.status_code)
        print("Error text:", response.text)
