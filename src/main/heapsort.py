import xml.etree.ElementTree as ET
import random
import heapq
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
import numpy as np
import string


LONGITUD_VECTOR_MIN = 5
LONGITUD_VECTOR_MAX = 10

#Creamos una clase para el arbol binario del heapsort
class ArbolNodos:
    def __init__(self, hoja):
        #Representa el valor padre
        self.hoja = hoja
        #Representa el valor hijo de la izquierda
        self.izq = None
        #Representa el valor hijo de la derecha
        self.der = None

#Método que convierte la lista correspondiente en un elemento de clase ArbolNodos
def convertir_arbol(lista):
    if not lista:
        return None
    
    #La raiz se corresponde con el elemento inicial de la lista
    raiz = ArbolNodos(lista[0])
    nodos = [raiz]
    #Representa el número de valores que se han añadido al arbol de la lista
    i = 1
    
    while i < len(lista):
        #Extraemos de la lista de nodos restantes el valor siguiente
        nodo = nodos.pop(0)
        
        if lista[i] is not None:
            #añadimos el valor siguiente del vector como hijo de la izquierda del nodo actual
            nodo.izq = ArbolNodos(lista[i])
            #añadimos el nuevo nodo a la lista de nodos pendientes por añadir al arbol
            nodos.append(nodo.izq)
        i += 1
        
        if i < len(lista) and lista[i] is not None:
            #añadimos el valor siguiente del vector como hijo de la derecha del nodo actual
            nodo.der = ArbolNodos(lista[i])
            #añadimos el nuevo nodo a la lista de nodos pendientes por añadir al arbol
            nodos.append(nodo.der)
        i += 1
        
    return raiz

#Metodo para poder visualizar completamente el arbol
def visualizar_arbol(root):
    if not root:
        return
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')
    
    depth = get_depth(root)
    max_width = 2 ** depth - 1
    posiciones = {}
    visualizar_nodo(ax, root, 0, max_width, 0, depth, posiciones)

#Método para preparar la visualizacion de un solo nodo con sus hijos
def visualizar_nodo(ax, nodo, izq, der, level, depth, posiciones):
    if not nodo:
        return
    
    x = (izq + der) / 2
    y = depth - level
    ax.text(x, y, str(nodo.hoja), ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))  # etiqueta del nodo
    posiciones[nodo] = (x, y)
    
    if nodo.izq:
        izq_hijo_izq = izq
        izq_hijo_der = x - 1
        visualizar_nodo(ax, nodo.izq, izq_hijo_izq, izq_hijo_der, level + 1, depth, posiciones)
        ax.plot([x, (izq_hijo_izq + izq_hijo_der) / 2], [y, y - 1], color='black')  # línea a hijo izquierdo
    
    if nodo.der:
        der_hijo_izq = x + 1
        der_hijo_der = der
        visualizar_nodo(ax, nodo.der, der_hijo_izq, der_hijo_der, level + 1, depth, posiciones)
        ax.plot([x, (der_hijo_izq + der_hijo_der) / 2], [y, y - 1], color='black')  # línea a hijo derecho

def get_depth(raiz):
    if not raiz:
        return 0
    return max(get_depth(raiz.izq), get_depth(raiz.der)) + 1

#método que genera una lista de letras para poder visualizar el árbol correctamente
def generar_lista_letras(n):
    
    abecedario = string.ascii_lowercase
    lista_letras = [abecedario[i % len(abecedario)] for i in range(n)]
    
    return lista_letras

