# -*- coding: utf-8 -*-

import spyral
import pygame

import sys
import os
import random

SIZE = (1000, 750)
BG_COLOR = (255, 255, 255)
FG_COLOR = (0, 0, 0)
GREY = (125, 125, 125)

def cargar_frases():
    archivo = open("frases.txt", "r")
    frases = []
    for linea in archivo:
        if linea.find(",") > 0:
            # desciframos
            linea = str(linea)
            frases.append(linea)
    archivo.close()
    return frases

def nueva_frase():
    # una frase al azar
    linea = frases[random.randint(0, len(frases)-1)]
    ubi_coma = linea.find(",")
    infodato = linea[ubi_coma+1:-1]
    frase = linea[:ubi_coma]

    return frase, infodato

def wrap(text, length):
    words = text.split()
    lines = []
    line = ''
    for w in words:
        if len(w) + len(line) > length:
            lines.append(line)
            line = ''
        line = line + w + ' '
        if w is words[-1]: lines.append(line)
    return '\n'.join(lines)

class Colgadito(spyral.Sprite):
    def __init__(self, scene):
        super(Colgadito, self).__init__(scene)

        self.anchor = 'bottomright'
        self.y = SIZE[1]
        self.x = SIZE[0]

        self.update(6)

    def update(self, intentos):
        if intentos>=6:
            self.image = spyral.Image(filename="images/Hangman-0.png")
        elif intentos==5:
            self.image = spyral.Image(filename="images/Hangman-1.png")
        elif intentos==4:
            self.image = spyral.Image(filename="images/Hangman-2.png")
        elif intentos==3:
            self.image = spyral.Image(filename="images/Hangman-3.png")
        elif intentos==2:
            self.image = spyral.Image(filename="images/Hangman-4.png")
        elif intentos==1:
            self.image = spyral.Image(filename="images/Hangman-5.png")
        elif intentos==0:
            self.image = spyral.Image(filename="images/Hangman-6.png")
        self.image.scale((512,512))


class Descartadas(spyral.Sprite):
    def __init__(self, scene):
        super(Descartadas, self).__init__(scene)

        font_path = "fonts/SFDigitalReadout-Medium.ttf"
        self.font = spyral.Font(font_path, 72, GREY)
        self.image = self.font.render(scene.erradas)
        self.text = ""

        self.anchor = 'midtop'

        self.x = SIZE[0]/2
        self.y = 300

    def update(self, scene):
        if self.text:
            self.set_text(self.text)
        else:
            self.image = self.font.render(scene.erradas)

    def set_text(self, text):
        self.image = self.font.render(text)
        self.text = text


class Tablero(spyral.Sprite):
    def __init__(self, scene):
        super(Tablero, self).__init__(scene)

        self.completo = False

        font_path = "fonts/SFDigitalReadout-Medium.ttf"
        self.font = spyral.Font(font_path, 50, FG_COLOR)
        self.image = self.font.render("")
        self.text = ""

        self.anchor = 'midtop'

        self.x = SIZE[0]/2
        self.y = 120

    def set_text(self, text):
        self.image = self.font.render(text)
        self.text = text

    def mostrar(self, frase, acertadas):
        total = 0
        estado = ""
        for letra in frase:
            if letra in acertadas:
                estado = estado + " " + letra
                total = total + 1
            else:
                estado = estado + " _"

        if total==len(frase):
            self.completo = True

        self.set_text(estado)

class MultilineText(spyral.Sprite):
    def __init__(self, scene, text, x, y, w, h):
        super(MultilineText, self).__init__(scene)
        self.image = spyral.Image(size=(w,h))

        font_path = "fonts/LiberationSans-Regular.ttf"
        self.font = spyral.Font(font_path, 24, FG_COLOR)
        self.line_height = self.font.linesize

        self.anchor = 'center'
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.image = self.render_text(text)
        self.text = text


    def render_text(self, text):
        text_width = self.font.get_size(text)[0]

        ancho_promedio = self.font.get_size("X")[0]
        caracteres = self.w / ancho_promedio
        lineas = wrap(text, caracteres).splitlines()

        ln = 0
        for linea in lineas:
            self.image.draw_image(image=self.font.render(linea),
                                position=(0, ln * self.line_height),
                                anchor="midtop")
            ln = ln + 1
        return self.image
        

