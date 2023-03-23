# Libreria para expresiones regulares
import re

# TODO
# Cambiar diccionarios (a exepcion de reservedWord) por expresiones regulares
# Cambiar los contadores que dependen de los diccionarios

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
                             'sinosi' : 'Palabra reservada',
                             'mientras': 'Palabra reservada',
                             'hacer': 'Palabra reservada',
                             'para' : 'Palabra reservada'}
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

        def check_syntax(lines):
            for i, line in enumerate(lines):
                print(line)
                if "if" in line:
                    # Look for opening bracket
                    try:
                        start_index = line.index("{")

                    except ValueError:
                        print(f"Error: Line {i + 1}: Missing opening bracket for if statement")
                        return False

                    # Check if there's a closing bracket on the same line
                    if "}" in line:
                        try:
                            end_index = line.index("}")
                            if end_index < start_index:
                                print(f"Error: Line {i + 1}: Closing bracket before opening bracket")
                                return False
                        except ValueError:
                            pass  # Ignore closing brackets on same line

                    # Look for closing bracket on subsequent lines
                    else:
                        found_closing_bracket = False
                        for j in range(i + 1, len(lines)):
                            if "}" in lines[j]:
                                found_closing_bracket = True
                                break
                        if not found_closing_bracket:
                            print(f"Error: Line {i + 1}: Missing closing bracket for if statement")
                            return False

            return True

        def complete_if_statement(statement):
            pass

        def check_if_statement(statement):
            return 'sale if'

            pattern = r"\s*if\s*\(\s*(.*)\s*\)\s*\{\s*(.*)\s*\}\s*"

            match = re.match(pattern, statement)
            if match:
                condition, body = match.groups()
                print("The if-statement is correctly formatted.")
            else:
                print("The if-statement is not correctly formatted.")

        # Extraer el contenido del archivo
        content = file.read()

        # Declaracion de variables
        declaration = 0            # Contador para ver el numero de linea que toca
        message = ""            # Mensaje final

        program = content.split("\n")
        print(program)

        for i, token in enumerate(program):
            if token != '':
                declaration += 1
                message += f"Info declaracion: {declaration}:\n"

                if 'si' not in token:
                    message += f"{check_variable_declaration(token)}"

                elif 'sino' not in token:
                    test = ''
                    print(f"Start: {test}")

                    for new_token in program[i:]:
                        test += f"{new_token}"

                        if '}' in new_token and 'sino' not in new_token:
                            break

                        print(test)

                    print(f"Final: {test}")

                    message += f"{check_if_statement(token)}"

                    # print(check_syntax(program[i:]))

                message += f"\n\n\n"

        file.close()
        return message

    def get_counters(self):
        print(self.countSign)
        print(self.countIdentifier)
        print(self.countOperator)
        print(self.countReserverdWord)
