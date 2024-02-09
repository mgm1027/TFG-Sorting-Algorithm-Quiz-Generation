import xml.etree.ElementTree as ET

# Método que ordena un vector por medio del algoritmo de ordenación Mergesort
# Devuelve el algoritmo ordenado además de la ultima iteración del algoritmo sin ordenar
# Autor : Mario García Martínez
def mergeSort(vector):

    # Copia del vector que se usa para ordenar y no afectar al original
    vectorResultado = list(vector)
    ultimoVector = list(vector)

    
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
def crear_pregunta_mergesort(vector):

    vectorOrdenado,vectorSolucion = mergeSort(vector)
    
    for i in vectorOrdenado:
            print(i)
    # Creamos el elemento raíz del xml
    quiz = ET.Element("quiz")

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
        ]]>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]),
               ''.join(['<td>{{1:NUMERICAL:%100%{}:0.1#}}</td>'.format(val) for val in vectorSolucion]))

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")

    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return quiz

# Vector de ejemplo
vector_ejemplo = [86, 14, 9, 10, 38, 14, 21, 17, 36, 5, 54, 37]

# Crear pregunta
pregunta_mergesort = crear_pregunta_mergesort(vector_ejemplo)

# Crear el árbol XML y escribirlo en un archivo
tree = ET.ElementTree(pregunta_mergesort)
tree.write("pregunta_mergesort.xml", encoding="utf-8", xml_declaration=True)
