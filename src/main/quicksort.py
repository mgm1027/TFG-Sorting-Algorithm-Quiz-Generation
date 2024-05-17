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

longitud_vector_min = 5
longitud_vector_max = 10

# Método que calcula la primera partición obtenida tras pivotar
# unidireccionalmente con el primer elemento como pivote del algoritmo
# de ordenación Quicksort
# Autor: Mario García Martínez
def quickSort_unidireccional(vector, inicio, fin):

    # Copia del vector para no modificar el original
    vectorResultado = vector
    pivote = vectorResultado[inicio]
    # Primer y segundo puntero señalan a la posición posterior al pivote al comenzar
    izq = inicio + 1
    der = inicio + 1

    # Siempre que el segundo puntero no haya avanzado hasta el final
    while der <= fin:
        # Si el valor al que señala el segundo puntero es menor o igual que el pivote
        if vectorResultado[der] <= pivote:
            # Se intercambian los valores a los que señalan el primer y segundo puntero
            vectorResultado[izq], vectorResultado[der] = vectorResultado[der], vectorResultado[izq]
            # Se desplaza la posición del primer puntero solo cuando se ha producido un intercambio
            izq += 1
        # Se desplaza la posición del segundo puntero siempre hasta finalizar
        der += 1

    #Tras finalizar se intercambia el pivote por el valor al que apunta el primer puntero (posición intermedia)
    vectorResultado[inicio], vectorResultado[izq - 1] = vectorResultado[izq - 1], vectorResultado[inicio]

    return vectorResultado, (izq - 1)

def crear_pregunta_quicksort_indice(vector,quiz):
    vectorInicial = list(vector)
    vectorSolucion, finbidireccional = quickSort_bidireccional(list(vector), 0, (len(vector)-1) )
    # Hacer copias de los vectores para las opciones
    finb1 = finbidireccional + random.randint(-3,3)
    finb2 = finbidireccional + random.randint(-3,3)

    while finb1==finb2 or finb1== finbidireccional or finb2 == finbidireccional or finb1 <=0 or finb2 <=0:
        finb1= finbidireccional + random.randint(-3,3)
        finb2 = finbidireccional + random.randint(-3,3)
    
    # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
    opciones = [finb1, finb2, finbidireccional]
    random.shuffle(opciones)

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz, "question")
    question.set("type", "multichoice")  # Cambia a multichoice

    # Creamos el subelemento del vector quicksort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Quicksort " + str(vector)

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
        <p>¿En que posición quedaría el pivote({}) tras realizar el proceso de partición del <em>quicksort</em></p>
        <p>teniendo en cuenta que la primera posición corresponde a la posición 0? </p>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]),vector[0])

    # Agregamos opciones de respuesta
    for opcion in opciones:
        choice = ET.SubElement(question, "answer", fraction="100" if opcion == finbidireccional else "0")
        text_choice = ET.SubElement(choice, "text")
        text_choice.text = f"<![CDATA[<p>{opcion}</p>"

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")
    #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
    text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {finbidireccional}</p>"


    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return question

# Método que calcula la primera partición obtenida tras pivotar
# bidireccionalmente con el primer elemento como pivote del algoritmo
# de ordenación Quicksort
# Autor: Mario García Martínez
def quickSort_bidireccional(vector, inicio, fin):

    # Copia del vector para no modificar el original
    vectorResultado = vector
    pivote = vectorResultado[inicio]
    # Primer puntero señala al primer elemento posterior al pivote
    izq = inicio + 1
    # Segundo elemento señala al último elemento del vector
    der = fin
    

    while True:
        # Siempre que el puntero izquierdo este señalando una posición menor o igual a la del segundo
        
        # Si el valor que señala el puntero de la derecha es mayor que el pivote se pasa al siguiente valor
        while izq <= der and vectorResultado[der] >= pivote:
            der = der - 1

        # Si el valor que señala el puntero de la izquierda es menor que el pivote se pasa al siguiente valor
        while izq <= der and vectorResultado[izq] <= pivote:
            izq = izq + 1

        # (No salen del bucle hasta encontrar dos casos que no cumplan por lo cual son adecuados para ser intercambiados)

        # Si el puntero izquierdo está señalando una posición menor o igual a la del segundo 
        if izq <= der:
            # Se intercambian los valores a los que señalan los punteros
            vectorResultado[izq], vectorResultado[der] = vectorResultado[der], vectorResultado[izq]
        else:
            # Si los punteros ya han finalizado
            break

    # Se coloca al pivote en la posición donde el puntero derecho ha finalizado (posición intermedia)
    vectorResultado[inicio], vectorResultado[der] = vectorResultado[der], vectorResultado[inicio]

    return vectorResultado, der