# Pregunta de reconocer la posición de un valor en el árbol binario (heapsort)
# reordenando según se van añadiendo los valores (heappush)
# Autor : Mario García Martínez
def crear_pregunta_heapsort_imagen_heappush(vector, quiz):
    vectorInicial = list(vector)

    #Vamos reordenando los valores a medida que los vamos añadiendo a la lista con el método heappush
    vectorSolucionPush =[]
    for i in vectorInicial:
        heapq.heappush(vectorSolucionPush,i)

    valorSeleccionado= random.choice(vectorInicial)
    posiciónSeleccionada=vectorSolucionPush.index(valorSeleccionado)

    # Generamos las opciones
    opciones= generar_lista_letras(len(vectorInicial))
    #Generamos el arbol a partir de las opciones y codificamos las imágenes generadas a base64 para poder mostrarlas en el archivo xml sin tener que almacenarlas

    arbol= convertir_arbol(opciones)
    visualizar_arbol(arbol)
    plt.savefig(f'ImagenHeapsort{vectorInicial}.jpg')
    plt.close()

    imagen = plt.imread(f'ImagenHeapsort{vectorInicial}.jpg')
    imagenPillow = Image.fromarray(np.uint8(imagen))
    buffer = BytesIO()
    imagenPillow.save(buffer, format="JPEG")
    imagen64 = base64.b64encode(buffer.getvalue())
    #guardamos la imagen decodificada y su identificador como una tupla en la lista de opciones para poder identificar cada opción
    imagenFinal=imagen64.decode("utf-8")

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz, "question")
    question.set("type", "multichoice")  # Cambia a multichoice

    # Creamos el subelemento del vector heapsort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Heapsort " + str(vector)

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
        <p>¿ En qué posición del árbol quedaría el valor ({valorSeleccionado}) una vez ordenado con el método <em>heapsort</em> reordenando una vector a medida que se van introduciendo valores en dicho vector (<em>heappush</em>)?</p>
        <p><img src="@@PLUGINFILE@@/ImagenHeapsort{vectorInicial}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
    """

    # Agregamos opciones de respuesta
    for opcion in opciones:
        choice = ET.SubElement(question, "answer", fraction="100" if opciones.index(opcion) == posiciónSeleccionada else "0")
        text_choice = ET.SubElement(choice, "text")
        text_choice.text = f"<![CDATA[<p> </p>"
    
    #Guardamos en el archivo la imagen codificada correspondiente para que se pueda visualizar en el xml
    
    archivo=ET.SubElement(questiontext, f'file')
    archivo.set('name', f"ImagenHeapsort{vectorInicial}.jpg")
    archivo.set('path', "/")
    archivo.set('encoding', "base64")
    archivo.text = f"""{imagenFinal}"""
        

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")
    #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
    text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {opciones[posiciónSeleccionada]}</p>"


    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    #Eliminamos todas las imágenes almacenadas anteriormente
    os.remove(f'ImagenHeapsort{vectorInicial}.jpg')
    return question

# Pregunta de reconocer la posición de un valor en el árbol binario (heapsort)
# una vez la lista ya ha sido generada (heapify)
# Autor : Mario García Martínez
def crear_pregunta_heapsort_imagen_heapify(vector, quiz):
    vectorInicial = list(vector)
    vectorSolucionIfy = list(vector)

    #Reordenamos los valores de una lista desordenada con heapify
    heapq.heapify(vectorSolucionIfy)

    valorSeleccionado= random.choice(vectorInicial)
    posiciónSeleccionada=vectorSolucionIfy.index(valorSeleccionado)

    # Generamos las opciones
    opciones= generar_lista_letras(len(vectorInicial))
    #Generamos el arbol a partir de las opciones y codificamos las imágenes generadas a base64 para poder mostrarlas en el archivo xml sin tener que almacenarlas

    arbol= convertir_arbol(opciones)
    visualizar_arbol(arbol)
    plt.savefig(f'ImagenHeapsort{vectorInicial}.jpg')
    plt.close()

    imagen = plt.imread(f'ImagenHeapsort{vectorInicial}.jpg')
    imagenPillow = Image.fromarray(np.uint8(imagen))
    buffer = BytesIO()
    imagenPillow.save(buffer, format="JPEG")
    imagen64 = base64.b64encode(buffer.getvalue())
    #guardamos la imagen decodificada y su identificador como una tupla en la lista de opciones para poder identificar cada opción
    imagenFinal=imagen64.decode("utf-8")

    # Creamos el subelemento de pregunta
    question = ET.SubElement(quiz, "question")
    question.set("type", "multichoice")  # Cambia a multichoice

    # Creamos el subelemento del vector mergesort que se debe ordenar
    name = ET.SubElement(question, "name")
    text_name = ET.SubElement(name, "text")
    text_name.text = "Heapsort " + str(vector)

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
        <p>¿ En qué posición del árbol quedaría el valor ({valorSeleccionado}) una vez ordenado con el método <em>heapsort</em> reordenando una vector con sus valores ya generados (<em>heapify</em>)?</p>
        <p><img src="@@PLUGINFILE@@/ImagenHeapsort{vectorInicial}.jpg" alt="" width="580" height="415" style="vertical-align:text-bottom; margin: 0 .5em;"><br></p>
    """

    # Agregamos opciones de respuesta
    for opcion in opciones:
        choice = ET.SubElement(question, "answer", fraction="100" if opciones.index(opcion) == posiciónSeleccionada else "0")
        text_choice = ET.SubElement(choice, "text")
        text_choice.text = f"<![CDATA[<p> </p>"
    
    #Guardamos en el archivo la imagen codificada correspondiente para que se pueda visualizar en el xml
    
    archivo=ET.SubElement(questiontext, f'file')
    archivo.set('name', f"ImagenHeapsort{vectorInicial}.jpg")
    archivo.set('path', "/")
    archivo.set('encoding', "base64")
    archivo.text = f"""{imagenFinal}"""
        

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")
    #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
    text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {opciones[posiciónSeleccionada]}</p>"


    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    #Eliminamos todas las imágenes almacenadas anteriormente
    os.remove(f'ImagenHeapsort{vectorInicial}.jpg')
    return question

