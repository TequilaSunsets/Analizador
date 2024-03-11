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
            if automata.r1 == None:
                automata.estados[automata.estado_final.id-1].agregar_transicion('ε', automata.estados[automata.referencia.id+1].id)
                automata.referencia.agregar_transicion('ε',automata.estado_final.id)
            else:
                automata.r1.agregar_transicion('ε',automata.referencia.id)
                automata.referencia.agregar_transicion('ε', automata.estado_final.id)

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


expresion = "((a|b)|a)*"
automata = construir_automata(expresion)
imprimir_automata(automata)