# Pregunta de ejemplo sobre la primera llamada tras ejecutar quicksort (rellenar)
# Autor : Mario García Martínez
def crear_pregunta_quicksort(vector, quiz):

    # Obtenemos las soluciones de los 2 métodos para calcular la primera partición de Quicksort
    solucionBidireccional, finBidireccional = quickSort_bidireccional(list(vector), 0, (len(vector)-1) )
    solucionUnidireccional , finUnidireccional = quickSort_unidireccional(list(vector), 0, (len(vector)-1) )

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz,"question")
    question.set("type", "cloze")

    # Creamos el subelemento del vector quicksort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Quicksort " + str(vector)

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
        <p>Rellene los valores de los vectores resultantes al aplicar el proceso de partición del <em>quicksort</em>, utilizando el primer elemento como pivote.</p>
        <p>Para el primer método de partición, bidireccional, en el que dos índices empiezan en los dos extremos y avanzan en sentidos opuestos:</p>
        <table border="1" align="center">
        <tbody>
        <tr>{}</tr>
        </tbody>
        </table>
        </table>
        <p>Para el segundo método de partición, unirrecional, en el que dos índices empiezan en el extremo izquierdo y avanzan hacia la derecha:</p>
        <table border="1" align="center">
        <tbody>
        <tr>{}</tr>
        </tbody>
        </table>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]), # Visualización de vector en el enunciado
               ''.join(['<td>{{1:NUMERICAL:%100%{}:0.1#}}</td>'.format(val) for val in solucionBidireccional ]), # Solución 1 (Bidireccional)
               ''.join(['<td>{{1:NUMERICAL:%100%{}:0.1#}}</td>'.format(val) for val in solucionUnidireccional ])) # Solución 2 (Unirrecional)

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")

    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return question

# Pregunta selección múltiple sobre la partición de quicksort unidireccional
# Autor : Mario García Martínez
def crear_pregunta_quicksort_unidireccional_multiple(vector, quiz):

    solucionUnidireccional , finUnidireccional = quickSort_unidireccional(list(vector), 0, (len(vector)-1) )

    # Hacer copias de los vectores para las opciones
    vectorOpcion1 = vector.copy()
    vectorOpcion2 = vector.copy()

    # Cambiamos un poco el orden de las opciones incorrectas
    random.shuffle(vectorOpcion1)
    
    while(vectorOpcion1 == solucionUnidireccional):
        random.shuffle(vectorOpcion1)

    random.shuffle(vectorOpcion2)

    while(vectorOpcion2 == solucionUnidireccional):
        random.shuffle(vectorOpcion2)

    # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
    opciones = [vectorOpcion1, vectorOpcion2, solucionUnidireccional]
    random.shuffle(opciones)

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz, "question")
    question.set("type", "multichoice")  # Cambia a multichoice

    # Creamos el subelemento del vector quicksort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Quicksort " + str(vector)

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
        <p>Al aplicar el proceso de partición del <em>quicksort</em> utilizando el primer elemento como pivote, ¿Cuál sería el vector resultante aplicando el método unirrecional, en el que dos índices empiezan en el extremo izquierdo y avanzan hacia la derecha?</p>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]))

    # Agregamos opciones de respuesta
    for opcion in opciones:
        choice = ET.SubElement(question, "answer", fraction="100" if opcion == solucionUnidireccional else "0")
        text_choice = ET.SubElement(choice, "text")
        text_choice.text = f"<![CDATA[<p>{' '.join(map(str, opcion))}</p>"

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")
    #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
    text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {', '.join(map(str, solucionUnidireccional))}</p>"


    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return question


