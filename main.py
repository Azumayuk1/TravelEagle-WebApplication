import redis
import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

from algorithms.recommendations import create_recommendations
from algorithms.route_planning import plan_daily_route
from external_apis.maps_api import api_yandex_get_weather, api_2gis_find_places_nearby
from utility.parsers import parse_place_with_eatery_and_time

print('Connecting to Redis...')
# Connect to Redis
redis_host = 'localhost'
redis_port = 6379  # Default Redis port
redis_db = 0  # Default Redis database
redis_password = 12345  # No password by default

try:
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
    redis_client.ping()
    print('Connected to Redis.')
except:
    print('Failed to connect to Redis.')

print('Starting FastAPI server...')
app = FastAPI()


# response_test = yandex_find_places("Достопримечательность", "59.939119", "30.338029")
# response_eateries_test = yandex_find_eateries("59.939119", "30.338029")
# print('Тестовый запрос --- достопримечательности',response_test)
# print('Тестовый запрос --- кафе',response_eateries_test)

# print('2gis test - attractions', api_2gis_find_places('Санкт-Петербург', 'Достопримечательность'))
# print('2gis test - cafes', api_2gis_find_places('Санкт-Петербург', 'Кафе'))
#
# recommended_places = create_recommendations('Санкт-Петербург', 'Достопримечательность', 'ignored_place',
#                                             'preferred_place')
# print('2GIS after recommendations:', recommended_places)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/get_full_route/")
async def get_full_route(auth: str = '', city_name: str = 'Санкт-Петербург', ignored_place: str = '',
                         preferred_place: str = '', by_car: str = 'true', number_of_days: int = 1, ):
    # Getting places recommendations
    recommended_places_by_days = create_recommendations(city_name, 'Достопримечательность', ignored_place,
                                                        preferred_place,
                                                        number_of_days, redis_client)

    # Planning optimal route for each day
    daily_plans = []  # Plans for all days

    # Trip day - single trip day containing 3 places
    for trip_day in recommended_places_by_days:
        daily_places = plan_daily_route(trip_day[0], trip_day[1], trip_day[2])

        daily_destinations = []
        for place in daily_places:
            # Finding local cafe and restaurant
            eateries_nearby = api_2gis_find_places_nearby(place['latitude'], place['longitude'], 'Кафе')
            print('Found eateries:', eateries_nearby)

            chosen_eatery = eateries_nearby[0]

            eatery_likes = 0
            try:
                eatery_likes = float(redis_client.get(chosen_eatery['id']))
                print('Likes of place ', chosen_eatery['name'], ': ', eatery_likes)
            except Exception:
                print('Redis error: likes unavailable for eatery')

            chosen_eatery['likes'] = eatery_likes

            # Getting destination with place, eatery and approx. time
            destination = parse_place_with_eatery_and_time(place, chosen_eatery)
            daily_destinations.append(destination)

        daily_plans.append({'destinations': daily_destinations})

    # Getting weather alert
    weather_alert = api_yandex_get_weather()

    api_response_content = {
        'weatherWarning': weather_alert,
        'tripDays': daily_plans
    }

    return JSONResponse(content=api_response_content, status_code=200)


@app.get("/like_place/")
async def like_place(auth: str = '', place_id: str = ''):
    # TODO: Check authentication

    # Check if place_id is provided
    if not place_id:
        return {"error": "Please provide a place ID."}

    # Increase likes for the place_id by 1
    try:
        likes = redis_client.incr(place_id)
        return {"response": f"Successfully liked place {place_id}. Total likes: {likes}", "status": "200 ok"}
    except redis.exceptions.ResponseError as e:
        return {"error": f"Failed to like place {place_id}: {str(e)}", "status": "500 error"}


uvicorn.run(app, host='0.0.0.0', port=8000)
