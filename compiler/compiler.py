# Libreria para expresiones regulares
import numbers
import re


class Compiler:
    def __init__(self, file):
        # Declaramos el archivo
        self.file = file

        self.countReserverdWordPrint = 0
        self.countIdentifierPrint = 0
        self.countOperatorPrint = 0
        self.countSignPrint = 0

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

        self.declared_variables = {}
        self.declared_variables_keys = self.declared_variables.keys()

    # Analisis del archivo completo y sus cadenas
    def parse(self):
        file = open(self.file)

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
                        # check_declaration_value(declaration)

                        return message
                    except:
                        return f"{declaration}\nEl valor de la variable no esta en el formato correcto"
                else:
                    return f"{declaration}\nEl tipo de variable no es correcto"
            else:
                is_modification = check_variable_modification(declaration)
                if not(is_modification[1]):
                    return f"{declaration}\nLa declaracion de la variable no es correcta"

                else:
                    return is_modification[0]

        def check_variable_modification(modification):
            pattern = r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([+\-]?=)\s*([^;\n\r]+)\s*;"

            match = re.match(pattern, modification)

            if not(match):
                return f"{modification} esta mal declarado"

            else:
                var_name = match.group(1)

                if var_name not in self.declared_variables_keys:
                    return f"{var_name} no existe", False

                else:
                    # value = match.group(3)
                    # prev_value = self.declared_variables[var_name]
                    # mod_value = match.group(3)
                    #
                    # operation = match.group(2)
                    # if operation == "=":
                    #     new_value = mod_value
                    #
                    # elif operation == "+=":
                    #     if isinstance(prev_value, numbers.Number):
                    #         print('int')
                    #         new_value = prev_value + mod_value
                    #
                    #     elif isinstance(prev_value, float):
                    #         print('float')
                    #         new_value = float(prev_value) + float(mod_value)
                    #
                    #     elif isinstance(prev_value, str):
                    #         print('string')
                    #         prev_value = prev_value.replace('"', '')
                    #         mod_value = mod_value.replace('"', '')
                    #
                    #         new_value = prev_value + mod_value
                    #
                    # elif operation == "-=":
                    #     new_value = prev_value - mod_value

                    # self.declared_variables[var_name] = new_value

                    return f"Modificacion de variable\nNombre de variable: {var_name}\n", True

        def check_if_statement(statement):
            pattern = r"\s*si\s*\(.+\)\s*\{\s*.+\s*\}(?:\s*sino\s+si\s*\(.+\)\s*\{\s*.+\s*\})*(?:\s*sino\s*\{" \
                      r"\s*.+\s*\})?"

            match = re.match(pattern, statement)
            if match:
                message = 'Palabras reservadas: si, sino, sino si\n'
                return message
            else:
                return "La condicion esta mal declarada."

        # FUNCIONES CONTADORES

        def check_operator_in_token(token):
            pattern = r"[\+\-\*\/\%\=\==\<\>\>=\<=]"
            match = re.search(pattern, token)

            if match:
                return True
            else:
                return False

        def check_identifier_in_token(token):
            pattern = r"[a-zA-Z][a-zA-Z0-9]*"
            match = re.search(pattern, token)

            if match:
                return True
            else:
                return False

        def check_reserverdWord_in_token(token):
            pattern = r"\b(entero|decimal|booleano|cadena|si|sino|sino si|mientras|hacer|verdadero|falso)\b"
            match = re.search(pattern, token)

            if match:
                return True
            else:
                return False

        def check_sign_in_token(token):
            pattern = r"[\(\)\{\}\"\;]"
            match = re.search(pattern, token)

            if match:
                return True
            else:
                return False

        def is_token_sign(token):
            pattern = r"[\(\)\{\}\"\;]"
            match = re.match(pattern, token)

            if match:
                return True
            else:
                return False

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

                if check_operator_in_token(token):
                    self.countOperatorPrint += 1

                if check_reserverdWord_in_token(token):
                    self.countReserverdWordPrint += 1

                if check_sign_in_token(token):
                    self.countSignPrint += 1

                if check_identifier_in_token(token):
                    self.countIdentifierPrint += 1

                if 'si' in token and 'sino' not in token:
                    token = ''

                    for new_token in program[i:]:
                        token += f"{new_token}"

                        if '}' in new_token and 'sino' not in new_token:
                            break

                    message += f"{check_if_statement(token)}"

                elif 'sino' in token or 'sino si' in token:
                    continue

                elif '#' in token:
                    message += f"Comentario {token}"

                elif is_token_sign(token):
                    continue

                else:
                    message += f"{check_variable_declaration(token)}"

                message += f"\n\n\n"

        file.close()
        return message