# Pregunta selección múltiple sobre la partición de quicksort bidireccional
# Autor : Mario García Martínez
def crear_pregunta_quicksort_bidireccional_multiple(vector, quiz):

    solucionbidireccional , finUnidireccional = quickSort_bidireccional(list(vector), 0, (len(vector)-1) )

    # Hacer copias de los vectores para las opciones
    vectorOpcion1 = vector.copy()
    vectorOpcion2 = vector.copy()

    # Cambiamos un poco el orden de las opciones incorrectas
    random.shuffle(vectorOpcion1)
    
    while(vectorOpcion1 == solucionbidireccional):
        random.shuffle(vectorOpcion1)

    random.shuffle(vectorOpcion2)

    while(vectorOpcion2 == solucionbidireccional):
        random.shuffle(vectorOpcion2)

    # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
    opciones = [vectorOpcion1, vectorOpcion2, solucionbidireccional]
    random.shuffle(opciones)

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz, "question")
    question.set("type", "multichoice")  # Cambia a multichoice

    # Creamos el subelemento del vector quicksort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Quicksort " + str(vector)

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
        <p>Al aplicar el proceso de partición del <em>quicksort</em> utilizando el primer elemento como pivote, ¿Cuál sería el vector resultante aplicando el método bidirecional, en el que un índice comienza por el extremo izquierdo y el otro índice por el extremo derecho?</p>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]))

    # Agregamos opciones de respuesta
    for opcion in opciones:
        choice = ET.SubElement(question, "answer", fraction="100" if opcion == solucionbidireccional else "0")
        text_choice = ET.SubElement(choice, "text")
        text_choice.text = f"<![CDATA[<p>{' '.join(map(str, opcion))}</p>"

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")
    #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
    text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {', '.join(map(str, solucionbidireccional))}</p>"


    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return question

def crear_pregunta_quicksort_unidireccional_multiple_imagen(vector, quiz):
    vectorInicial = list(vector)
    global contador
    contador = 0
    vectorSolucion , finUnidireccional = quickSort_unidireccional(list(vector), 0, (len(vector)-1) )
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

    plt.bar(vSolucionstring,vectorSolucion,)
    plt.savefig(f'ImagenQuicksort{vectorInicial}-{numeroOpcion[0]}.jpg')
    plt.close()

    vOpcion1string=list()

    for i in vectorOpcion1:
        vOpcion1string.append(str(i))

    plt.bar(vOpcion1string,vectorOpcion1)
    plt.savefig(f'ImagenQuicksort{vectorInicial}-{numeroOpcion[1]}.jpg')
    plt.close()

    vOpcion2string=list()

    for i in vectorOpcion2:
        vOpcion2string.append(str(i))

    plt.bar(vOpcion2string,vectorOpcion2)
    plt.savefig(f'ImagenQuicksort{vectorInicial}-{numeroOpcion[2]}.jpg')
    plt.close()

    opciones =list()
    #Codificamos las imágenes generadas a base64 para poder mostrarlas en el archivo xml sin tener que almacenarlas
    for i in numeroOpcion:
        imagen = plt.imread(f'ImagenQuicksort{vectorInicial}-{i}.jpg')
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

    # Creamos el subelemento del vector Quicksort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Quicksort " + str(vector)

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
        <p>¿Cuál de estas imágenes corresponde al método <em>quicksort</em>, tras el primer método de partición de forma unidireccional (en el que dos índices empiezan en el extremo izquierdo y avanzan hacia la derecha) y teniendo el primer valor del vector como pivote?</p>
        <p>a.<img src="@@PLUGINFILE@@/ImagenQuicksort{vectorInicial}-{opciones[0][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
        <p>b.<img src="@@PLUGINFILE@@/ImagenQuicksort{vectorInicial}-{opciones[1][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
        <p>c.<img src="@@PLUGINFILE@@/ImagenQuicksort{vectorInicial}-{opciones[2][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
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
        archivo[contadorArchivo].set('name', f"ImagenQuicksort{vectorInicial}-{opcion[1]}.jpg")
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
        os.remove(f'ImagenQuicksort{vectorInicial}-{opcion[1]}.jpg')

    return question

