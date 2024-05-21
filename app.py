from flask import Flask, render_template, abort, request
import requests
import os
from dotenv import load_dotenv
import random

app = Flask(__name__)
datos_razas=[]
url_todo="https://api.thecatapi.com/v1/breeds"
url_key="https://api.thecatapi.com/v1/images/search?limit=10&breed_ids="
url_ramdom="https://api.thecatapi.com/v1/images/search?limit=10"

load_dotenv ()
API_KEY=os.getenv('KEY')

def divide_chunks(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i:i + n]




@app.route('/')
def inico():
    datos_razas.clear()
    razas = requests.get(url_todo)
    razas_json= razas.json()

    for raza in razas_json:
        datos_razas.append(raza)

    list_raza = []
    list_id = []
    for raza in datos_razas:
        list_raza.append(raza["name"])
        list_id.append(raza["id"])


    # Paginación
    pagina = request.args.get('page', 1, type=int)
    tamano_pagina = 15
    paginas_razas = list(divide_chunks(list_raza, tamano_pagina))
    raza_paginada = paginas_razas[pagina - 1]

    return render_template("inicio.html", razas_gato=raza_paginada, id=list_id, paginas=len(paginas_razas))


@app.route('/adivina')
def adivina():
    while True:
        posicion_aleatoria = random.randint(1, len(datos_razas) - 1)
        raza_acertada = datos_razas[posicion_aleatoria]
        
        if "reference_image_id" in raza_acertada:
            nombre = raza_acertada["name"]
            id_raza = raza_acertada["id"]
            imagen_raza = raza_acertada["reference_image_id"]
            break
        else:
            print(f"reference_image_id no encontrado en {raza_acertada}")

    nombres = []
    if posicion_aleatoria > 0:
        nombres.append(datos_razas[posicion_aleatoria - 1]["name"])
    if posicion_aleatoria < len(datos_razas) - 1:
        nombres.append(datos_razas[posicion_aleatoria + 1]["name"])

    nombres.insert(random.randint(0, len(nombres)), nombre)

    return render_template("adivina.html", lista=nombres, imagen=imagen_raza, id=id_raza, nombre_correcto=nombre)



@app.route('/verificar_respuesta', methods=['POST'])
def verificar_respuesta():
    seleccion = request.form['seleccion']
    id_correcto = request.form['id_correcto']
    nombre_correcto = request.form['nombre_correcto']

    if seleccion == nombre_correcto:
        mensaje = "OK"
    else:
        mensaje = "Fallo"

    return render_template("resultado.html", mensaje=mensaje)


@app.route('/buscador')
def buscador():
    raza = request.args.get('raza', '') 
    razas_nombre = []
    for i in datos_razas:
        razas_nombre.append(i["name"])
    return render_template("buscador.html", razas=razas_nombre)

@app.route('/lista', methods=["post"])
def lista():
    raza = request.form.get('raza')
    for datos in datos_razas:
        if raza == datos["name"]:
            enlaces_info = datos["vetstreet_url"] if "vetstreet_url" in datos else "No disponible"
            return render_template("lista.html",nombre=datos["name"],enlaces_info=enlaces_info,Temperamento=datos["temperament"],
                                origen=datos["origin"],descripcion=datos["description"],vida=datos["life_span"],
                                relacion_perros=datos["dog_friendly"],imagen=datos["reference_image_id"])
    return abort(404)


@app.route('/detalle/<id>')
def razaid(id):
    for raza in datos_razas:
        if raza["id"] == id:
            imagenes_get = requests.get(url_key + raza["id"] + "&api_key=" + API_KEY, timeout=10)
            imagenes_json = imagenes_get.json()
            url_imagenes = []
            for imagen in imagenes_json:
                url_imagenes.append(imagen["url"])
            return render_template("detalle.html", nombre=raza["name"], descripcion=raza["description"], imagenes=url_imagenes)
    return abort(404)


@app.route('/galeria')
def imagenes_aleatorias():
    img=requests.get(url_ramdom)
    img=img.json()
    url=[]
    for imagen in img:
        url.append(imagen["url"])
    
    return render_template('galería.html',imagenes=url)


app.run("0.0.0.0",5000,debug=True)