# # Método que ordena un montículo de el algoritmo de ordenación Heapsort
# # Autor : Mario García Martínez
# def heapify(vector, n, i):
#   mayor = i
#   izq = 2 * i + 1
#   der = 2 * i + 2

#   if izq < n and vector[i] < vector[izq]:
#       mayor = izq

#   if der < n and vector[mayor] < vector[der]:
#       mayor = der

#   if mayor != i:
#       vector[i], vector[mayor] = vector[mayor], vector[i]
#       heapify(vector, n, mayor)

# # Método que ordena una lista por medio del algoritmo de ordenación por montículos o Heapsort
# # Devuelve la ista ordenada además de la ultima iteración de la lista sin ordenar
# # Autor : Mario García Martínez
# def heapSort(vector):
#     vectorResultado = vector
#     ultimoVector = vector
#     n = len(vectorResultado)

#     for i in range(n//2, -1, -1):
#         heapify(vectorResultado, n, i)
        
#     ultimoVector= list(vectorResultado)
#     for i in range(n-1, 0, -1):
#         vectorResultado[i], vectorResultado[0] = vectorResultado[0], vectorResultado[i]

#         heapify(vector, i, 0)
    
#     return vectorResultado, ultimoVector


# # Pregunta de ejemplo sobre la primera llamada tras ejecutar heapsort(ordenación por montículos)
# # Autor : Mario García Martínez
# def crear_pregunta_heapsort(vector, quiz):
#     vectorInicial= list(vector)

#     vectorOrdenado,vectorSolucion = heapSort(vectorInicial)


#     # Creamos el subelemento de pregunta
#     question = ET.SubElement(quiz,"question")
#     question.set("type", "cloze")

#     # Creamos el subelemento del vector heapsort que se debe ordenar
#     name = ET.SubElement(question, "name")
#     text_name = ET.SubElement(name, "text")
#     text_name.text = "Heapsort " + str(vector)

#     # Creamos el subelemento de la pregunta del test para el formato html
#     questiontext = ET.SubElement(question, "questiontext", format="html")

#     # Creamos el subelemento del texto de la pregunta
#     text_question = ET.SubElement(questiontext, "text")

#     # Introducimos el enunciado de la pregunta
#     text_question.text = """
#         <![CDATA[
#         <p>Dado el siguiente vector:</p>
#         <table border="1" align="center">
#         <tbody>
#         <tr>{}</tr>
#         </tbody>
#         </table>
#         <p>Rellene los valores del vector resultante al aplicar el método <em>heapsort</em>, tras la finalización de las llamadas recursivas del primer for, antes de realizar el último proceso de mezcla:</p>
#         <table border="1" align="center">
#         <tbody>
#         <tr>{}</tr>
#         </tbody>
#         </table>
#     """.format(''.join(['<td>{}</td>'.format(val) for val in vector]),
#                ''.join(['<td>{{1:NUMERICAL:%100%{}:0.1#}}</td>'.format(val) for val in vectorSolucion]))


