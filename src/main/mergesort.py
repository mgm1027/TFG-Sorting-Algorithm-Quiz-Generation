import xml.etree.ElementTree as ET
import random

LONGITUD_VECTOR_MIN = 5
LONGITUD_VECTOR_MAX = 10

# Método que ordena un vector por medio del algoritmo de ordenación Mergesort
# Devuelve el algoritmo ordenado además de la ultima iteración del algoritmo sin ordenar
# Autor : Mario García Martínez
def mergeSort(vector):

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


# Pregunta de ejemplo sobre la primera llamada tras ejecutar mergesort (rellenar)
# Autor : Mario García Martínez
def crear_pregunta_mergesort(vector, quiz):
    vectorInicial= list(vector)

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

# Pregunta selección múltiple sobre la primera llamada de mergesort
# Autor : Mario García Martínez
def crear_pregunta_mergesort_multiple(vector, quiz):
    vectorInicial = list(vector)

    vectorOrdenado, vectorSolucion = mergeSort(vectorInicial)
    # Hacer copias de los vectores para las opciones
    vectorOpcion1 = vectorInicial.copy()
    vectorOpcion2 = vectorInicial.copy()

    # Cambiamos un poco el orden de las opciones incorrectas
    random.shuffle(vectorOpcion1)
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
# vector_ejemplo = [86, 14, 9, 10, 38, 14, 21, 17, 36, 5, 54, 37]

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
        pregunta_aleatoria = random.choice([crear_pregunta_mergesort, crear_pregunta_mergesort_multiple])   
        pregunta_aleatoria(vector_aleatorio, quiz)

    # Creamos el árbol XML y lo escribimos en un archivo
    tree = ET.ElementTree(quiz)
    tree.write("pregunta_mergesort.xml", encoding="utf-8", xml_declaration=True)
    

generar_preguntas_mergesort(10)
    
    

