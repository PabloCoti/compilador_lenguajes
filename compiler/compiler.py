# Libreria para expresiones regulares
import re


# TODO
# Cambiar diccionarios (a exepcion de reservedWord) por expresiones regulares
# Cambiar los contadores que dependen de los diccionarios
# AGREGAR METODOS PARA LOS CONTADORES Y HACER QUE FUCIONEN DENTRO DE LA INTERFAZ

class Compiler:
    def __init__(self, file):
        # Declaramos el archivo
        self.file = file

        # Declaramos contadores de palabras reservadas
        self.countReserverdWord = 0
        self.countIdentifier = 0
        self.countOperator = 0
        self.countSign = 0

        # Declaramos un diccionario "reservedWord" para saber todos los tkns
        self.reservedWord = {'entero': 'Palabra reservada',
                             'decimal': 'Palabra reservada',
                             'booleano': 'Palabra reservada',
                             'cadena': 'Palabra reservada',
                             'si': 'Palabra reservada',
                             'sino': 'Palabra reservada',
                             'sino si': 'Palabra reservada',
                             'mientras': 'Palabra reservada',
                             'hacer': 'Palabra reservada',
                             'para': 'Palabra reservada'}
        self.reservedWord_key = self.reservedWord.keys()

        # Declaramos un diccionario "operator" para saber todos los tkns
        self.operator = {'+': 'Operador',
                         '-': 'Operador',
                         '*': 'Operador',
                         '/': 'Operador',
                         '%': 'Operador',
                         '=': 'Operador',
                         '==': 'Operador',
                         '<': 'Operador',
                         '>': 'Operador',
                         '>=': 'Operador',
                         '<=': 'Operador'}
        self.operator_key = self.operator.keys()

        # Declaramos un diccionario "sign" para saber todos los tkns
        self.sign = {'(': 'Signo',
                     ')': 'Signo',
                     '{': 'Signo',
                     '}': 'Signo',
                     '"': 'Signo',
                     ';': 'Signo'}
        self.sign_key = self.sign.keys()

        # Declaramos un diccionario "identifier" para saber los tkns
        self.identifier = {'a': 'Identificador',
                           'b': 'Identificador',
                           'c': 'Identificador',
                           'd': 'Identificador',
                           'e': 'Identificador',
                           'f': 'Identificador',
                           'g': 'Identificador',
                           'h': 'Identificador',
                           'i': 'Identificador',
                           'j': 'Identificador',
                           'k': 'Identificador',
                           'l': 'Identificador',
                           'm': 'Identificador',
                           'n': 'Identificador',
                           'ñ': 'Identificador',
                           'o': 'Identificador',
                           'p': 'Identificador',
                           'q': 'Identificador',
                           'r': 'Identificador',
                           's': 'Identificador',
                           't': 'Identificador',
                           'u': 'Identificador',
                           'v': 'Identificador',
                           'w': 'Identificador',
                           'x': 'Identificador',
                           'y': 'Identificador',
                           'z': 'Identificador'}
        self.identifier_key = self.identifier.keys()

        self.declared_variables = {}
        self.declared_variables_keys = self.declared_variables.keys()

    # Analisis del archivo completo y sus cadenas
    def parse(self):
        file = open(self.file)

        def check_declaration_value(declaration):
            tokens = declaration.split()

            for token in tokens:
                if token in self.operator:
                    self.countOperator += 1

                elif token in self.sign:
                    self.countSign += 1

                elif token in self.identifier:
                    self.countIdentifier += 1

        def check_variable_declaration(declaration):
            pattern = r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^;]+)\s*;"

            match = re.match(pattern, declaration)

            if match:
                type = match.group(1)

                if type in self.reservedWord_key:
                    try:
                        name = match.group(2)
                        value = match.group(3)

                        self.declared_variables[name] = value

                        message = f"Tipo de variable: {type}\nNombre de variable: {name}\nValor de la variable: {value}"

                        eval(value)
                        self.countReserverdWord += 1
                        check_declaration_value(declaration)

                        return message
                    except:
                        return f"{declaration}\nEl valor de la variable no esta en el formato correcto"
                else:
                    return f"{declaration}\nEl tipo de variable no es correcto"
            else:
                return f"{declaration}\nLa declaracion de la variable no es correcta"

        def check_variable_modification(modification):
            pass

        def check_if_statement(statement):
            pattern = r"\s*si\s*\(.+\)\s*\{\s*.+\s*\}(?:\s*sino\s+si\s*\(.+\)\s*\{\s*.+\s*\})*(?:\s*sino\s*\{\s*.+\s*\})?"

            match = re.match(pattern, statement)
            if match:
                message = 'Palabras reservadas: si, sino, sino si\n'
                return message
            else:
                return "La condicion esta mal declarada."

        # EJEMPLO DE CONTADORESSSSSSSSSSSSSSSSSSSSSSSSSSSS
        def check_operator_in_token(token):
            pattern = r"expresion regular"

            match = re.match(pattern, token)
            if match:
                self.countOperator += 1

        # Extraer el contenido del archivo
        content = file.read()

        # Declaracion de variables
        declaration = 0  # Contador para ver el numero de linea que toca
        message = ""  # Mensaje final

        program = content.split("\n")

        for i, token in enumerate(program):
            if token != '':
                declaration += 1
                message += f"Info declaracion: {declaration}:\n"

                check_operator_in_token(token)

                if 'si' in token and 'sino' not in token:
                    token = ''

                    for new_token in program[i:]:
                        token += f"{new_token}"

                        if '}' in new_token and 'sino' not in new_token:
                            break

                    message += f"{check_if_statement(token)}"

                elif 'sino' in token or 'sino si' in token:
                    continue

                else:
                    message += f"{check_variable_declaration(token)}"

                message += f"\n\n\n"

        file.close()
        return message

    def get_counters(self):
        print(self.countSign)
        print(self.countIdentifier)
        print(self.countOperator)
        print(self.countReserverdWord)
