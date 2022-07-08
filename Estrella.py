# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:18:31 2022

@author: noesi
"""
import math

def Distancia(Origen, Destino, Tipo = "Manhattan"):
    if(Tipo == "Manhattan"):
        return (abs(Origen[0]-Destino[0]) + abs(Origen[1] - Destino[1]))
    if(Tipo == "Euclidiana"):
        return math.sqrt(math.pow(Origen[0]-Destino[0], 2) + math.pow(Origen[1]-Destino[1], 2))
    
def ConvierteMapa(X, Y, xmax, ymax, sumx, sumy):
        X = (X + sumx + xmax)%xmax
        Y = (Y + sumy + ymax)%ymax
        return [X,Y]

def MenorPeso(lista):
    menor = int(lista[0][1]) + int(lista[0][2])
    indice = 0
    suma = 0
    if(len(lista) > 1):
        for i in (range(len(lista)-1)):
            suma = int(lista[i][1]) + int(lista[i][2])
            if(suma<menor):
                menor = suma
                indice = i
        return lista[indice], lista[:indice] + lista[indice+1:]
    elif len(lista) == 1:
        return lista[0], []
    else:
        return -1, -1
            
def AEstrella(Origen, Destino, Intersecciones):
    Resuelto = []
    PorResolver = []
    CorResueltas = []
    TipodeDistancia = "Manhattan"
    '''Para los nodos necitamos guardar:
    -Coordenadas del nodo
    -Distancia recorrida desde el origen hasta el nodo
    -Heuristica
    -Padre'''
    PorResolver.append([Origen, 0, Distancia(Origen, Destino, TipodeDistancia), ""])
    encontrado = False
    n = -1
    while not encontrado:
        #Sacamos el primer elemento de por resolver
        n+= 1
        Nodo, PorResolver = MenorPeso(PorResolver)
        #Si es el destino, terminamos de buscar
        if(Nodo[0] == Destino):
            encontrado = True
            Resuelto.append(Nodo)
        #Si ya esta en Resuelto no hacer nada
        elif(Nodo[0] in CorResueltas):
            pass
        #De otra forma revisamos los nodos que están conectados al que sacamos
        else:
            Resuelto.append(Nodo)
            CorResueltas.append(Nodo[0])
            for i in Intersecciones:
                if i[0] == Nodo[0]:
                    for j in i[1]:
                        agrega = []
                        agrega = [j, Nodo[1] + Distancia(Nodo[0], j, TipodeDistancia), Distancia(j, Destino, TipodeDistancia), Nodo[0]]
                        PorResolver.append(agrega)
    #Aqui ya tenemos el camino, solo es desenvolverlo
    encontrado = False
    Nodo = Resuelto[-1]
    Camino = []
    CamCor = []
    while(not encontrado):
        Camino.append(Nodo)
        CamCor.append(Nodo[0])
        if(Nodo[0] == Origen):
            encontrado = True
        else:
            Nodo = Resuelto[CorResueltas.index(Nodo[3])]
    CamCor = CamCor[::-1]
    return CamCor