class Finale(spyral.Scene):
    def __init__(self, frase, infodato, ganaste):
        spyral.Scene.__init__(self, SIZE)

        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)

        self.text = frase
        font_path = "fonts/SFDigitalReadout-Medium.ttf"
        font = spyral.Font(font_path, 72, FG_COLOR)

        self.finale = spyral.Sprite(self)
        self.finale.image = font.render(self.text)
        self.finale.anchor = 'midtop'
        self.finale.x = SIZE[0]/2
        self.finale.y = 75

        self.infodato_label = MultilineText(self, infodato, self.finale.x, 500, 1000, 500)

        if ganaste:
            animation = spyral.Animation('y', spyral.easing.Sine(50),
                                    shift=75, duration=3, loop=True)
        else:
            animation = spyral.Animation('x', spyral.easing.Sine(50),
                                    shift=self.finale.x, duration=3, loop=True)
        self.finale.animate(animation)

        spyral.event.register("input.keyboard.down.*", self.procesar_tecla)
        self.closing = False
        spyral.event.register("system.quit", spyral.director.quit)

    def procesar_tecla(self):
        if not self.closing:
            spyral.director.pop()
            self.closing = True


class Game(spyral.Scene):
    """
    Colgadito
    """
    def __init__(self, activity=None):
        global SIZE
        pantalla = pygame.display.get_surface()
        SIZE = pantalla.get_size()

        spyral.Scene.__init__(self, SIZE)

        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)
        self.erradas = ""

        self.hangman = Colgadito(self)
        self.tablero = Tablero(self)
        self.descartadas = Descartadas(self)
        self.setup()

        pygame.mixer.init()
        self.bonus = pygame.mixer.Sound('sounds/BonusCube_0.ogg')
        self.fallo = pygame.mixer.Sound('sounds/Hurt_0.ogg')
        self.exito = pygame.mixer.Sound('sounds/chipquest.wav')
        self.pierde = pygame.mixer.Sound('sounds/punch.wav')
        self.aplauso = pygame.mixer.Sound('sounds/applause.wav')

        pygame.mixer.music.load('sounds/snare.wav')
        pygame.mixer.music.play(-1)

        spyral.event.register("input.keyboard.down.*", self.procesar_tecla)
        spyral.event.register("system.quit", spyral.director.quit)

        if activity:
            activity.show_game(None)
            activity._pygamecanvas.grab_focus()
            activity.window.set_cursor(None)
            self.activity = activity

    def setup(self):
        self.frase, self.infodato = nueva_frase()
        self.intentos = 6
        self.erradas = ""
        self.acertadas = " "
        self.tablero.completo = False

        self.sinacentos = ''
        for letra in self.frase:
            if letra==u"á":
                letra = "a"
            if letra==u"é":
                letra = "e"
            if letra==u"í":
                letra = "i"
            if letra==u"ó":
                letra = "o"
            if letra==u"ú":
                letra = "u"
            if letra==u"ñ":
                letra = "n"
            self.sinacentos = self.sinacentos + letra

        self.hangman.update(self.intentos)
        self.tablero.mostrar(self.sinacentos, self.acertadas)
        self.descartadas.update(self)

    def procesar_tecla(self, key):

        if not 0<key<255:
            return

        respuesta = chr(key)

        if respuesta in self.sinacentos:
            self.acertadas = self.acertadas + respuesta
            self.bonus.play()
        else:
            if self.intentos==0:
                self.perdiste()
            else:
                self.erradas = self.erradas + respuesta
                self.intentos = self.intentos - 1
                self.fallo.play()

        self.hangman.update(self.intentos)
        self.tablero.mostrar(self.sinacentos, self.acertadas)
        self.descartadas.update(self)

        if self.tablero.completo:
            self.ganaste()

    def ganaste(self):
        self.exito.play()
        self.aplauso.play()
        self.final(1)

    def perdiste(self):
        self.pierde.play()
        self.final(0)

    def final(self, ganaste):
        spyral.director.push(Finale(self.sinacentos, self.infodato, ganaste))
        self.setup()


frases = cargar_frases()

if __name__ == "__main__":
    spyral.director.init(SIZE) # the director is the manager for your scenes
    spyral.director.run(scene=Game()) # This will run your game. It will not return.
