# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:12:34 2024

@author: naked
"""

#Codigo para el analizador de expresiones regulares#

#Sugiero que no se acepte la operacion de cerradura positiva, para simplificar
#las expresiones regulares.

class Estado:
    def __init__(self, id):
        self.id = id
        self.transiciones = {}

    def agregar_transicion(self, simbolo, estado):
        if simbolo in self.transiciones:
            self.transiciones[simbolo].append(estado)
        else:
            self.transiciones[simbolo] = [estado]


class Automata:
    def __init__(self):
        self.estados = {}
        self.estado_inicial = None
        self.estado_final = None
        self.alfabeto = []
        self.referencia = None
        self.r1 = None

    def agregar_estado(self, id):
        estado = Estado(id)
        self.estados[id] = estado
        return estado

    def definir_estado_inicial(self, estado):
        self.estado_inicial = estado

    def definir_estado_final(self, estado):
        self.estado_final = estado

    def agregar_simbolo(self, simbolo):
        if simbolo in self.alfabeto:
            return
        else:
            self.alfabeto.append(simbolo)

def construir_automata(expresion):
    automata = Automata()
    estado_inicial = automata.agregar_estado(0)
    estado_final = estado_inicial
    automata.definir_estado_inicial(estado_inicial)
    automata.definir_estado_final(estado_final)
    automata.referencia = estado_final
    

    for i in range(len(expresion)):
        if expresion[i] == '(':
            if expresion[i-1] == '(':
                pass
            else:
                r1 = automata.referencia
                nuevo_estado = automata.agregar_estado(len(automata.estados))
                automata.referencia.agregar_transicion('ε',nuevo_estado.id)
                automata.definir_estado_final(nuevo_estado)

        elif expresion[i] == ')':
            automata.referencia = r1
            nuevo_estado = automata.agregar_estado(len(automata.estados))
            automata.estado_final.agregar_transicion('ε', nuevo_estado.id)
            automata.definir_estado_final(nuevo_estado)

        elif expresion[i] == '*':
            automata.estado_final.agregar_transicion('ε', automata.referencia.id)
            automata.referencia.agregar_transicion('ε',automata.estado_final.id)

        elif expresion[i] == '|':
            automata.r1 = automata.estado_final
            automata.definir_estado_final(automata.referencia)

        else:
            if expresion[i] not in automata.alfabeto:
                automata.alfabeto.append(expresion[i])

            if expresion[i-1] == '|':
                nuevo_estado = automata.agregar_estado(len(automata.estados)) #Creamos un nuevo estado
                automata.referencia = automata.estado_final
                automata.estado_final.agregar_transicion('ε', nuevo_estado.id)
                automata.definir_estado_final(nuevo_estado) #Definimos el nuevo estado como estado final
                nuevo_estado = automata.agregar_estado(len(automata.estados)) #Creamos un nuevo estado
                automata.estado_final.agregar_transicion(expresion[i],nuevo_estado.id) #Agregamos una transicion del estado final al nuevo estado con el simbolo
                automata.definir_estado_final(nuevo_estado) #Definimos el nuevo estado como estado final
                automata.estado_final.agregar_transicion('ε', automata.r1.id)
                automata.definir_estado_final(automata.r1)

            else:
                nuevo_estado = automata.agregar_estado(len(automata.estados)) #Creamos un nuevo estado
                automata.referencia = automata.estado_final
                automata.estado_final.agregar_transicion('ε', nuevo_estado.id)
                automata.definir_estado_final(nuevo_estado) #Definimos el nuevo estado como estado final
                nuevo_estado = automata.agregar_estado(len(automata.estados)) #Creamos un nuevo estado
                automata.estado_final.agregar_transicion(expresion[i],nuevo_estado.id) #Agregamos una transicion del estado final al nuevo estado con el simbolo
                automata.definir_estado_final(nuevo_estado) #Definimos el nuevo estado como estado final
                nuevo_estado = automata.agregar_estado(len(automata.estados)) #Creamos un nuevo estado
                automata.estado_final.agregar_transicion('ε',nuevo_estado.id) #Agregamos una transicion con la cadena vacia del estado final al nuevo estado
                automata.definir_estado_final(nuevo_estado) #Definimos el nuevo estado como estado final
            
    return automata

def imprimir_automata(automata):
    for id, estado in automata.estados.items():
        print(f"Estado {id}: {estado.transiciones}")
    print("Estado inicial:", automata.estado_inicial.id)
    print("Estado final:", automata.estado_final.id)
    print("Alfabeto", automata.alfabeto)


def cadena_aceptada(automata, cadena):
    visited = set()  # Conjunto para realizar un seguimiento de los estados visitados

    def dfs(estado_actual, indice):
        # Creamos una tupla que representa el estado actual y la posición en la cadena
        estado_actual_tupla = (estado_actual.id, indice)
        
        # Si ya hemos visitado este estado con la misma posición en la cadena, retornamos False
        if estado_actual_tupla in visited:
            return False

        # Agregamos el estado actual y la posición en la cadena al conjunto de visitados
        visited.add(estado_actual_tupla)

        if indice == len(cadena):
            if estado_actual == automata.estado_final:
                return True
            else:
                return False

        simbolo_actual = cadena[indice]

        if simbolo_actual in estado_actual.transiciones:
            for estado_siguiente in estado_actual.transiciones[simbolo_actual]:
                if dfs(automata.estados[estado_siguiente], indice + 1):
                    return True

        if 'ε' in estado_actual.transiciones:
            for estado_siguiente in estado_actual.transiciones['ε']:
                if dfs(automata.estados[estado_siguiente], indice):
                    return True

        return False

    return dfs(automata.estado_inicial, 0)



expresiones = ["(a|b)","1(0|1)*1","ab*"]
automatas = []

for i in range(0,len(expresiones)):
    automatas+= [construir_automata(expresiones[i])]
    imprimir_automata(automatas[i])
    print()
    
cadena = "a"
for j in range(0, len(automatas)):
    if cadena_aceptada(automatas[j], cadena):
        print(f"La cadena '{cadena}' es aceptada por el autómata {j}.")
    else:
            print(f"La cadena '{cadena}' no es aceptada por el autómata {j}.")