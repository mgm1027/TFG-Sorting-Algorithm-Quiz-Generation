import xml.etree.ElementTree as ET
import random

LONGITUD_VECTOR_MIN = 5
LONGITUD_VECTOR_MAX = 10

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
    random.shuffle(vectorOpcion2)

    # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
    opciones = [vectorOpcion1, vectorOpcion2, solucionUnidireccional]
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
    random.shuffle(vectorOpcion2)

    # Cambiamos el orden de las preguntas para que la respuesta correcta no sea siempre la misma opción
    opciones = [vectorOpcion1, vectorOpcion2, solucionbidireccional]
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

# Vector de ejemplo
#vector_ejemplo = [37, 14, 9, 10, 38, 14, 21, 17, 36, 5, 54, 86]

# Crear pregunta
#pregunta_quicksort = crear_pregunta_quicksort(vector_ejemplo)

# Crear el árbol XML y escribirlo en un archivo
#tree = ET.ElementTree(pregunta_quicksort)
#tree.write("pregunta_quicksort.xml", encoding="utf-8", xml_declaration=True)

# Generador de cuestionarios de preguntas aleatorias sobre Mergesort
# Autor : Mario García Martínez
def generar_preguntas_quicksort (numero_preguntas):

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
        pregunta_aleatoria = random.choice([crear_pregunta_quicksort, crear_pregunta_quicksort_unidireccional_multiple, crear_pregunta_quicksort_bidireccional_multiple])   
        pregunta_aleatoria(vector_aleatorio, quiz)

    # Creamos el árbol XML y lo escribimos en un archivo
    tree = ET.ElementTree(quiz)
    tree.write("pregunta_quicksort.xml", encoding="utf-8", xml_declaration=True)

generar_preguntas_quicksort(10)