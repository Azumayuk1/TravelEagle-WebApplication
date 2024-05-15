from redis import Redis

from external_apis.maps_api import api_2gis_find_places


def create_recommendations(city_name, query, ignored_place_types, preferred_place_types, number_of_days: int,
                           redis_client: Redis):
    days_with_top_places = []
    results_per_place = 5

    for day in range(1, number_of_days + 1):
        places = api_2gis_find_places(city_name, query, day, results_per_place)

        places_with_weights = []

        for place in places:
            # Calculating weight according to algorithm

            # Importance of each factor
            s_rating = 1
            s_reviews = 0.1
            s_likes = 0.2

            # Initial weight
            w0 = 1

            # Weight depending on ignored/preferred types
            if place['purpose_name'] in ignored_place_types:
                w1 = 0
            elif place['purpose_name'] in preferred_place_types:
                w1 = 2
            else:
                w1 = 1

            # Weight - rating
            w2 = place['general_rating'] * s_rating

            # Weight - reviews amount
            w3 = place['general_review_count'] * s_reviews

            # Weight - amount of likes in Redis database
            likes = 0
            try:
                likes = float(redis_client.get(place['id']))
                print('Likes of place ', place['name'], ': ', likes)
            except Exception:
                print('Redis error: likes unavailable')

            w4 = likes * s_likes

            # Additionally adding amount of likes to place
            place['likes'] = likes

            place_weight = w1 * (w0 + (w2 * w3) + w4)

            place_with_weight = {
                'place': place,
                'weight': place_weight
            }

            places_with_weights.append(place_with_weight)

        # Sorting places by their weights in descending order
        places_with_weights.sort(key=lambda x: x['weight'], reverse=True)

        # Print top places for debug
        for index, place_with_weight in enumerate(places_with_weights[:3], start=1):
            place_name = place_with_weight['place']['name']
            weight = place_with_weight['weight']
            print(f"{index}. {place_name}: {weight:.2f}")

        # Selecting only the top places
        daily_top_places = []
        for place in places_with_weights[:3]:
            daily_top_places.append(place['place'])

        days_with_top_places.append(daily_top_places)

    return days_with_top_places
