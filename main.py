from flask import Flask, request, render_template, url_for,send_file, redirect
import src.main.mergesort
import src.main.quicksort
import src.main.heapsort

#va a buscar en el modulo principal de nuestra app (plantillas en templates)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'src'

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/mergesort')
def mergesort():
    return render_template('mergesort.html')
@app.route('/quicksort')
def quicksort():
    return render_template('quicksort.html')

@app.route('/heapsort')
def heapsort():
    return render_template('heapsort.html')

@app.route('/acercade')
def acercade():
    return render_template('masInformacion.html')

@app.route('/formularioMergesort', methods=['GET','POST'])
def formularioMergesort():
    if request.method == 'GET':
        return render_template('formularioMergesort.html')
    numero_preguntas= int(request.form.get('numero_preguntas'))
    longitud_min= int(request.form.get('longitud_min'))
    longitud_max= int(request.form.get('longitud_max'))
    preguntas=[]
    preguntas.append(bool(request.form.get('Pregunta_seleccionar')))
    preguntas.append(bool(request.form.get('Pregunta_rellenar')))
    preguntas.append(bool(request.form.get('Pregunta_comparaciones')))
    preguntas.append(bool(request.form.get('Pregunta_imagen')))

    src.main.mergesort.generar_preguntas_mergesort(numero_preguntas, longitud_min,longitud_max, preguntas)
    return redirect(url_for('datosMergesort'))

@app.route('/formularioQuicksort', methods=['GET','POST'])
def formularioQuicksort():
    if request.method == 'GET':
        return render_template('formularioQuicksort.html')
    numero_preguntas= int(request.form.get('numero_preguntas'))
    longitud_min= int(request.form.get('longitud_min'))
    longitud_max= int(request.form.get('longitud_max'))
    preguntas=[]
    preguntas.append(bool(request.form.get('Pregunta_seleccionar_unidireccional')))
    preguntas.append(bool(request.form.get('Pregunta_seleccionar_bidireccional')))
    preguntas.append(bool(request.form.get('Pregunta_rellenar')))
    preguntas.append(bool(request.form.get('Pregunta_pivote')))
    preguntas.append(bool(request.form.get('Pregunta_imagen_unidireccional')))
    preguntas.append(bool(request.form.get('Pregunta_imagen_bidireccional')))
    src.main.quicksort.generar_preguntas_quicksort(numero_preguntas, longitud_min,longitud_max,preguntas)
    return redirect(url_for('datosQuicksort'))

@app.route('/formularioHeapsort', methods=['GET','POST'])
def formularioHeapsort():
    if request.method == 'GET':
        return render_template('formularioHeapsort.html')
    numero_preguntas= int(request.form.get('numero_preguntas'))
    longitud_min= int(request.form.get('longitud_min'))
    longitud_max= int(request.form.get('longitud_max'))
    preguntas=[]
    preguntas.append(bool(request.form.get('Pregunta_seleccionar_heapify')))
    preguntas.append(bool(request.form.get('Pregunta_seleccionar_heappush')))
    preguntas.append(bool(request.form.get('Pregunta_rellenar_heapify')))
    preguntas.append(bool(request.form.get('Pregunta_rellenar_heappush')))
    preguntas.append(bool(request.form.get('Pregunta_maximos')))
    preguntas.append(bool(request.form.get('Pregunta_extraccion')))
    src.main.heapsort.generar_preguntas_heapsort(numero_preguntas, longitud_min,longitud_max, preguntas)
    return redirect(url_for('datosHeapsort'))

@app.route('/datosQuicksort')
def datosQuicksort():
    return render_template('datosQuicksort.html')

@app.route('/datosMergesort')
def datosMergesort():
    return render_template('datosMergesort.html')

@app.route('/datosHeapsort')
def datosHeapsort():
    return render_template('datosHeapsort.html')
   
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return redirect(url_for('index'))

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    file_path = ''
    if filename == 'pregunta_mergesort.xml':
        file_path = 'pregunta_mergesort.xml'
    elif filename == 'pregunta_quicksort.xml':
        file_path = 'pregunta_quicksort.xml'
    elif filename == 'pregunta_heapsort.xml':
        file_path = 'pregunta_heapsort.xml'

    return send_file(file_path, as_attachment=True)

if __name__=='__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')