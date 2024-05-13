import redis
import uvicorn
from fastapi import FastAPI

from algorithms.recommendations import create_recommendations
from algorithms.route_planning import plan_daily_route

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
                         preferred_place: str = '', by_car: str = 'true', number_of_days: int = 3, ):
    recommended_places_by_days = create_recommendations(city_name, 'Достопримечательность', ignored_place,
                                                        preferred_place,
                                                        number_of_days, redis_client)

    daily_plans = []

    for trip_day in recommended_places_by_days:
        daily_plans.append(plan_daily_route(trip_day[0], trip_day[1], trip_day[2]))

    return daily_plans


@app.get("/like_place/")
async def like_place(auth: str = '', place_id: str = ''):
    # TODO: Check authentication

    # Check if place_id is provided
    if not place_id:
        return {"error": "Please provide a place ID."}

    # Increase likes for the place_id by 1
    try:
        likes = redis_client.incr(place_id)
        return {"response": f"Successfully liked place {place_id}. Total likes: {likes}"}
    except redis.exceptions.ResponseError as e:
        return {"error": f"Failed to like place {place_id}: {str(e)}"}


uvicorn.run(app, host='0.0.0.0', port=8000)
