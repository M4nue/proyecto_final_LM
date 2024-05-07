from flask import Flask, render_template, request, abort
from static import funciones
archivo_json = funciones.cargar_json()
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/buscador')
def buscador():
    return render_template("buscador.html")

@app.route('/lista', methods=["post"])
def lista():
    nombre = request.form.get("Caja")
    descoincidencias_nombres_caja = []
    precio_compra_descoincidencias = []
    precio_venta_descoincidencias = []
    coincidencias =[]
    precio_compra = []
    precio_venta = []

    for caja in archivo_json:
        if nombre == caja["nombre"]:
            return render_template("lista.html", nombre=caja["nombre"], precio_compra=caja["precio_compra"], precio_venta=caja["sale_price_text"])
        
        elif nombre != "":
            
            
            if caja["nombre"].count(nombre) != 0:
                coincidencias.append(caja["nombre"])
                precio_compra.append(caja["precio_compra"])
                precio_venta.append(caja["sale_price_text"])

                #return render_template("lista.html", nombre=caja["nombre"], precio_compra=caja["precio_compra"], precio_venta=caja["sale_price_text"]) 
            else:
                descoincidencias_nombres_caja.append(caja["nombre"])
                precio_compra_descoincidencias.append(caja["precio_compra"])
                precio_venta_descoincidencias.append(caja["sale_price_text"])

        else:
            descoincidencias_nombres_caja.append(caja["nombre"])
            precio_compra_descoincidencias.append(caja["precio_compra"])
            precio_venta_descoincidencias.append(caja["sale_price_text"])

    if len(coincidencias)==0:
        return render_template("lista.html", cajas=descoincidencias_nombres_caja, precio_compra=precio_venta_descoincidencias, precio_venta=precio_venta_descoincidencias) 
    else:
        return render_template("lista.html", cajas=coincidencias,precio_compra=precio_compra,precio_venta=precio_venta) 

@app.route('/detalle/<nombre>')
def cajanombre(nombre):
    for caja in archivo_json:
        if caja["nombre"] == nombre:
            return render_template("detalle.html", nombre=nombre)
    return abort(404)


app.run("0.0.0.0",5000,debug=True)