def crear_pregunta_quicksort_bidireccional_multiple_imagen(vector, quiz):
    vectorInicial = list(vector)
    global contador
    contador = 0
    vectorSolucion , finUnidireccional = quickSort_bidireccional(list(vector), 0, (len(vector)-1) )
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
    plt.savefig(f'ImagenQuicksort{vectorInicial}-{numeroOpcion[0]}.jpg')
    plt.close()

    vOpcion1string=list()

    for i in vectorOpcion1:
        vOpcion1string.append(str(i))

    plt.bar(vOpcion1string,vectorOpcion1)
    plt.savefig(f'ImagenQuicksort{vectorInicial}-{numeroOpcion[1]}.jpg')
    plt.close()

    vOpcion2string=list()

    for i in vectorOpcion2:
        vOpcion2string.append(str(i))

    plt.bar(vOpcion2string,vectorOpcion2)
    plt.savefig(f'ImagenQuicksort{vectorInicial}-{numeroOpcion[2]}.jpg')
    plt.close()

    opciones =list()
    #Codificamos las imágenes generadas a base64 para poder mostrarlas en el archivo xml sin tener que almacenarlas
    for i in numeroOpcion:
        imagen = plt.imread(f'ImagenQuicksort{vectorInicial}-{i}.jpg')
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

    # Creamos el subelemento del vector Quicksort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Quicksort " + str(vector)

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
        <p>¿Cuál de estas imágenes corresponde al método <em>quicksort</em>, tras el primer método de partición de forma bidireccional (en el que un índice comienza por el extremo izquierdo y el otro índice por el extremo derecho) y teniendo el primer valor del vector como pivote?</p>
        <p>a.<img src="@@PLUGINFILE@@/ImagenQuicksort{vectorInicial}-{opciones[0][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
        <p>b.<img src="@@PLUGINFILE@@/ImagenQuicksort{vectorInicial}-{opciones[1][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
        <p>c.<img src="@@PLUGINFILE@@/ImagenQuicksort{vectorInicial}-{opciones[2][1]}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
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
        archivo[contadorArchivo].set('name', f"ImagenQuicksort{vectorInicial}-{opcion[1]}.jpg")
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
        os.remove(f'ImagenQuicksort{vectorInicial}-{opcion[1]}.jpg')

    return question

# Vector de ejemplo
#vector_ejemplo = [37, 14, 9, 10, 38, 14, 21, 17, 36, 5, 54, 86]

# Crear pregunta
#pregunta_quicksort = crear_pregunta_quicksort(vector_ejemplo)

# Crear el árbol XML y escribirlo en un archivo
#tree = ET.ElementTree(pregunta_quicksort)
#tree.write("pregunta_quicksort.xml", encoding="utf-8", xml_declaration=True)

# Generador de cuestionarios de preguntas aleatorias sobre Quicksort
# Autor : Mario García Martínez
def generar_preguntas_quicksort (numero_preguntas, longitud_min, longitud_max):
    global longitud_vector_min
    global longitud_vector_max
    longitud_vector_min= longitud_min
    longitud_vector_max= longitud_max
    # Creamos el elemento raíz del xml
    quiz = ET.Element("quiz")

    #Generamos un numero de preguntas a partir de la variable pasada por parámetro
    for i in range(numero_preguntas):
        #Inicializamos el vector que vamos a usar como pregunta
        vector_aleatorio = []
        #Generamos aleatoriamente la longitud de la pregunta
        longitud = random.randint( longitud_vector_min , longitud_vector_max )
        #Rellenamos los valores del vector con valores aleatorios
        for i in range(longitud):
            vector_aleatorio.append(random.randint(0,100))
        
        #Creamos la pregunta una vez tenemos el vector aleatoriamente entre las distintas preguntas de las que disponemos
        pregunta_aleatoria = random.choice([crear_pregunta_quicksort, crear_pregunta_quicksort_unidireccional_multiple, crear_pregunta_quicksort_bidireccional_multiple, crear_pregunta_quicksort_indice
                                            ,crear_pregunta_quicksort_unidireccional_multiple_imagen,crear_pregunta_quicksort_bidireccional_multiple_imagen])   
        pregunta_aleatoria(vector_aleatorio, quiz)

    # Creamos el árbol XML y lo escribimos en un archivo
    tree = ET.ElementTree(quiz)
    tree.write("pregunta_quicksort.xml", encoding="utf-8", xml_declaration=True)


#generar_preguntas_quicksort(10)


