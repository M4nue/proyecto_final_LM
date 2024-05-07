import requests

codigo = requests.get("https://api.thecatapi.com/v1/images/search", timeout=10)
contenido=codigo.json()

print(codigo)
print(contenido)