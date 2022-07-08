# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 22:12:33 2022

@author: noesi
"""
import pyglet
from pyglet.window import key
from pyglet import shapes
import pickle
import neat
import os
import PPacman as pac
import Fanstasma as fan
import Estrella as est
import numpy as np

class pacmann:
    
    def __init__(self):
        self.escala = 16
        self.pacman = pac.PPacman(self.escala)
        self.pinky = fan.Fantasma(self.escala, "Pinky", 1 , 1)
        self.blinky = fan.Fantasma(self.escala, "Blinky", 26 , 1)
        
        
    def cargamapa(self):
        archivo = open("C:/Users/noesi/Documents/Python/Pacman/Mapa.csv","r",encoding = "utf-8")
        mapa = archivo.read()
        archivo.close()
        mapa = mapa.split("\n")
        for i in range(len(mapa)):
            mapa[i] = mapa[i].split(",")
        mapa = mapa[:-1]
        return mapa

    def entrena_ia(self, genoma, config):
        red = neat.nn.FeedForwardNetwork.create(genoma, config)
        self.genome = genoma
        mapa = self.cargamapa()
        intersecciones = []
        for i in range(len(mapa) -1):
            for j in range(len(mapa[i])-1):
                if(mapa[i][j] != "-1"):
                    vecinosx = 0
                    vecinosy = 0
                    vecinos = []
                    if(mapa[(i+1)%len(mapa)][j] != "-1"):
                        vecinosy += 1
                        vecinos.append([j,(i+1)%len(mapa)])
                    if(mapa[(i-1+len(mapa))%len(mapa)][j] != "-1"):
                        vecinosy += 1
                        vecinos.append([j,(i-1+len(mapa))%len(mapa)])
                    if(mapa[i][(j+1)%len(mapa[i])] != "-1"):
                        vecinosx += 1
                        vecinos.append([(j+1)%len(mapa[i]),i])
                    if(mapa[i][(j-1+len(mapa[i]))%len(mapa[i])] != "-1"):
                        vecinosx += 1
                        vecinos.append([(j-1+len(mapa[i]))%len(mapa[i]),i])
                    if(vecinosx > 0 and vecinosy > 0):
                        intersecciones.append([[j,i],vecinos])
        intersecciones.append([[14,23], [[13,23],[15,23]]])
        intersecciones = np.array(intersecciones, dtype=object)
        n = 0
        for i in intersecciones:
            elementos = []
            for j in i[1]:
                encontrado = False
                nodo = []
                nodo.append(j[0])
                nodo.append(j[1])
                while(not encontrado):
                    if(nodo in list(intersecciones[:,0])):
                        elementos.append(nodo)
                        encontrado = True
                    else:
                        nodo[1] += j[1]-i[0][1]
                        nodo[0] += j[0]-i[0][0]
                        if(nodo[0] > len(mapa[0])):
                            nodo[0] = 0
                        if(nodo[1] > len(mapa)):
                            nodo[1] = 0
                        if(nodo[0] < 0):
                            nodo[0] = len(mapa[0])-1
                        if(nodo[1] < 0):
                            nodo[1] = len(mapa)-1
            intersecciones[n][1] = elementos
            n += 1   
        intersecciones = intersecciones.tolist()
        mapa = self.pacman.avanza(mapa, self.escala, intersecciones)
        #while(est.Distancia(self.pacman.posicion(), self.pinky.posicion()) > 4 and est.Distancia(self.pacman.posicion(), self.blinky.posicion()) > 4 and self.pacman.comida < 245 and self.pinky.tiempo < 6000):
        while(est.Distancia(self.pacman.posicion(), self.pinky.posicion()) > 4 and self.pacman.comida < 245 and self.pinky.tiempo < 6000):
            Entradas = []
            Entradas.append(self.pacman.posicionx)
            Entradas.append(self.pacman.posiciony)
            if(self.pacman.direccion == [-1,0]):
                Entradas.append(0)
            elif(self.pacman.direccion == [0,-1]):
                Entradas.append(1)
            elif(self.pacman.direccion == [1,0]):
                Entradas.append(2)
            elif(self.pacman.direccion == [0,1]):
                Entradas.append(3)
            Entradas.append(self.pacman.puntocriticosig[0])
            Entradas.append(self.pacman.puntocriticosig[1])
            contiguo = est.ConvierteMapa(self.pacman.posicionx/self.escala, self.pacman.posiciony/self.escala, len(mapa[0]), len(mapa), 1, 0)
            Entradas.append(mapa[int(contiguo[1])][int(contiguo[0])])
            contiguo = est.ConvierteMapa(self.pacman.posicionx/self.escala, self.pacman.posiciony/self.escala, len(mapa[0]), len(mapa), -1, 0)
            Entradas.append(mapa[int(contiguo[1])][int(contiguo[0])])
            contiguo = est.ConvierteMapa(self.pacman.posicionx/self.escala, self.pacman.posiciony/self.escala, len(mapa[0]), len(mapa), 0, 1)
            Entradas.append(mapa[int(contiguo[1])][int(contiguo[0])])
            contiguo = est.ConvierteMapa(self.pacman.posicionx/self.escala, self.pacman.posiciony/self.escala, len(mapa[0]), len(mapa), 0, -1)
            Entradas.append(mapa[int(contiguo[1])][int(contiguo[0])])
            Entradas.append(self.pinky.posicionx)
            Entradas.append(self.pinky.posiciony)
            Entradas.append(est.Distancia(self.pacman.posicion(), self.pinky.posicion()))
            #Entradas.append(self.blinky.posicionx)
            #Entradas.append(self.blinky.posiciony)
            #Entradas.append(est.Distancia(self.pacman.posicion(), self.blinky.posicion()))
            salida = red.activate(Entradas)
            decision = salida.index(max(salida))
            self.pacman.gira(decision)
            mapa = self.pacman.avanza(mapa, self.escala, intersecciones)
            mapa = self.pacman.avanza(mapa, self.escala, intersecciones)
            mapa = self.pacman.avanza(mapa, self.escala, intersecciones)
            self.pinky.avanza(mapa, self.escala, self.pacman.posicion(), self.pacman.puntocritico, self.pacman.puntocriticosig, intersecciones)
            self.pinky.avanza(mapa, self.escala, self.pacman.posicion(), self.pacman.puntocritico, self.pacman.puntocriticosig, intersecciones)
            #self.blinky.avanza(mapa, self.escala, self.pacman.posicion(), self.pacman.puntocritico, self.pacman.puntocriticosig, intersecciones)
            #self.blinky.avanza(mapa, self.escala, self.pacman.posicion(), self.pacman.puntocritico, self.pacman.puntocriticosig, intersecciones)
        self.genome.fitness = self.pacman.comida
        return self.genome.fitness
        
def test_ai(self, net):
    mapa = pacmann.cargamapa()
    intersecciones = []
    for i in range(len(mapa) -1):
        for j in range(len(mapa[i])-1):
            if(mapa[i][j] != "-1"):
                vecinosx = 0
                vecinosy = 0
                vecinos = []
                if(mapa[(i+1)%len(mapa)][j] != "-1"):
                    vecinosy += 1
                    vecinos.append([j,(i+1)%len(mapa)])
                if(mapa[(i-1+len(mapa))%len(mapa)][j] != "-1"):
                    vecinosy += 1
                    vecinos.append([j,(i-1+len(mapa))%len(mapa)])
                if(mapa[i][(j+1)%len(mapa[i])] != "-1"):
                    vecinosx += 1
                    vecinos.append([(j+1)%len(mapa[i]),i])
                if(mapa[i][(j-1+len(mapa[i]))%len(mapa[i])] != "-1"):
                    vecinosx += 1
                    vecinos.append([(j-1+len(mapa[i]))%len(mapa[i]),i])
                if(vecinosx > 0 and vecinosy > 0):
                    intersecciones.append([[j,i],vecinos])
    intersecciones.append([[14,23], [[13,23],[15,23]]])
    
    intersecciones = np.array(intersecciones, dtype=object)
    
    n = 0
    for i in intersecciones:
        elementos = []
        for j in i[1]:
            encontrado = False
            nodo = []
            nodo.append(j[0])
            nodo.append(j[1])
            while(not encontrado):
                if(nodo in list(intersecciones[:,0])):
                    elementos.append(nodo)
                    encontrado = True
                else:
                    nodo[1] += j[1]-i[0][1]
                    nodo[0] += j[0]-i[0][0]
                    if(nodo[0] > len(mapa[0])):
                        nodo[0] = 0
                    if(nodo[1] > len(mapa)):
                        nodo[1] = 0
                    if(nodo[0] < 0):
                        nodo[0] = len(mapa[0])-1
                    if(nodo[1] < 0):
                        nodo[1] = len(mapa)-1
        intersecciones[n][1] = elementos
        n += 1   
    intersecciones = intersecciones.tolist()
    escala = 16
    pacman = pac.PPacman(escala)
    pinky = fan.Fantasma(escala, "Pinky", 1 , 1)
    #pinky2 = fan.Fantasma(escala, "Pinky", 26 , 1)
    window = pyglet.window.Window(len(mapa[0]) * escala, len(mapa) * escala, resizable=False)
    batch = pyglet.graphics.Batch()

    

def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    return winner_net

def evalua_genomas(genomas, config):
    for i, (genome_id1, genome) in enumerate(genomas):
        print(round(i/len(genomas) * 100), end=" ")
        juego = pacmann()
        genome.fitness = 0
        genome.fitness = juego.entrena_ia(genome, config)
        

def corre_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1003')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(20))
    winner = p.run(evalua_genomas, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)
    

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config.txt")
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
corre_neat(config)
jugador = test_best_network(config)

def cargamapa():
    archivo = open("C:/Users/noesi/Documents/Python/Pacman/Mapa.csv","r",encoding = "utf-8")
    mapa = archivo.read()
    archivo.close()
    mapa = mapa.split("\n")
    for i in range(len(mapa)):
        mapa[i] = mapa[i].split(",")
    mapa = mapa[:-1]
    return mapa

mapa = cargamapa()

intersecciones = []
for i in range(len(mapa) -1):
    for j in range(len(mapa[i])-1):
        if(mapa[i][j] != "-1"):
            vecinosx = 0
            vecinosy = 0
            vecinos = []
            if(mapa[(i+1)%len(mapa)][j] != "-1"):
                vecinosy += 1
                vecinos.append([j,(i+1)%len(mapa)])
            if(mapa[(i-1+len(mapa))%len(mapa)][j] != "-1"):
                vecinosy += 1
                vecinos.append([j,(i-1+len(mapa))%len(mapa)])
            if(mapa[i][(j+1)%len(mapa[i])] != "-1"):
                vecinosx += 1
                vecinos.append([(j+1)%len(mapa[i]),i])
            if(mapa[i][(j-1+len(mapa[i]))%len(mapa[i])] != "-1"):
                vecinosx += 1
                vecinos.append([(j-1+len(mapa[i]))%len(mapa[i]),i])
            if(vecinosx > 0 and vecinosy > 0):
                intersecciones.append([[j,i],vecinos])
intersecciones.append([[14,23], [[13,23],[15,23]]])

intersecciones = np.array(intersecciones, dtype=object)

n = 0
for i in intersecciones:
    elementos = []
    for j in i[1]:
        encontrado = False
        nodo = []
        nodo.append(j[0])
        nodo.append(j[1])
        while(not encontrado):
            if(nodo in list(intersecciones[:,0])):
                elementos.append(nodo)
                encontrado = True
            else:
                nodo[1] += j[1]-i[0][1]
                nodo[0] += j[0]-i[0][0]
                if(nodo[0] > len(mapa[0])):
                    nodo[0] = 0
                if(nodo[1] > len(mapa)):
                    nodo[1] = 0
                if(nodo[0] < 0):
                    nodo[0] = len(mapa[0])-1
                if(nodo[1] < 0):
                    nodo[1] = len(mapa)-1
    intersecciones[n][1] = elementos
    n += 1   
intersecciones = intersecciones.tolist()
escala = 16
pacman = pac.PPacman(escala)
pinky = fan.Fantasma(escala, "Pinky", 1 , 1)
#pinky2 = fan.Fantasma(escala, "Pinky", 26 , 1)
window = pyglet.window.Window(len(mapa[0]) * escala, len(mapa) * escala, resizable=False)
batch = pyglet.graphics.Batch()

def Pintamapa():
    lista = []
    rectangle = shapes.Rectangle(0, 0, len(mapa[0]) * escala, len(mapa) * escala, color=(0, 0, 0), batch=batch)
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            if("-1" in str(mapa[len(mapa)-y-1][x])):
                if not("-1" in mapa[len(mapa)-y-2][x]):
                    rectangle = shapes.Rectangle(x*escala+2, y*escala+escala-2, escala-2, 2, color=(36, 36, 255), batch=batch)
                    lista.append(rectangle)
                if not("-1" in mapa[(len(mapa)-y)%len(mapa)][x]):
                    rectangle = shapes.Rectangle(x*escala+2, y*escala, escala-2, 2, color=(36, 36, 255), batch=batch)
                    lista.append(rectangle)
                if not("-1" in mapa[len(mapa)-y-1][(x+1)%len(mapa[0])]):
                    rectangle = shapes.Rectangle(x*escala+escala-2, y*escala, 2, escala, color=(36, 36, 255), batch=batch)
                    lista.append(rectangle)
                if not("-1" in mapa[len(mapa)-y-1][(x-1+len(mapa[0]))%len(mapa[0])]):
                    rectangle = shapes.Rectangle(x*escala+2, y*escala, 2, escala, color=(36, 36, 255), batch=batch)
                    lista.append(rectangle)
                #canvas.create_rectangle(x*16, y*16, x*16+2, y*16+16, fill='blue', outline='blue')
                
                #rectangle = shapes.Rectangle(x*escala, y*escala, escala, escala, color=(36, 36, 255), batch=batch)
            if(str(mapa[len(mapa)-y-1][x]) == "1"):
                rectangle = shapes.Rectangle(x*escala+(escala/2)-1, y*escala+(escala/2)-1 , 2, 2, color=(255, 182, 182), batch=batch)
            lista.append(rectangle)
    return lista



@window.event
def on_draw():
    window.clear()
    listaa = Pintamapa()
    listaa.append(shapes.Circle(pacman.posicionx, (len(mapa))*escala - pacman.posiciony, 6, color = (255,255,31), batch = batch))
    listaa.append(shapes.Circle(pinky.posicionx, (len(mapa))*escala - pinky.posiciony, 6, color = pinky.color, batch = batch))
    #listaa.append(shapes.Circle(pinky2.posicionx, (len(mapa))*escala - pinky2.posiciony, 6, color = pinky2.color, batch = batch))
    #print(str(pacman.permitirgirod) + " " + str(pacman.permitirgiroi) + " " + str(pacman.direccion) + str(pacman.direccionan))
    batch.draw()
        
def remplaza(Mapa2):
    mapa = Mapa2

        
def update(dt):
    #pinky2.avanza(mapa, escala, pacman.posicion(), pacman.puntocritico, pacman.puntocriticosig, intersecciones)
    #pinky2.avanza(mapa, escala, pacman.posicion(), pacman.puntocritico, pacman.puntocriticosig, intersecciones)
    Entradas = []
    Entradas.append(pacman.posicionx)
    Entradas.append(pacman.posiciony)
    if(pacman.direccion == [-1,0]):
        Entradas.append(0)
    elif(pacman.direccion == [0,-1]):
        Entradas.append(1)
    elif(pacman.direccion == [1,0]):
        Entradas.append(2)
    elif(pacman.direccion == [0,1]):
        Entradas.append(3)
    Entradas.append(pacman.puntocriticosig[0])
    Entradas.append(pacman.puntocriticosig[1])
    contiguo = est.ConvierteMapa(pacman.posicionx/escala, pacman.posiciony/escala, len(mapa[0]), len(mapa), 1, 0)
    Entradas.append(mapa[int(contiguo[1])][int(contiguo[0])])
    contiguo = est.ConvierteMapa(pacman.posicionx/escala, pacman.posiciony/escala, len(mapa[0]), len(mapa), -1, 0)
    Entradas.append(mapa[int(contiguo[1])][int(contiguo[0])])
    contiguo = est.ConvierteMapa(pacman.posicionx/escala, pacman.posiciony/escala, len(mapa[0]), len(mapa), 0, 1)
    Entradas.append(mapa[int(contiguo[1])][int(contiguo[0])])
    contiguo = est.ConvierteMapa(pacman.posicionx/escala, pacman.posiciony/escala, len(mapa[0]), len(mapa), 0, -1)
    Entradas.append(mapa[int(contiguo[1])][int(contiguo[0])])
    Entradas.append(pinky.posicionx)
    Entradas.append(pinky.posiciony)
    Entradas.append(est.Distancia(pacman.posicion(), pinky.posicion()))
    #Entradas.append(pinky2.posicionx)
    #Entradas.append(pinky2.posiciony)
    #Entradas.append(est.Distancia(pacman.posicion(), pinky2.posicion()))
    salida = jugador.activate(Entradas)
    decision = salida.index(max(salida))
    pacman.gira(decision)
    if(est.Distancia(pacman.posicion(), pinky.posicion()) > 4 and pacman.comida < 245 and pinky.tiempo < 6000):
        remplaza(pacman.avanza(mapa, escala, intersecciones))
        remplaza(pacman.avanza(mapa, escala, intersecciones))
        remplaza(pacman.avanza(mapa, escala, intersecciones))
        pinky.avanza(mapa, escala, pacman.posicion(), pacman.puntocritico, pacman.puntocriticosig, intersecciones)
        pinky.avanza(mapa, escala, pacman.posicion(), pacman.puntocritico, pacman.puntocriticosig, intersecciones)
    
remplaza(pacman.avanza(mapa, escala, intersecciones))
pyglet.clock.schedule_interval(update,1/10)
pyglet.app.run()

