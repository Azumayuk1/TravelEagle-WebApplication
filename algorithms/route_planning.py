import itertools

from external_apis.maps_api import api_2gis_get_distances_matrix


def calculate_total_distance(path, distances):
    total_distance = 0
    for i in range(len(path) - 1):
        for item in distances:
            if (item['source_id'] == path[i] and item['target_id'] == path[i + 1]) or \
                    (item['source_id'] == path[i + 1] and item['target_id'] == path[i]):
                total_distance += item['distance']
                break
    return total_distance


def find_shortest_path(distances):
    points = set(item['source_id'] for item in distances)
    shortest_distance = float('inf')
    shortest_path = None

    for perm in itertools.permutations(points):
        distance = calculate_total_distance(perm, distances)
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_path = perm

    return shortest_path, shortest_distance


# Solving OTSP for three points
def plan_daily_route(place_x, place_y, place_z):
    distances_matrix = api_2gis_get_distances_matrix({'lat': place_x['latitude'], 'lon': place_x['longitude']},
                                                     {'lat': place_y['latitude'], 'lon': place_y['longitude']},
                                                     {'lat': place_z['latitude'], 'lon': place_z['longitude']}, )
    print('Distances matrix: ', distances_matrix)

    places_with_indexes = {
        0: place_x,
        1: place_y,
        2: place_z,
    }

    optimal_places_route = []

    # Find the shortest path
    shortest_path, shortest_distance = find_shortest_path(distances_matrix)
    print(f'Shortest_path: {shortest_path}, Shortest_distance:{shortest_distance}')

    for place_index in shortest_path:
        place = places_with_indexes[place_index]
        if place_index == shortest_path[0]:
            place['travel_distance'] = 0
        else:
            place['travel_distance'] = shortest_distance
        optimal_places_route.append(place)

    print('Debug: finished optimal route of recommended places')
    for index, place in enumerate(optimal_places_route):
        print(f"{index}. {place['name']}")

    return optimal_places_route
