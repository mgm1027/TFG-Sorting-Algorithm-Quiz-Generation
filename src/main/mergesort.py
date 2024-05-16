import xml.etree.ElementTree as ET
import random
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

LONGITUD_VECTOR_MIN = 5
LONGITUD_VECTOR_MAX = 10

contador = 0

# Método que ordena un vector por medio del algoritmo de ordenación Mergesort
# Devuelve el algoritmo ordenado además de la ultima iteración del algoritmo sin ordenar
# Autor : Mario García Martínez
def mergeSort(vector):
    global contador
    # Copia del vector que se usa para ordenar y no afectar al original
    vectorResultado = vector
    ultimoVector = vector

    
    if len(vectorResultado) > 1:
        mid = len(vectorResultado)//2
        L = vectorResultado[:mid]
        R = vectorResultado[mid:]
        mergeSort(L)
        mergeSort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):

            contador += 1
            if L[i] < R[j]:
                vectorResultado[k] = L[i]
                i += 1
                
            else:
                vectorResultado[k] = R[j]
                j += 1
                
            k += 1

        while i < len(L):
            vectorResultado[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            vectorResultado[k] = R[j]
            j += 1
            k += 1

        ultimoVector = L + R
    
    
    return vectorResultado, ultimoVector


def crear_pregunta_mergesort_multiple_imagen(vector, quiz):
    vectorInicial = list(vector)
    global contador
    contador = 0
    vectorOrdenado, vectorSolucion = mergeSort(vectorInicial)
    # Hacer copias de los vectores para las opciones
    vectorOpcion1 = vectorInicial.copy()
    vectorOpcion2 = vectorInicial.copy()

    # Cambiamos un poco el orden de las opciones incorrectas
    random.shuffle(vectorOpcion1)
    
    while(vectorOpcion1 == vectorSolucion):
        random.shuffle(vectorOpcion1)

    random.shuffle(vectorOpcion2)

    while(vectorOpcion2 == vectorSolucion):
        random.shuffle(vectorOpcion2)
    
    #Le asignamos un número identificador a cada opción aleatoriamente para diferenciar las imágenes
    numeroOpcion= [0,1,2]
    random.shuffle(numeroOpcion)

    #Generamos las imágenes correspondientes a los vectores

    vSolucionstring=list()

    for i in vectorSolucion:
        vSolucionstring.append(str(i))
    plt.bar(vSolucionstring,vectorSolucion)
    plt.savefig(f'ImagenMergesort{vectorInicial}-{numeroOpcion[0]}.jpg')
    plt.close()

    vOpcion1string=list()

    for i in vectorOpcion1:
        vOpcion1string.append(str(i))
    plt.bar(vOpcion1string,vectorOpcion1)
    plt.savefig(f'ImagenMergesort{vectorInicial}-{numeroOpcion[1]}.jpg')
    plt.close()

    vOpcion2string=list()

    for i in vectorOpcion2:
        vOpcion2string.append(str(i))
    plt.bar(vOpcion2string,vectorOpcion2)
    plt.savefig(f'ImagenMergesort{vectorInicial}-{numeroOpcion[2]}.jpg')
    plt.close()

    opciones =list()
    #Codificamos las imágenes generadas a base64 para poder mostrarlas en el archivo xml sin tener que almacenarlas
    for i in numeroOpcion:
        imagen = plt.imread(f'ImagenMergesort{vectorInicial}-{i}.jpg')
        imagenPillow = Image.fromarray(np.uint8(imagen))
        buffer = BytesIO()
        imagenPillow.save(buffer, format="JPEG")
        imagen64 = base64.b64encode(buffer.getvalue())
        #guardamos la imagen decodificada y su identificador como una tupla en la lista de opciones para poder identificar cada opción
        opciones.append((imagen64.decode("utf-8"),i))


    # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
    random.shuffle(opciones)

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz, "question")
    question.set("type", "multichoice")  # Cambia a multichoice

    # Creamos el subelemento del vector mergesort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Mergesort " + str(vector)

    # Creamos el subelemento de la pregunta del test para el formato html
    questiontext = ET.SubElement(question, "questiontext", format="html")

    # Creamos el subelemento del texto de la pregunta
    text_question = ET.SubElement(questiontext, "text")

    # Introducimos el enunciado de la pregunta
    text_question.text = f"""
    <![CDATA[
        <p>Dado el siguiente vector:</p>
        <table border="1" align="center">
        <tbody>
        <tr>{''.join(['<td>{}</td>'.format(val) for val in vector])}</tr>
        </tbody>
        </table>
        <p>¿Cuál de estas imágenes corresponde al método <em>mergesort</em>, en la primera llamada, una vez resueltas las llamadas recursivas, antes de realizar el último proceso de mezcla? </p>
        <p>a.<img src="@@PLUGINFILE@@/ImagenMergesort{vectorInicial}-{opciones[0][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
        <p>b.<img src="@@PLUGINFILE@@/ImagenMergesort{vectorInicial}-{opciones[1][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
        <p>c.<img src="@@PLUGINFILE@@/ImagenMergesort{vectorInicial}-{opciones[2][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
    """

    # Agregamos opciones de respuesta

    for opcion in opciones:
        choice = ET.SubElement(question, "answer", fraction="100" if opcion[1] == numeroOpcion[0] else "0")
        text_choice = ET.SubElement(choice, "text")
        text_choice.text = f"<![CDATA[<p>{' '}</p>"
    archivo=list()
    contadorArchivo=0
    #Guardamos en el archivo la imagen codificada correspondiente para que se pueda visualizar en el xml
    for opcion in opciones:
        archivo.append(ET.SubElement(questiontext, f'file'))
        archivo[contadorArchivo].set('name', f"ImagenMergesort{vectorInicial}-{opcion[1]}.jpg")
        archivo[contadorArchivo].set('path', "/")
        archivo[contadorArchivo].set('encoding', "base64")
        archivo[contadorArchivo].text = f"""{opcion[0]}"""
        contadorArchivo+=1

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")
    #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
    text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {', '.join(map(str, vectorSolucion))}</p>"


    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")
    
    #Eliminamos todas las imágenes almacenadas anteriormente
    for opcion in opciones:
        os.remove(f'ImagenMergesort{vectorInicial}-{opcion[1]}.jpg')

    return question


