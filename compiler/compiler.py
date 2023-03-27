# Libreria para expresiones regulares
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
                if not (is_modification[1]):
                    return f"{declaration}\nLa declaracion de la variable no es correcta"

                else:
                    return is_modification[0]

        def check_variable_modification(modification):
            pattern = r"\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([+\-]?=)\s*([^;\n\r]+)\s*;"

            match = re.match(pattern, modification)

            if not (match):
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
                    #
                    # self.declared_variables[var_name] = new_value

                    return f"Modificacion de variable\nNombre de variable: {var_name}\n", True

        def check_condition_statement(statement):
            pattern = r"\(\s*([a-zA-Z0-9]*)\s*([==|!=|>=|<=|>|<|is])\s*(.*)\)"

            match = re.match(pattern, statement)

            if not (match):
                return f"{statement} mal declarado"

            else:
                return f"{statement} bien declarado"

        def check_if_statement(statement):
            pattern = r"\s*(si)\s*(\(.+\))\s*(\{\s*.+\s*\})\s*(sino\s+si)" \
                      r"\s*(\(.+\))\s*(\{\s*.+\s*\})*\s*(sino)\s*(\{\s*.+\s*\})?"

            match = re.match(pattern, statement)
            if match:
                reserved1, reserved2, reserved3 = match.group(1), match.group(4) if not None else '', \
                                                  match.group(7) if not None else ''

                main_condition, other_conditions = match.group(2), match.group(5)

                action1, action2, action3 = match.group(3), match.group(6), match.group(8)

                message = f"Palabras reservadas: {reserved1}, {reserved2}, {reserved3}\n" \
                          f"Condiciones: {check_condition_statement(main_condition)}, " \
                          f"{check_condition_statement(other_conditions)}\nAcciones: {action1}, {action2}, {action3}"

                return message
            else:
                return "La condicion esta mal declarada."

        def is_token_sign(token):
            pattern = r"[\(\)\{\}\"\;]"
            match = re.match(pattern, token)

            if match:
                return True
            else:
                return False

        def check_doWhile_statement(statement):
            pattern = r"hacer\s*\{[\s\S]*?\}\s*mientras\s*\((.+?)\)\s*;"
            expresion = re.compile(pattern)

            if expresion.match(statement):
                message = 'Palabra reservada: hacer-mientras'
                return message

            else:
                return "La condicion -hacer/mientras- esta mal declarada"

        def check_while_statement(statement):
            pattern = r"mientras\s*\(([^;]+)\)\s*\{([\s\S]*?)\}"
            regex = re.compile(pattern)

            if regex.match(statement):
                message = 'Palabra reservada: mientras'
                return message
            else:
                return "La condicion -mientras- esta mal declarada"

        # FUNCIONES CONTADORES

        def check_sign_in_token(token):
            pattern = r"[\(\)\{\}\"\;]"
            match = re.findall(pattern, token)

            if match:
                return len(match)

        def check_operator_in_token(token):
            pattern = r"[\+\-\*\/\%\=\==\<\>\>=\<=]"
            match = re.findall(pattern, token)

            if match:
                return len(match)

        def check_identifier_in_token(token):
            pattern = r'\b(?!entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso|[0-9])\w+(?!\w*;)(?=(?:[^"]|"[^"]*")*$)\b'
            # \b(?!entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso)[^\W\d]+\b(?=(?:(?:[^"]*"){2})*[^"]*$) casi funciona
            # \b(?!entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso|"|[0-9])\w+\b casi funciona x2 pero reconoce tambien los valores que se le da a la variable
            match = re.findall(pattern, token)

            if match:
                return len(match)

        def check_reserverdWord_in_token(token):
            pattern = r"\b(entero|decimal|booleano|cadena|si|sino|sino si|mientras|hacer|verdadero|falso)\b"
            match = re.findall(pattern, token)

            if match:
                return len(match)

        # Extraer el contenido del archivo
        content = file.read()

        # Declaracion de variables
        declaration = 0  # Contador para ver el numero de linea que toca
        message = ""  # Mensaje final
        message2 = ""

        program = content.split("\n")

        for i, token in enumerate(program):
            if token != '':

                declaration += 1
                message += f"Info declaracion: {declaration}:\n"

                if check_operator_in_token(token):
                    self.countOperatorPrint += check_operator_in_token(token)

                if check_reserverdWord_in_token(token):

                    self.countReserverdWordPrint += check_reserverdWord_in_token(token)

                if check_sign_in_token(token):
                    self.countSignPrint += check_sign_in_token(token)

                if check_identifier_in_token(token):
                    print(f"{declaration}: {check_identifier_in_token(token)}")
                    self.countIdentifierPrint += check_identifier_in_token(token)

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

                if 'hacer' in token and 'mientras' not in token:
                    for new_token in program[i:]:
                        token += f"{new_token}"

                        if '}' in new_token and 'mientras' not in new_token:
                            break
                    message += f"{check_doWhile_statement(token)}\n"

                if 'hacer' in token:
                    message2 += f"{check_while_statement(token)}"

                message += f"\n\n\n"

        file.close()
        return message + message2
