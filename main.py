from fastapi import FastAPI
from api_keys import api_key_yandex_orgs

app = FastAPI()


async def make_get_request():
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": "<your_api_key>",
        "text": "<your_text>",
        "lang": "<language_code>",
    }
    response = requests.get(url, params=params)
    return response.json()

response = make_get_request()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
