from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="clases"
        )
        print("Conexión a MySQL exitosa")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def fetch_all_personas():
    connection = create_connection()
    if connection is None:
        return []
    query = "SELECT * FROM personas"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.before_request
def before_request():
    print('Antes de la petición...')

@app.after_request
def after_request(response):
    print('Después de la petición')
    return response

@app.route('/')
def index():
    personas = fetch_all_personas()
    data = {
        'personas': personas,
        'titulo': 'Lista de Personas',
        'bienvenida': 'Bienvenidos a la lista de personas'
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)

@app.route('/query_string')
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return 'ok'

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
