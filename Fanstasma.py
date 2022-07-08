# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 18:43:19 2022

@author: noesi


Clyde, naranja, se acerca a menos de 8 cuadros de distancia. abajo izquierda


Inky, azul cualquiera de los otros 3 abajo derecha

Pinky, rosa, busca emboscar a pacman, no se lo come directamente arriba izquierda

Blinky, rojo, persigue a pacman arriba derecha
"""


import Estrella as est
import random as rdm
import numpy as np

#%%
vel = 2

class Fantasma:
    def __init__(self, multiplicadorRes, FNombre, iniciox, inicioy):
        self.nombre = FNombre
        self.tiempo = 0
        self.vista = []
        self.descanso = 1000
        self.TInky = 0
        self.PInky = ""
        self.PuntoAnterior = []
        if self.nombre == "Clyde":
            self.color = (255,190,88)
        elif self.nombre == "Inky":
            self.color = (75,222,203)
        elif self.nombre == "Pinky":
            self.color = (253,194,212)
        elif self.nombre == "Blinky":
            self.color = (252,59,16)
        self.posicionx = int(iniciox*multiplicadorRes+multiplicadorRes/2)
        self.posiciony = int(inicioy*multiplicadorRes+multiplicadorRes/2)
    
#Clyde, naranja, se acerca a menos de 8 cuadros de distancia.
#Inky, azul cualquiera de los otros 3
#Pinky, rosa, busca emboscar a pacman, no se lo come directamente
#Blinky, rojo, persigue a pacman, nodo critico anterior a pacman

    def posicion(self):
        return self.posicionx, self.posiciony
    
    def direccion(self, Destino, intersecciones, multiplicadorRes, CorPac):        
        x = int(self.posicionx / multiplicadorRes)
        y = int(self.posiciony / multiplicadorRes)
        ruta = est.AEstrella([x,y], Destino, intersecciones)    
        direccion = []
        if(len(ruta) == 1):
            Coordenadas = CorPac
        else:
            self.PuntoAnterior = ruta[1]
            Coordenadas = ruta[1]
        if(Coordenadas == [6,14] or [x,y] == [6,14]):
            if(Coordenadas == [21,14] or [x,y] == [21,14]):
                Coordenadas2 = []
                Coordenadas2.append(x)
                Coordenadas2.append(y)
                x = Coordenadas[0]
                y = Coordenadas[1]
                Coordenadas = Coordenadas2
        if x == Coordenadas[0]:
            direccion.append(0)
            direccion.append((int(Coordenadas[1]-y)/abs(Coordenadas[1]-y)))
        else:
            direccion.append(int((Coordenadas[0]-x)/abs(Coordenadas[0]-x)))
            direccion.append(0)
        return direccion
    
    def gira(self, mapa, multiplicadorRes, Pac, PacAnt, PacSig, intersecciones):
        if self.nombre == "Inky":
            if(self.inky == 0):
                self.TInky = 500
                self.PInky = rdm.randint(0,2)
        if self.nombre == "Clyde" or (self.nombre == "Inky" and self.PInky == 0):
            if est.Distancia([int(self.posicionx / multiplicadorRes), int(self.posiciony / multiplicadorRes)], Pac, "Manhattan"):
                pass
            else:
                self.vista = self.direccion(PacAnt, intersecciones, multiplicadorRes, Pac)
        elif self.nombre == "Pinky" or (self.nombre == "Inky" and self.PInky == 1):
            self.vista = self.direccion(PacSig, intersecciones, multiplicadorRes, Pac)
        elif self.nombre == "Blinky" or (self.nombre == "Inky" and self.PInky == 2):
            self.vista = self.direccion(PacAnt, intersecciones, multiplicadorRes, Pac)
            
    def avanza(self, mapa, multiplicadorRes, Pac, PacAnt, PacSig, intersecciones):
        self.tiempo+= .5
        intersecciones = np.array(intersecciones, dtype=object)
        if(self.posicionx % multiplicadorRes == int(multiplicadorRes/2) and self.posiciony % multiplicadorRes == int(multiplicadorRes/2)):
            if([int(self.posicionx/multiplicadorRes), int(self.posiciony/multiplicadorRes)] in list(intersecciones[:,0])):
                self.gira(mapa, multiplicadorRes, Pac, PacAnt, PacSig, intersecciones)
        self.posicionx, self.posiciony = est.ConvierteMapa(self.posicionx, self.posiciony, len(mapa[0]) * multiplicadorRes , len(mapa) * multiplicadorRes, self.vista[0] * vel, self.vista[1] * vel)
        
            
            