#     generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
#     text_generalfeedback = ET.SubElement(generalfeedback, "text")

#     penalty = ET.SubElement(question, "penalty")
#     penalty.text = "0.3333333"

#     hidden = ET.SubElement(question, "hidden")
#     hidden.text = "0"

#     idnumber = ET.SubElement(question, "idnumber")

#     return question

# Pregunta selección múltiple sobre la primera llamada de heapsort
# Autor : Mario García Martínez
# def crear_pregunta_heapsort_multiple(vector, quiz):
#     vectorInicial = list(vector)

#     vectorOrdenado, vectorSolucion = heapSort(vectorInicial)
#     # Hacer copias de los vectores para las opciones
#     vectorOpcion1 = vectorInicial.copy()
#     vectorOpcion2 = vectorInicial.copy()

#     # Cambiamos un poco el orden de las opciones incorrectas
#     random.shuffle(vectorOpcion1)
#     random.shuffle(vectorOpcion2)

#     # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
#     opciones = [vectorOpcion1, vectorOpcion2, vectorSolucion]
#     random.shuffle(opciones)

#     # Creamos el subelemento de pregunta
#     question = ET.SubElement(quiz, "question")
#     question.set("type", "multichoice")  # Cambia a multichoice

#     # Creamos el subelemento del vector heapsort que se debe ordenar
#     name = ET.SubElement(question, "name")
#     text_name = ET.SubElement(name, "text")
#     text_name.text = "heapsort " + str(vector)

#     # Creamos el subelemento de la pregunta del test para el formato html
#     questiontext = ET.SubElement(question, "questiontext", format="html")

#     # Creamos el subelemento del texto de la pregunta
#     text_question = ET.SubElement(questiontext, "text")

#     # Introducimos el enunciado de la pregunta
#     text_question.text = """
#         <![CDATA[
#         <p>Dado el siguiente vector:</p>
#         <table border="1" align="center">
#         <tbody>
#         <tr>{}</tr>
#         </tbody>
#         </table>
#         <p>¿Qué nuevo vector resultaría al aplicar el método <em>heapsort</em>, en la primera llamada, tras la finalización de las llamadas recursivas del primer for, antes de realizar el último proceso de mezcla? </p>
#     """.format(''.join(['<td>{}</td>'.format(val) for val in vector]))

#     # Agregamos opciones de respuesta
#     for opcion in opciones:
#         choice = ET.SubElement(question, "answer", fraction="100" if opcion == vectorSolucion else "0")
#         text_choice = ET.SubElement(choice, "text")
#         text_choice.text = f"<![CDATA[<p>{' '.join(map(str, opcion))}</p>"

#     generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
#     text_generalfeedback = ET.SubElement(generalfeedback, "text")
#     #Cambiamos el texto que se muestra al corregir la pregunta para que muestre la respuesta correcta:
#     text_generalfeedback.text = f"<![CDATA[<p>La respuesta correcta es: {', '.join(map(str, vectorSolucion))}</p>"


#     penalty = ET.SubElement(question, "penalty")
#     penalty.text = "0.3333333"

#     hidden = ET.SubElement(question, "hidden")
#     hidden.text = "0"

#     idnumber = ET.SubElement(question, "idnumber")

#     return question

# Generador de cuestionarios de preguntas aleatorias sobre Heapsort
# Autor : Mario García Martínez
def generar_preguntas_heapsort (numero_preguntas):

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
        pregunta_aleatoria = random.choice([crear_pregunta_heapsort_imagen_heapify,crear_pregunta_heapsort_imagen_heappush])   
        pregunta_aleatoria(vector_aleatorio, quiz)

    # Creamos el árbol XML y lo escribimos en un archivo
    tree = ET.ElementTree(quiz)
    tree.write("pregunta_heapsort.xml", encoding="utf-8", xml_declaration=True)

generar_preguntas_heapsort(10)
    
    

