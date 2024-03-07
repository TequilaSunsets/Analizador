class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.transiciones = {}

class Automata:
    def __init__(self):
        self.estados = []
        self.estado_inicial = None
        self.estado_final = None

    def agregar_estado(self, estado):
        self.estados.append(estado)

    def agregar_transicion(self, estado_origen, simbolo, estado_destino):
        if estado_origen in self.estados:
            if simbolo in estado_origen.transiciones:
                estado_origen.transiciones[simbolo].append(estado_destino)
            else:
                estado_origen.transiciones[simbolo] = [estado_destino]

    def establecer_estado_inicial(self, estado):
        if estado in self.estados:
            self.estado_inicial = estado

    def establecer_estado_final(self, estado):
        if estado in self.estados:
            self.estado_final = estado

def thompson(expresion_regular):
    automata = Automata()
    pila = []

    for caracter in expresion_regular:
        if caracter == '(':
            pila.append(caracter)
        elif caracter == ')':
            operadores = []
            while pila[-1] != '(':
                operadores.append(pila.pop())
            pila.pop()  # Eliminar el paréntesis izquierdo '('

            operador = operadores.pop() if operadores else None
            if operador == '*':
                estado_final = pila.pop()
                estado_inicial = Estado('q' + str(len(automata.estados) + 1))
                automata.agregar_estado(estado_inicial)
                automata.establecer_estado_inicial(estado_inicial)
                automata.establecer_estado_final(estado_inicial)

                automata.agregar_transicion(estado_inicial, '', estado_final)
                automata.agregar_transicion(estado_inicial, '', automata.estado_final)
                automata.agregar_transicion(automata.estado_final, '', estado_inicial)
                pila.append(estado_inicial)
            elif operador == '.':
                estado_final = pila.pop()
                estado_inicial = pila.pop()
                automata.agregar_transicion(estado_inicial, '', estado_final)
                pila.append(estado_inicial)
            elif operador == '|':
                estado_final1 = pila.pop()
                estado_inicial1 = pila.pop()
                estado_final2 = pila.pop()
                estado_inicial2 = pila.pop()

                estado_inicial = Estado('q' + str(len(automata.estados) + 1))
                estado_final = Estado('q' + str(len(automata.estados) + 2))
                automata.agregar_estado(estado_inicial)
                automata.agregar_estado(estado_final)
                automata.establecer_estado_inicial(estado_inicial)
                automata.establecer_estado_final(estado_final)

                automata.agregar_transicion(estado_inicial, '', estado_inicial1)
                automata.agregar_transicion(estado_inicial, '', estado_inicial2)
                automata.agregar_transicion(estado_final1, '', estado_final)
                automata.agregar_transicion(estado_final2, '', estado_final)
                pila.append(estado_inicial)
                pila.append(estado_final)
        elif caracter in ['|', '.', '*']:
            pila.append(caracter)
        else:
            estado_inicial = Estado('q' + str(len(automata.estados) + 1))
            estado_final = Estado('q' + str(len(automata.estados) + 2))
            automata.agregar_estado(estado_inicial)
            automata.agregar_estado(estado_final)
            automata.establecer_estado_inicial(estado_inicial)
            automata.establecer_estado_final(estado_final)

            automata.agregar_transicion(estado_inicial, caracter, estado_final)
            pila.append(estado_inicial)
            pila.append(estado_final)

    return automata

def visualizar_automata(automata):
    print("Automata:")
    for estado in automata.estados:
        print(f"Estado: {estado.nombre}")
        for simbolo, estados_destino in estado.transiciones.items():
            for estado_destino in estados_destino:
                print(f"  --> '{simbolo}' --> {estado_destino.nombre}")

# Ejemplo de uso
expresion_regular = "(a|b)*.c"
automata = thompson(expresion_regular)
visualizar_automata(automata)