# Pregunta de ejemplo sobre la primera llamada tras ejecutar mergesort (rellenar)
# Autor : Mario García Martínez
def crear_pregunta_mergesort(vector, quiz):
    vectorInicial= list(vector)
    global contador
    contador = 0
    vectorOrdenado,vectorSolucion = mergeSort(vectorInicial)

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz,"question")
    question.set("type", "cloze")

    # Creamos el subelemento del vector mergesort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Mergesort " + str(vector)

    # Creamos el subelemento de la pregunta del test para el formato html
    questiontext = ET.SubElement(question, "questiontext", format="html")

    # Creamos el subelemento del texto de la pregunta
    text_question = ET.SubElement(questiontext, "text")

    # Introducimos el enunciado de la pregunta
    text_question.text = """
        <![CDATA[
        <p>Dado el siguiente vector:</p>
        <table border="1" align="center">
        <tbody>
        <tr>{}</tr>
        </tbody>
        </table>
        <p>Rellene los valores del vector resultante al aplicar el método <em>mergesort</em>, en la primera llamada, una vez resueltas las llamadas recursivas, antes de realizar el último proceso de mezcla:</p>
        <table border="1" align="center">
        <tbody>
        <tr>{}</tr>
        </tbody>
        </table>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]),
               ''.join(['<td>{{1:NUMERICAL:%100%{}:0.1#}}</td>'.format(val) for val in vectorSolucion]))

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")

    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return question

def crear_pregunta_mergesort_contador(vector,quiz):
    vectorInicial = list(vector)
    global contador
    contador = 0
    vectorOrdenado, vectorSolucion = mergeSort(vectorInicial)
    # Hacer copias de los vectores para las opciones
    contadoropcion1 = contador + random.randint(-3,3)
    contadoropcion2 = contador + random.randint(-3,3)

    while contadoropcion1==contadoropcion2 or contadoropcion1== contador or contadoropcion2 == contador or contadoropcion1 <=0 or contadoropcion2 <=0:
        contadoropcion1= contador + random.randint(-3,3)
        contadoropcion2 = contador + random.randint(-3,3)
    

    # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
    opciones = [contadoropcion1, contadoropcion2, contador]
    random.shuffle(opciones)

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz, "question")
    question.set("type", "multichoice")  # Cambia a multichoice

    # Creamos el subelemento del vector mergesort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Mergesort " + str(vector)

    # Creamos el subelemento de la pregunta del test para el formato html
    questiontext = ET.SubElement(question, "questiontext", format="html")

    # Creamos el subelemento del texto de la pregunta
    text_question = ET.SubElement(questiontext, "text")

    # Introducimos el enunciado de la pregunta
    text_question.text = """
        <![CDATA[
        <p>Dado el siguiente vector:</p>
        <table border="1" align="center">
        <tbody>
        <tr>{}</tr>
        </tbody>
        </table>
        <p>¿Cuántas comparaciones se producirán usando el algoritmo <em>mergesort</em>, una vez la lista esté ordenada? </p>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]))

    # Agregamos opciones de respuesta
    for opcion in opciones:
        choice = ET.SubElement(question, "answer", fraction="100" if opcion == contador else "0")
        text_choice = ET.SubElement(choice, "text")
        text_choice.text = f"<![CDATA[<p>{opcion}</p>"

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")
    #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
    text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {contador}</p>"


    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return question

