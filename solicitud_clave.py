import requests

raza = input("Introduce la raza de gato en ingles: ")

codigo = requests.get("https://api.thecatapi.com/v1/images/search?limit=10&breed_ids="+raza+"&api_key=live_u7HNRzqeBOAtiwurs7IROBki2UYor2vW8bsSGAgJ8kR3QyzRRHTmgzeI6mWtDaCZ", timeout=10)
contenido=codigo.json()

print(codigo)
print(contenido)