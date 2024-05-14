from flask import Flask, render_template, abort, request
import requests
import json

app = Flask(__name__)
datos_razas=[]


@app.route('/')
def razas():
    datos_razas.clear()
    razas = requests.get("https://api.thecatapi.com/v1/breeds")
    razas_json= razas.json()

    for raza in razas_json:
        datos_razas.append(raza)

    list_raza = []
    list_id= []
    for raza in razas_json:
        list_raza.append(raza["name"])
        list_id.append(raza["id"])
    list_raza.sort()

    
    return render_template("inicio.html",razas_gato=list_raza, id=list_id)


@app.route('/10img')
def inicio():
    codigo = requests.get("https://api.thecatapi.com/v1/images/search?limit=10")
    contenido=codigo.json()
    url_imagenes = []

    for url in contenido:
        url_imagenes.append(url["url"])

    return render_template("10img.html",imagenes=url_imagenes)


@app.route('/buscador')
def buscador():
    raza = request.args.get('raza', '') 
    valor=print(raza)
    return render_template("buscador.html",nombre=valor, raza=raza)

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
    for raza in datos_razas :
        if raza["id"] == id:
            return render_template("detalle.html", nombre=raza["name"],descripcion=raza["description"],imagen=raza["reference_image_id"])
    return abort(404)


app.run("0.0.0.0",5000,debug=True)