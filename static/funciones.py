import os
import json
def cargar_json():
    with open('./static/cajas.json', 'r') as fichero_cajas:
        datos = json.load(fichero_cajas)
    return(datos)