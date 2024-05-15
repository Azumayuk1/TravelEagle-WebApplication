from utility.utility import calculate_approximate_travel_time


def parse_place_with_eatery_and_time(place, eatery):
    place_response = {
        'placeId': place['id'],
        'name': place['name'],
        'type': place['purpose_name'] if place['purpose_name'] else 'Место',
        'imageUrl': place['image'],
        'userRating': place['general_rating'],
        'userReviews': place['general_review_count'],
        'likes': place['likes'],
        'website': place['url'],
        'description': place['description'],
        'address': place['address'],
        # 'latitude': obj['latitude'],
        # 'longitude': obj['longitude']
    }

    eatery_response = {
        'placeId': eatery['id'],
        'name': eatery['name'],
        'type': eatery['purpose_name'] if eatery['purpose_name'] else 'Место',
        'imageUrl': eatery['image'],
        'userRating': eatery['general_rating'],
        'userReviews': eatery['general_review_count'],
        'likes': eatery['likes'],
        'website': eatery['url'],
        'description': eatery['description'],
        'address': eatery['address']
    }

    travel_time = calculate_approximate_travel_time(place['travel_distance'])

    return {'place': place, 'eatery': eatery, 'travelTime': travel_time}
