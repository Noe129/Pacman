# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 22:18:42 2022

@author: noesi
"""
'''
0 <-
1 arriba
2 ->
3 abajo
'''

import numpy as np
import Estrella as est

vel = 2

class PPacman:
    def __init__(self, multiplicadorRes):
        self.posicionx = int(14*multiplicadorRes+multiplicadorRes/2)
        self.posiciony = int(23*multiplicadorRes+multiplicadorRes/2)
        self.direccion = [-1,0]
        self.direccionan = [-1,0]
        self.matdir = [[-1,0],
                       [0,-1],
                       [1,0],
                       [0,1]
                       ]
        self.permitirgirod = True
        self.permitirgiroi = True
        self.puntocritico = [14,23]
        self.puntocriticoant = [14,23]
        self.puntocriticosig = []
        self.vivo = True
        self.comida = 0
        
    def posicion(self):
        return self.posicionx, self.posiciony
    
    def mueve(self):
        self.posicionx += vel * self.direccionan[0]
        self.posiciony += vel * self.direccionan[1]
    
    def avanza(self, mapa, multiplicadorRes, intersecciones):
        casilla = [int(self.posicionx / multiplicadorRes), int(self.posiciony / multiplicadorRes)]
        objetivo = [casilla[0] + self.direccionan[0], casilla[1] + self.direccionan[1]]
        objetivodeseado = [casilla[0] + self.direccion[0], casilla[1] + self.direccion[1]]
        centro = multiplicadorRes / 2
        if (objetivo[0] >= len(mapa[0]) or objetivodeseado[0] >= len(mapa[0])) and self.direccionan == [1,0] :
            casilla[0] = 0
            objetivo[0] = 1
            objetivodeseado = objetivo
            self.posicionx = centro+2
        if objetivo[0] < 0 or casilla[0] < 0 and self.direccionan == self.matdir[0]:
            casilla[0] = len(mapa[0]) - 1
            objetivo[0] = len(mapa[0]) - 2
            objetivodeseado = objetivo
            self.posicionx = len(mapa[0]) * multiplicadorRes - centro
        if(self.posicionx % multiplicadorRes == centro and self.posiciony % multiplicadorRes == centro) and ("-1" not in mapa[(objetivodeseado[1]+len(mapa))%len(mapa)][(len(mapa[0])+objetivodeseado[0])%len(mapa[0])]):
            self.permitirgirod = True
            self.permitirgiroi = True
            self.direccionan = self.direccion
            self.mueve()
            intersecciones = np.array(intersecciones, dtype=object)
            if([int(self.posicionx/multiplicadorRes), int(self.posiciony/multiplicadorRes)] in list(intersecciones[:,0])):
                lista = intersecciones[:,0]
                lista = lista.tolist()
                self.puntocritico = [int(self.posicionx/multiplicadorRes), int(self.posiciony/multiplicadorRes)]
                sig = [self.puntocritico[0] + self.direccionan[0], self.puntocritico[1] + self.direccionan[1]]
                encontrado = False
                while not encontrado:
                    if(sig in list(intersecciones[lista.index(self.puntocritico),1])):
                        self.puntocriticosig = sig
                        encontrado = True
                    else:
                        sig = est.ConvierteMapa(sig[0], sig[1], len(mapa[0]), len(mapa), self.direccionan[0], self.direccion[1])
        elif(self.posicionx % multiplicadorRes == centro and self.direccionan[0] != 0) or (self.posiciony % multiplicadorRes == centro and self.direccionan[1] != 0):
            if("-1" not in mapa[objetivo[1]][objetivo[0]]):
                self.mueve()
        else:
            self.mueve()
        if("1" in mapa[casilla[1]][casilla[0]]):
            if(self.posicionx % multiplicadorRes > multiplicadorRes/4 and self.posicionx % multiplicadorRes < multiplicadorRes-multiplicadorRes/4 and self.posiciony % multiplicadorRes > multiplicadorRes/4 and self.posiciony % multiplicadorRes < multiplicadorRes-multiplicadorRes/4):
                self.comida += 1
                mapa[casilla[1]][casilla[0]] = "0"
        return mapa
    
    def gira(self, cambio):
        if(cambio == 0):
            self.direccion = self.matdir[(self.matdir.index(self.direccionan))]
            self.permitirgirod = True
            self.permitirgiroi = True
        if(cambio == 1 and self.permitirgirod):#1 derecha
            self.permitirgirod = False
            self.permitirgiroi = True
            self.direccion = self.matdir[(self.matdir.index(self.direccionan) + 1) % 4]    
        if(cambio == 2 and self.permitirgiroi):
            self.permitirgiroi = False
            self.permitirgirod = True
            self.direccion = self.matdir[((self.matdir.index(self.direccionan) - 1) + 4) % 4]    
        if(cambio == 3):
            indice = self.matdir.index(self.direccionan)
            self.direccion = self.matdir[(indice+2)%4]
            self.direccionan = self.direccion
            self.permitirgirod = True
            self.permitirgiroi = True