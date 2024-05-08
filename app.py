from flask import Flask, render_template, request, abort
import requests
from static import funciones

datos_razas=[]

app = Flask(__name__)

@app.route('/')
def inicio():
    codigo = requests.get("https://api.thecatapi.com/v1/images/search?limit=10")
    contenido=codigo.json()
    url_imagenes = []
    for url in contenido:
        url_imagenes.append(url["url"])

    return render_template("inicio.html",imagenes=url_imagenes)


@app.route('/razas')
def razas():
    razas = requests.get("https://api.thecatapi.com/v1/breeds")
    razas_json= razas.json()
    datos_razas.append(razas_json)
    list_raza = []
    for raza in razas_json:
        list_raza.append(raza["name"])
    list_raza.sort()
    return render_template("razas.html",razas_gato=list_raza)



@app.route('/buscador')
def buscador():

    return render_template("buscador.html")

@app.route('/lista', methods=["post"])
def lista():
    raza = requests.form.get('raza')
    for datos in datos_razas:
        if raza == datos["name"]:
            return render_template("lista.html", nombre=datos["name"], enlaces_info=datos["vcahospitals_url"], Temperamento=datos["temperament"],
                                origen=datos["origin"], descripcion=datos["description"], vida=datos["life_span"],relacion_perros=datos["dog_friendly"],
                                imagen=datos["reference_image_id"])
            


@app.route('/detalle/<nombre>')
def cajanombre(nombre):
    for caja in archivo_json:
        if caja["nombre"] == nombre:
            return render_template("detalle.html", nombre=nombre)
    return abort(404)


app.run("0.0.0.0",5000,debug=True)