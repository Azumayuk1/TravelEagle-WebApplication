from fastapi import FastAPI

from external_apis.yandex_api import yandex_find_places, yandex_find_eateries, yandex_get_distances_matrix, yandex_get_weather_alert

app = FastAPI()

response_test = yandex_find_places("Достопримечательность", "59.939119", "30.338029")
response_eateries_test = yandex_find_eateries("59.939119", "30.338029")



print('Тестовый запрос --- достопримечательности',response_test)
print('Тестовый запрос --- кафе',response_eateries_test)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
