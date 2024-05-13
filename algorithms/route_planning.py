from external_apis.maps_api import api_2gis_get_distances_matrix


# Solving OTSP for three points
def plan_daily_route(place_x, place_y, place_z):
    distances_matrix = api_2gis_get_distances_matrix({'lat': place_x['latitude'], 'lon': place_x['longitude']},
                                                     {'lat': place_y['latitude'], 'lon': place_y['longitude']},
                                                     {'lat': place_z['latitude'], 'lon': place_z['longitude']}, )
    print('Distances matrix: ', distances_matrix)

    for distance in distances_matrix:
        print(distance)

    return distances_matrix
