# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:12:34 2024

@author: naked
"""

#Codigo para el analizador de expresiones regulares#

#Sugiero que no se acepte la operacion de cerradura positiva, para simplificar
#las expresiones regulares.

ER = ["(0+1)*","0(11)*0"]

class Estado:
    def __init__(self, id):
        self.id = id
        self.transiciones = {}

    def agregar_transicion(self, simbolo, estado):
        if simbolo == 'ε' and simbolo in self.transiciones:
            return
        elif simbolo in self.transiciones:
            print("Ya existe una transicion con este simbolo en este estado")
        else:
            self.transiciones[simbolo] = [estado]

class Automata:
    def __init__(self):
        self.estados = {}
        self.estado_inicial = None
        self.estado_final = None

    def agregar_estado(self, id):
        estado = Estado(id)
        self.estados[id] = estado
        return estado

    def definir_estado_inicial(self, estado):
        self.estado_inicial = estado

    def definir_estado_final(self, estado):
        self.estado_final = estado
   
    
def construir_automata:
    automata = Automata()
    estado_inicial = automata.agregar_estado(0)
    estado_final = automata.agregar_estado(1)
    automata.definir_estado_inicial(estado_inicial)
    automata.definir_estado_final(estado_final)


    for caracter in expresion:
        if caracter == '(':
            
        elif caracter == '|':

        elif caracter == '*':

        elif caracter == ')':

        elif caracter == '+':

        
