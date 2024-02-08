import xml.etree.ElementTree as ET

# Pregunta de ejemplo sobre la primera llamada tras ejecutar quicksort (rellenar)
# Autor : Mario García Martínez
def crear_pregunta_quicksort(vector):

    # Creamos el elemento raíz del xml
    quiz = ET.Element("quiz")

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
        ]]>
    """.format(''.join(['<td>{}</td>'.format(val) for val in vector]), # Visualización de vector en el enunciado
               ''.join(['<td>{{1:NUMERICAL:%100%{}:0.1#}}</td>'.format(val) for val in sorted(vector) ]), # Solución 1 (Bidireccional)
               ''.join(['<td>{{1:NUMERICAL:%100%{}:0.1#}}</td>'.format(val) for val in sorted(vector) ])) # Solución 2 (Unirrecional)

    generalfeedback = ET.SubElement(question, "generalfeedback", format="html")
    text_generalfeedback = ET.SubElement(generalfeedback, "text")

    penalty = ET.SubElement(question, "penalty")
    penalty.text = "0.3333333"

    hidden = ET.SubElement(question, "hidden")
    hidden.text = "0"

    idnumber = ET.SubElement(question, "idnumber")

    return quiz

# Vector de ejemplo
vector_ejemplo = [37, 14, 9, 10, 38, 14, 21, 17, 36, 5, 54, 86]

# Crear pregunta
pregunta_quicksort = crear_pregunta_quicksort(vector_ejemplo)

# Crear el árbol XML y escribirlo en un archivo
tree = ET.ElementTree(pregunta_quicksort)
tree.write("pregunta_quicksort.xml", encoding="utf-8", xml_declaration=True)