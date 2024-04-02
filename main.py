from flask import Flask, render_template
import src.main.mergesort
import src.main.quicksort

#va a buscar en el modulo principal de nuestra app (plantillas en templates)
app = Flask(__name__)

@app.route('/')
def index():
    name = None
    list= ['e1','e2','e3']
    return render_template('inicio.html', name = name, list = list)

#string
@app.route('/hello')
@app.route('/hello/<name>')
@app.route('/hello/<name>/<int:age>')
def hello(name = None, age = None):
    if name == None and age == None:
        return 'Hola Mundo!'
    elif age == None:
        return f'Hola, {name}'
    else:
        return f'Hola, {name} tienes {age} años!'

#int
#path

from markupsafe import escape # para poner un path que lo muestre y no lo ejecute
@app.route('/code/<path:code>')
def code(code):
    return f'<code>{escape(code)}</code>'