# Pregunta selección múltiple sobre la primera llamada de mergesort
# Autor : Mario García Martínez
def crear_pregunta_mergesort_multiple(vector, quiz):
    vectorInicial = list(vector)
    global contador
    contador = 0
    vectorOrdenado, vectorSolucion = mergeSort(vectorInicial)
    # Hacer copias de los vectores para las opciones
    vectorOpcion1 = vectorInicial.copy()
    vectorOpcion2 = vectorInicial.copy()

    # Cambiamos un poco el orden de las opciones incorrectas
    random.shuffle(vectorOpcion1)
    
    while(vectorOpcion1 == vectorSolucion):
        random.shuffle(vectorOpcion1)

    random.shuffle(vectorOpcion2)

    while(vectorOpcion2 == vectorSolucion):
        random.shuffle(vectorOpcion2)

    # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
    opciones = [vectorOpcion1, vectorOpcion2, vectorSolucion]
    random.shuffle(opciones)

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz, "question")
    question.set("type", "multichoice")  # Cambia a multichoice

    # Creamos el subelemento del vector mergesort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Mergesort " + str(vector)

    # Creamos el subelemento de la pregunta del test para el formato html
    questiontext = ET.SubElement(question, "questiontext", format="html")

    # Creamos el subelemento del texto de la pregunta
    text_question = ET.SubElement(questiontext, "text")

    # Introducimos el enunciado de la pregunta
    text_question.text = """
        <![CDATA[
        <p>Dado el siguiente vector:</p>
        <table border="1" align="center">
        <tbody>
        <tr>{}</tr>
        </tbody>
        </table>
        <p>¿Qué nuevo vector resultaría al aplicar el método <em>mergesort</em>, en la primera llamada, una vez resueltas las llamadas recursivas, antes de realizar el último proceso de mezcla? </p>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]))

    # Agregamos opciones de respuesta
    for opcion in opciones:
        choice = ET.SubElement(question, "answer", fraction="100" if opcion == vectorSolucion else "0")
        text_choice = ET.SubElement(choice, "text")
        text_choice.text = f"<![CDATA[<p>{' '.join(map(str, opcion))}</p>"

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")
    #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
    text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {', '.join(map(str, vectorSolucion))}</p>"


    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return question

# Vector de ejemplo
#vector_ejemplo = [86, 14, 9, 10, 38, 14, 21, 17, 36, 5, 54, 37]

# Crear pregunta
#pregunta_mergesort = crear_pregunta_mergesort(vector_ejemplo)

# Crear el árbol XML y escribirlo en un archivo
#tree = ET.ElementTree(pregunta_mergesort)
#tree.write("pregunta_mergesort.xml", encoding="utf-8", xml_declaration=True)


# Generador de cuestionarios de preguntas aleatorias sobre Mergesort
# Autor : Mario García Martínez
def generar_preguntas_mergesort (numero_preguntas):

    # Creamos el elemento raíz del xml
    quiz = ET.Element("quiz")

    #Generamos un numero de preguntas a partir de la variable pasada por parámetro
    for i in range(numero_preguntas):
        #Inicializamos el vector que vamos a usar como pregunta
        vector_aleatorio = []
        #Generamos aleatoriamente la longitud de la pregunta
        longitud = random.randint( LONGITUD_VECTOR_MIN , LONGITUD_VECTOR_MAX )
        #Rellenamos los valores del vector con valores aleatorios
        for i in range(longitud):
            vector_aleatorio.append(random.randint(0,100))
        
        #Creamos la pregunta una vez tenemos el vector aleatoriamente entre las distintas preguntas de las que disponemos
        pregunta_aleatoria = random.choice([crear_pregunta_mergesort, crear_pregunta_mergesort_multiple,crear_pregunta_mergesort_multiple_imagen, crear_pregunta_mergesort_contador])   
        pregunta_aleatoria(vector_aleatorio, quiz)

    # Creamos el árbol XML y lo escribimos en un archivo
    tree = ET.ElementTree(quiz)
    tree.write("pregunta_mergesort.xml", encoding="utf-8", xml_declaration=True)


#generar_preguntas_mergesort(10)

    
    

