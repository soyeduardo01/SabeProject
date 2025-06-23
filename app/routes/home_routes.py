from flask import Blueprint, render_template, request, redirect, url_for

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template("index.html")

@home_bp.route('/procesar-filtros', methods=['POST'])
def procesar_filtros():
    provincia = request.form.get('provincia')
    genero = request.form.get('genero')
    edad_min = request.form.get('edad_min')
    edad_max = request.form.get('edad_max')
    # Continúa con los demás filtros...

    # Aquí tú aplicas lógica para filtrar los postulantes
    resultados = []  # esto debería venir de una función con lógica real

    return render_template("resultados.html", datos=resultados)
