import os
from dotenv import load_dotenv
import requests

load_dotenv ()
API_KEY=os.getenv('KEY')

raza = input("Introduce la raza de gato en ingles: ")

codigo = requests.get("https://api.thecatapi.com/v1/images/search?limit=3&breed_ids="+raza+"&api_key="+API_KEY, timeout=10)
contenido=codigo.json()

print(codigo)
print(contenido)