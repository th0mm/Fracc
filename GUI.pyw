import pygame, pygame.freetype
import tkinter as tk
import math, random, datetime, time
from decimal import *
import subprocess, os
#import a will to live

pygame.init()
pygame.font.init()
pygame.display.set_caption('Fracc')

meme = pygame.image.load("white.png")
pygame.display.set_icon(meme)

screenWidth, screenHeight = 300, 300
screen = pygame.display.set_mode((screenWidth, screenHeight))

cubic = pygame.font.SysFont('Times New Roman', int(screenHeight/16))
square = pygame.font.SysFont('georgia', int(screenHeight/16))
line = pygame.font.SysFont('georgia', int(screenHeight/20))
dot = pygame.font.SysFont('Lucida Console', int(screenHeight/30))

bgColour = (255, 255, 255)

colourPalette = [(100,100,100), (160, 160, 160), (200, 200, 200), (220, 220, 220), (64,224,208)]

titleColour = colourPalette[0]
textColour = colourPalette[1]
buttonColour = colourPalette[2]
selectColour = colourPalette[3]
logColour = colourPalette[4]

text = []
titles = []
settings = []
buttons = []

FASE = {
        'CHOOSE': 0,
        'SET': 1,
        'PLOT': 2,
    }

currentFase = 0

FRACTAL = {
        'Mandelbrot': 0,
        'Sierpinski': 1,
        'Julia Sets': 2,
        'IFS': 3
    }

currentFractal = -1

TYPE = {
        'INT': 0,
        'FLOAT': 1,
        'PARAMETERS': 3,
        'DONE': 4
    }


PRESETS = [
    [
        ["0,279", 0.279, 0],
        ["1 - φ", 1-1.618, 0],
        ["-0,4 + 0,6i", -0.4, 0.6],
        ["0,285 + 0,01i", 0.285, 0.01],
        ["-0,835 - 0,232i", -0.835, -0.232],
        ["-0,8i", 0, -0.8]
    ],
    [
	["IFS 1", [0, -0.5, 0.5, 0, 0.5, 0],[0, 0.5, -0.5, 0, 0.5, 0.5],[0.5, 0, 0, 0.5, 0.25, 0.5]],
	["IFS 2", [0, 0.577, -0.577, 0, 0.0951, 0.5893],[0, 0.577, -0.577, 0, 0.4413, 0.7893],[0, 0.577, -0.577, 0, 0.0952, 0.9893]],
	["IFS 3", [0.382, 0, 0, 0.382, 0.3072, 0.619],[0.382, 0, 0, 0.382, 0.6033, 0.4044],[0.382, 0, 0, 0.382, 0.0139, 0.4044], [0.382, 0, 0, 0.382, 0.1253, 0.0595], [0.382, 0, 0, 0.382, 0.492, 0.0595]],
	["IFS 4", [0.195, -0.488, 0.344, 0.443, 0.4431, 0.2452],[0.462, 0.414, -0.252, 0.361, 0.2511, 0.5692],[-0.058, -0.07, 0.453, -0.111, 0.5976, 0.0969],[-0.035, 0.07, -0.469, -0.022, 0.4884, 0.5069],[-0.637, 0, 0, 0.501, 0.8662, 0.2513]],
	["IFS 5", [0.849, 0.037, -0.037, 0.849, 0.075, 0.183],[0.197, -0.226, 0.226, 0.197, 0.4, 0.049],[-0.15, 0.283, 0.26, 0.237, 0.575, -0.084],[0, 0, 0, 0.16, 0.5, 0]]
    ]
]

AREA = [-2, 2, 2, -2]
SCALE = 0.4
mousePos = [0, 0, False] #[x, y, pressed?]

def resetColours():
    global bgColour, titleColour, textColour, buttonColour, selectColour, logColour
    bgColour = (255, 255, 255)
    titleColour = colourPalette[0]
    textColour = colourPalette[1]
    buttonColour = colourPalette[2]
    selectColour = colourPalette[3]
    logColour = colourPalette[4]

def setMenu(window):
    global text, titles, screen
    global screenWidth, screenHeight
    global font, textColour
    global settings
    text = []
    if window == '2D':
        titles = ['Fracc', 'Mandelbrot', 'Sierpinski', 'Julia Sets', 'IFS']
        settings = [
            [[TYPE['INT'], "Iterations:", 200, 1, 10]],
            [[TYPE['INT'], "Iterations:", 10000, 1, 1000], [TYPE['INT'], "N-polygon:", 3, 3, 1], [TYPE['FLOAT'], "Distance:", 0.5, 0, 1]],
            [[TYPE['INT'], "Iterations:", 200, 1, 10], [TYPE['PARAMETERS'], "C-value:", 0, 0]],
            [[TYPE['INT'], "Iterations:", 10000, 1, 1000], [TYPE['PARAMETERS'], "IFS:", 1, 0]]
        ]
        text.append([square.render(titles[0], True, titleColour), False])
    for title in titles[1: len(titles)]:
        text.append([square.render(title, True, textColour), False])

def drawMenu():
    global text
    for i in range(len(text)):
        pos = [screenWidth/2 - text[i][0].get_width()/2, screenHeight*(3+i*2)/15-text[i][0].get_height()]
        if i != 0 and text[i][0].get_rect().left + pos[0] < pygame.mouse.get_pos()[0] < text[i][0].get_rect().right + pos[0] and text[i][0].get_rect().top + pos[1] < pygame.mouse.get_pos()[1] < text[i][0].get_rect().bottom + pos[1]:
            text[i][0] = square.render(titles[i], True, selectColour)
        elif i !=0:
            text[i][0] = square.render(titles[i], True, textColour)
        else:
            text[i][0] = square.render(titles[i], True, titleColour)
        screen.blit(text[i][0], (pos[0], pos[1]))

def setSettings():
    global text, title
    text = []
    text.append([square.render(currentFractal, True, titleColour), False])
    for setting in settings[ FRACTAL[currentFractal] ]:
        text.append([square.render(setting[1], True, textColour), False])

L = 255
def drawSettings():
    global L, screen, text, setup
    global titleColour, textColour, selectColour
    setup = False
    if L > colourPalette[0][0]:
        titleColour = (L, L, L)
        if L > colourPalette[1][0]:
            textColour = (L, L, L)
            if L > colourPalette[2][0]:
                buttonColour = (L, L, L)
                if L > colourPalette[3][0]:
                    selectColour = (L, L, L)
        L-=1

    text[0][0] = square.render(currentFractal, True, titleColour)
    for i in range(1, len(text)):
        text[i][0] = square.render(settings[FRACTAL[currentFractal]][i-1][1], True, textColour)
    screen.blit(text[0][0], (screenWidth/2 - text[0][0].get_width()/2, screenHeight*(3)/15-text[0][0].get_height()))
    for i in range(1, len(text)):
        pos = (screenWidth/6, screenHeight*(3+i*2)/15-text[i][0].get_height())
        screen.blit(text[i][0], pos)

def setButtons():
    global buttons
    buttons = []
    for setting in settings[FRACTAL[currentFractal]]:
        if setting[0] == TYPE['INT']:
            surface1 = square.render('-', True, buttonColour)
            surface2 = square.render('+', True, buttonColour)
            buttons.append([TYPE['INT'], surface1, surface2])
        elif setting[0] == TYPE['FLOAT']:
            surface1 = square.render('set', True, buttonColour)
            buttons.append([TYPE['FLOAT'], surface1])
        elif setting[0] == TYPE['PARAMETERS']:
            surface1 = square.render('<', True, buttonColour)
            surface2 = square.render('>', True, buttonColour)
            buttons.append([TYPE['PARAMETERS'], surface1, surface2])
    surface = cubic.render("- OK, I'm done! -", True, buttonColour)
    buttons.append([TYPE['DONE'], surface])

def drawButtons():
    global buttons, screen
    for i in range(len(buttons)):
        if buttons[i][0] == TYPE['INT']:
            for m in range(1, len( buttons[i][1:len(buttons[i])] )+1):
                screen.blit(buttons[i][m], (screenWidth*6/12 + (m-1)*4*screenWidth/12 - buttons[i][m].get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][m].get_height()) )
            numbah = square.render(str(settings[FRACTAL[currentFractal]][i][2]), True, textColour)
            screen.blit(numbah, (screenWidth*8/12 - numbah.get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][1].get_height()) )
        elif buttons[i][0] == TYPE['FLOAT']:
            screen.blit(buttons[i][1], (screenWidth*6/12 - buttons[i][1].get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][1].get_height()) )
            REQUIEM = open("TEXT\\requiem.txt", "r")
            try:
                settings[FRACTAL[currentFractal]][i][2] = float(REQUIEM.read().split()[0])
            except (ValueError, IndexError):
                pass
            REQUIEM.close()
            numbah = square.render(str(settings[FRACTAL[currentFractal]][i][2]), True, textColour)
            screen.blit(numbah, (screenWidth*8/12 - numbah.get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][1].get_height()) )
        elif buttons[i][0] == TYPE['PARAMETERS']:
            for m in range(1, len( buttons[i][1:len(buttons[i])] )+1):
                screen.blit(buttons[i][m], (screenWidth*6/12 + (m-1)*4*screenWidth/12 - buttons[i][m].get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][m].get_height()) )
            numbah = line.render(PRESETS[ settings[FRACTAL[currentFractal]][i][2] ][ settings[FRACTAL[currentFractal]][i][3] ][0], True, textColour)
            screen.blit(numbah, (screenWidth*8/12 - numbah.get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][1].get_height()*0.8) )
        elif buttons[i][0] == TYPE['DONE']:
            screen.blit(buttons[i][1], (screenWidth/2 - buttons[i][1].get_width()/2, screenHeight*10/12))

fadeOut = -1
def hitbox(x, y):
    global text, screen
    global buttons
    global R9K, INPUT
    global currentFase
    global fadeOut
    if currentFase == FASE['CHOOSE']:
        for i in range(len(text)):
            pos = [screenWidth/2 - text[i][0].get_width()/2, screenHeight*(3+i*2)/15-text[i][0].get_height()]
            if text[i][0].get_rect().left + pos[0] < x < text[i][0].get_rect().right + pos[0] and text[i][0].get_rect().top + pos[1] < y < text[i][0].get_rect().bottom + pos[1]:
                text[i][1] = True
    if currentFase == FASE['SET']:
       for i in range(len(buttons)):
            if buttons[i][0] == TYPE['INT']:
                for m in range(1,3):
                    pos = [screenWidth*6/12 + (m-1)*4*screenWidth/12 - buttons[i][m].get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][m].get_height()]
                    if buttons[i][m].get_rect().left + pos[0] < x < buttons[i][m].get_rect().right + pos[0] and buttons[i][m].get_rect().top + pos[1] < y < buttons[i][m].get_rect().bottom + pos[1]:
                        if m == 1:
                            aniki = settings[FRACTAL[currentFractal]][i][2] - settings[FRACTAL[currentFractal]][i][4]
                            if(aniki >= settings[FRACTAL[currentFractal]][i][3]):
                                settings[FRACTAL[currentFractal]][i][2] = aniki #wauw een chiasme 
                        elif m == 2:
                            settings[FRACTAL[currentFractal]][i][2] += settings[FRACTAL[currentFractal]][i][4]
                numbah = square.render(str(settings[FRACTAL[currentFractal]][i][2]), True, textColour)
                pos = [screenWidth*8/12 - numbah.get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][1].get_height()]
                if numbah.get_rect().left + pos[0] < x < numbah.get_rect().right + pos[0] and numbah.get_rect().top + pos[1] < y < numbah.get_rect().bottom + pos[1]:
                    pass
            elif buttons[i][0] == TYPE['FLOAT']:
                pos = (screenWidth*6/12 - buttons[i][1].get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][1].get_height())
                if buttons[i][1].get_rect().left + pos[0] < x < buttons[i][1].get_rect().right + pos[0] and buttons[i][1].get_rect().top + pos[1] < y < buttons[i][1].get_rect().bottom + pos[1]:
                    subprocess.Popen("WINTERWOEDE.pyw 1", shell=True)
            elif buttons[i][0] == TYPE['PARAMETERS']:
                for m in range(1,3):
                    pos = [screenWidth*6/12 + (m-1)*4*screenWidth/12 - buttons[i][m].get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][m].get_height()]
                    if buttons[i][m].get_rect().left + pos[0] < x < buttons[i][m].get_rect().right + pos[0] and buttons[i][m].get_rect().top + pos[1] < y < buttons[i][m].get_rect().bottom + pos[1]:
                        if m == 1:
                            settings[FRACTAL[currentFractal]][i][3] -= 1
                        elif m == 2:
                            settings[FRACTAL[currentFractal]][i][3] += 1
                        if settings[FRACTAL[currentFractal]][i][3] == len(PRESETS[1]):
                            settings[FRACTAL[currentFractal]][i][3] = 0
                        elif settings[FRACTAL[currentFractal]][i][3] == -1:
                            settings[FRACTAL[currentFractal]][i][3] = len(PRESETS[1])-1 #waarom heeft python geen wraparound voor lists
                numbah = line.render(PRESETS[ settings[FRACTAL[currentFractal]][i][2] ][ settings[FRACTAL[currentFractal]][i][3] ][0], True, textColour)
                pos = [screenWidth*8/12 - numbah.get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][1].get_height()*0.8]
                if numbah.get_rect().left + pos[0] < x < numbah.get_rect().right + pos[0] and numbah.get_rect().top + pos[1] < y < numbah.get_rect().bottom + pos[1]:
                    pass
            elif buttons[i][0] == TYPE['DONE']:
                pos = [screenWidth/2 - buttons[i][1].get_width()/2, screenHeight*10/12]
                if buttons[i][1].get_rect().left + pos[0] < x < buttons[i][1].get_rect().right + pos[0] and buttons[i][1].get_rect().top + pos[1] < y < buttons[i][1].get_rect().bottom + pos[1]:
                    updateFiles()
                    fadeOut = 0

SkiBaBopBaDopBop = pygame.Surface((screenWidth, screenHeight))
SkiBaBopBaDopBop.fill((0, 0, 0))
j = 0
def checkbox(x, y):
    global j, textColour, titleColour, selectColour, bgColour
    global currentFase, currentFractal
    global R9K
    global buttons
    global fadeOut
    if currentFase == FASE['CHOOSE']:
        for i in range(1, len(text)):
            if text[i][1]:
                if j <= 155:
                    titleColour = (colourPalette[0][0]+j,colourPalette[0][1]+j,colourPalette[0][2]+j)
                    if j <= 95:
                        textColour = selectColour = (colourPalette[1][0]+j,colourPalette[1][1]+j,colourPalette[1][2]+j)
                    j+=8
                else:
                    currentFase = FASE['SET']
                    currentFractal = titles[i]
    elif currentFase == FASE['SET']:
        if not fadeOut >= 0:
            for i in range(len(buttons)):
                if buttons[i][0] == TYPE['INT']:
                    for m in range(1,3):
                        pos = [screenWidth*6/12 + (m-1)*4*screenWidth/12 - buttons[i][m].get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][m].get_height()]
                        if buttons[i][m].get_rect().left + pos[0] < x < buttons[i][m].get_rect().right + pos[0] and buttons[i][m].get_rect().top + pos[1] < y < buttons[i][m].get_rect().bottom + pos[1]:
                            if m == 1:
                                buttons[i][m] = square.render('-', True, selectColour)
                            elif m == 2:
                                buttons[i][m] = square.render('+', True, selectColour)
                        else:
                            if m == 1:
                                buttons[i][m] = square.render('-', True, buttonColour)
                            elif m == 2:
                                buttons[i][m] = square.render('+', True, buttonColour)
                elif buttons[i][0] == TYPE['FLOAT']:
                    pos = (screenWidth*6/12 - buttons[i][1].get_width()/2, screenHeight*(3+(i+1)*2)/15-buttons[i][1].get_height())
                    if buttons[i][1].get_rect().left + pos[0] < x < buttons[i][1].get_rect().right + pos[0] and buttons[i][1].get_rect().top + pos[1] < y < buttons[i][1].get_rect().bottom + pos[1]:
                        buttons[i][1] = square.render('set', True, selectColour)
                    else:
                        buttons[i][1] = square.render('set', True, buttonColour)
                elif(buttons[i][0] == TYPE['DONE']):
                    pos = [screenWidth/2 - buttons[i][1].get_width()/2, screenHeight*10/12]
                    if buttons[i][1].get_rect().left + pos[0] < x < buttons[i][1].get_rect().right + pos[0] and buttons[i][1].get_rect().top + pos[1] < y < buttons[i][1].get_rect().bottom + pos[1]:
                        buttons[i][1] = cubic.render("- OK, I'm done! -", True, selectColour)
                    else:
                        buttons[i][1] = cubic.render("- OK, I'm done! -", True, buttonColour)
        else:
            SkiBaBopBaDopBop.set_alpha(int(255*fadeOut))
            screen.blit(SkiBaBopBaDopBop, (0,0))
            fadeOut += 0.01
            if fadeOut >= 1:
                subprocess.Popen([r"engine.exe"])
                bgColour = (0, 0, 0)
                currentFase = FASE['PLOT']

def updateFiles():
    R9K = open("TEXT\R9K.txt", "w")
    reimu = [FRACTAL[currentFractal], AREA[0], AREA[1], AREA[2], AREA[3], screenWidth, screenHeight] #[fractal, range[4], screen[2]]
    for bird in reimu:
        R9K.write(str(bird) + " ")
    R9K.close()
    INPUT = open("TEXT\input.txt", "w")
    marisa = settings[FRACTAL[currentFractal]]
    for setting in marisa:
        if setting[0] == TYPE['INT'] or setting[0] == TYPE['FLOAT']:
            INPUT.write(str(setting[2]) + " ") #[all settings met spaties]
        else:
            if setting[2] == 0:
                INPUT.write(str(PRESETS[setting[2]][setting[3]][1]) + " " + str(PRESETS[setting[2]][setting[3]][2]) + " ")
            if setting[2] == 1:
                INPUT.write(str(PRESETS[setting[2]][setting[3]][0][4]) + " ")
    INPUT.close()

epsilon = 0.000003
useFloat = True
data = []
def readFile():    
    global PLOT, raw, data, useFloat
    PLOT = open("TEXT/plot.txt", "r")
    PLOT.seek(0)
    data = PLOT.read().split()
    if (AREA[2]-AREA[0])/screenWidth < epsilon or (AREA[1]-AREA[3])/screenHeight < epsilon:
        data = [Decimal(i) for i in data]
        useFloat = False
    else:
        data = [float(i) for i in data]
        useFloat = True
    PLOT.close()

def plot(surface):
    global screen, PLOT, screen
    CHECK = open("TEXT/check.txt", "r")
    CHECK.seek(0)
    try:
        c = int(CHECK.read())
    except ValueError:
        c = 0
    if(c and not mousePos[2]):
        updateFiles()
        CHECK = open("TEXT/check.txt", "w")
        CHECK.truncate()
        CHECK.write('0')
        readFile()
        subprocess.Popen([r"engine.exe"])
        CHECK.close()
    for i in range(0, int(len(data)/3)):
        x = y = 0
        if useFloat:
            if surface[0] < data[i*3] < surface[2] and surface[3] < data[i*3+1] < surface[1]:
                x = int((data[i*3]-surface[0])/(surface[2]-surface[0])*screenWidth)
                y = int((data[i*3+1]-surface[3])/(surface[1]-surface[3])*screenHeight)
        else:
            if Decimal(surface[0]) < data[i*3] < Decimal(surface[2]) and Decimal(surface[3]) < data[i*3+1] < Decimal(surface[1]):
                x = int((data[i*3]-Decimal(surface[0]))/Decimal(surface[2]-surface[0])*screenWidth)
                y = int((data[i*3+1]-Decimal(surface[3]))/Decimal(surface[1]-surface[3])*screenHeight)
        if currentFractal == 'Mandelbrot' or currentFractal == 'Julia Sets':
            colour = int(float(data[i*3+2]*255/settings[FRACTAL[currentFractal]][0][2]))
        else:
            colour = 255
        try:
            screen.set_at((x, y), (colour, colour, colour))
        except TypeError:
            screen.set_at((x, y), (255, 255, 255))

def resetToMenu():
    global bgColour, currentFractal, setMenu, setup, SkiBaBopBaDopBop, fadeOut, L, AREA, currentFase #A͋̓ͯÅ̋À͕͙̻̣̬̪̺͈̗̘̘̘̰̩̖̘̟̣͡͞͠A͊͑͗ͯ̂̏AÄ́Ą̛̖̖̺̟̣͎̦̘̖̪͙̣̰̏ͣA̓̅̈́̔ͮͥ̐ͧA͇͚̬͉͖͈̿̐͟
    global titleColour, textColour, buttonColour, selectColour, log #A̐̒̋ͮA̓ͯÅ̀͡A͕͙̻̣̬̪̺͈̗̘̘̘̰̩̖̘̟̣͠A͊̏Ä́Ą̛̖̖̺̟̣͎̦̘̖̪͙̣̰̏ͣ̓̅A̓̅̈́̔AͮͥA̐ͧ̔̕A͇͚̬͉͖͈ͯ͟Å̀͡A͕͙̻̣̬̪̺͈̗̘̘̘̰̩̖̘̟̣͠A͊̏Ä́Ą̛̖̖̺̟̣͎̦̘̖̪͙̣̰̏ͣ̓̅A̓̅̈́̔Aͮͥ
    resetColours()
    currentFractal = -1
    setMenu('2D')
    setup = True
    SkiBaBopBaDopBop.set_alpha(255)
    fadeOut = -1
    L = 255
    log = []
    AREA = [-2, 2, 2, -2]
    currentFase = FASE['CHOOSE']

log = []
updateLog = 0
def writeToLog(miku):
    global log, updateLog
    log.append(str(miku))
    updateLog = 255

def drawLog():
    global screen, updateLog, log
    if updateLog > 0:
        updateLog -= 15
    else:
        log = []
    for i in range(len(log)):
        output = dot.render(log[i], False, logColour)
        #output = pygame.Surface((output.get_width(), output.get_height()), SRCALPHA, output)
        output.set_alpha(updateLog)
        screen.blit(output, (screenWidth/12, screenHeight*11/12 - output.get_height()*(len(log)-i-1)))

setup = True
setMenu('2D')
quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                resetToMenu()
            elif event.key == pygame.K_s:
                path = "SS\\bazinga" + str(time.strftime("%d%m%y%H%M%S")) + ".bmp"
                pygame.image.save(screen, path)
            if currentFase == FASE['PLOT']:
                if event.key == pygame.K_UP:
                    oniichan = settings[FRACTAL[currentFractal]][0][2] + settings[FRACTAL[currentFractal]][0][4]
                    if(oniichan >= settings[FRACTAL[currentFractal]][0][3]):
                        settings[FRACTAL[currentFractal]][0][2] = oniichan
                        writeToLog("Iterations: " + str(oniichan))
                elif event.key == pygame.K_DOWN:
                    oniichan = settings[FRACTAL[currentFractal]][0][2] - settings[FRACTAL[currentFractal]][0][4]
                    if(oniichan >= settings[FRACTAL[currentFractal]][0][3]):
                        settings[FRACTAL[currentFractal]][0][2] = oniichan
                        writeToLog("Iterations: " + str(oniichan))
                elif event.key == pygame.K_RIGHT:
                    if currentFractal == 'Sierpinski':
                        settings[FRACTAL[currentFractal]][1][2] += 1
                        writeToLog("N-polygon: " + str(settings[FRACTAL[currentFractal]][1][2]))
                    elif currentFractal == 'Julia Sets':
                        if settings[FRACTAL[currentFractal]][1][3] + 1 > 5:
                            settings[FRACTAL[currentFractal]][1][3] = 0
                        else:
                            settings[FRACTAL[currentFractal]][1][3] +=1
                        writeToLog(PRESETS[0][settings[FRACTAL[currentFractal]][1][3]][0])
                    elif currentFractal == 'IFS':
                        if settings[FRACTAL[currentFractal]][1][3] + 1 > 4:
                            settings[FRACTAL[currentFractal]][1][3] = 0
                        else:
                            settings[FRACTAL[currentFractal]][1][3] +=1
                        writeToLog(PRESETS[1][settings[FRACTAL[currentFractal]][1][3]][0])
                elif event.key == pygame.K_LEFT:
                    if currentFractal == 'Sierpinski':
                        imoutochan = settings[FRACTAL[currentFractal]][1][2] - 1
                        if(imoutochan >= 3):
                            settings[FRACTAL[currentFractal]][1][2] = imoutochan
                            writeToLog("N-polygon: " + str(settings[FRACTAL[currentFractal]][1][2]))
                    elif currentFractal == 'Julia Sets':
                        if settings[FRACTAL[currentFractal]][1][3] - 1 < 0:
                            settings[FRACTAL[currentFractal]][1][3] = 5
                        else:
                            settings[FRACTAL[currentFractal]][1][3] -=1
                        writeToLog(PRESETS[0][settings[FRACTAL[currentFractal]][1][3]][0])
                    elif currentFractal == 'IFS':
                        if settings[FRACTAL[currentFractal]][1][3] - 1 < 0:
                            settings[FRACTAL[currentFractal]][1][3] = 4
                        else:
                            settings[FRACTAL[currentFractal]][1][3] -= 1
                        writeToLog(PRESETS[1][settings[FRACTAL[currentFractal]][1][3]][0])
                    
        if currentFase == FASE['CHOOSE'] or currentFase == FASE['SET']:
            if event.type == pygame.MOUSEBUTTONUP:  
                hitbox(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(event.button == 1): #left click
                    mousePos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], True]
                    old = AREA[:]
                elif(event.button == 4): #scroll up
                    offset = [(((AREA[0]+AREA[2])/2)-AREA[0])*SCALE, (((AREA[1]+AREA[3])/2)-AREA[1])*SCALE]
                    AREA[0] += offset[0]
                    AREA[2] -= offset[0]
                    AREA[1] += offset[1]
                    AREA[3] -= offset[1]
                    #print([(AREA[2]-AREA[0])/screenWidth, (AREA[1]-AREA[3])/screenHeight])
                elif(event.button == 5): #scroll down
                    offset = [(((AREA[0]+AREA[2])/2)-AREA[0])*SCALE, (((AREA[1]+AREA[3])/2)-AREA[1])*SCALE]
                    AREA[0] -= offset[0]
                    AREA[2] += offset[0]
                    AREA[1] -= offset[1]
                    AREA[3] += offset[1]
                elif(event.button == 3): #right click
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if(event.button == 1): #left click
                    mousePos[2] = False
                    pygame.event.set_grab(False)
    
    screen.fill(bgColour)
    if currentFase == FASE['CHOOSE']:
        drawMenu()
        checkbox(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    elif currentFase == FASE['SET']:
        if setup:
            setSettings()
            setButtons()
        drawSettings()
        drawButtons()
        checkbox(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    elif currentFase == FASE['PLOT']:
        if(mousePos[2]):
            AREA[0] = old[0] + (mousePos[0] - pygame.mouse.get_pos()[0])*(old[2]-old[0])/screenWidth
            AREA[2] = old[2] + (mousePos[0] - pygame.mouse.get_pos()[0])*(old[2]-old[0])/screenWidth
            AREA[1] = old[1] + (mousePos[1] - pygame.mouse.get_pos()[1])*(old[1]-old[3])/screenHeight
            AREA[3] = old[3] + (mousePos[1] - pygame.mouse.get_pos()[1])*(old[1]-old[3])/screenHeight
        plot(AREA)
        drawLog()
    pygame.time.Clock().tick(400)
    pygame.display.flip()
pygame.quit()

"""
Python klaagmuur (deels humoristisch, deels serieuze ergernissen):
    -python is gewoon echt heel erg dom en sloom
    -whitespace is deel van de syntax
    -whitespace is deel van de syntax
    -whitespace is deel van de syntax
    -geen index wrap-around voor lists
    -soms werkt int(x) niet, maar int(float(x)) wel, casting is B R O K E N
    -mist een paar datatypes voor getallen (geen long double bijv)
        -Decimal zou long double perfect kunnen vervangen ALS HET NIET ZO SLOOM
        WAS REEEEEEEEEEEEEEEEEEEEEE
    -kopieën van lists zijn zonder de [:] geen echte kopieën, maar references
    -oh ja, whitespace is deel van de syntax
    -Dynamic Typing geeft in ruil voor de 0.0000001 seconden dat het duurt om
    een datatype in te tikken realistisch gezien meer ruimte voor bugs en is
    daarom een concept dat in theorie goed lijkt te werken, maar faalt in
    de executie. Net als het communisme ☭
    -waarom zou ik voor het wijzigen van een waarde van een GLOBAL variabele in
    een functie eerst naar de GLOBAL variabele in kwestie met een global
    keyword moeten refereren, als de variabele al in de GLOBAL scope is
    gedeclareerd
    -error meldingen laten niet eens zien bij welke character het mis was
    gegaan
    -'tHe zEN oF pYThOn' is net zo pretentieus als mijn KUA lessen over
    abstracte kunst
    -de syntax doet me denken aan pseudocode
    -whitespace is deel van de syntax
    -Koningscobra's zijn veel cooler dan pythons
    -GEEN POINTERS AAAAAAAA
    -Python is een interpreted taal, wat betekent dat je programma op veel
    computers niet zomaar zal kunnen runnen, omdat ze allemaal python
    en de nodige libraries geinstalleerd moeten hebben
    -Had ik al gezegd dat whitespace een deel van de syntax vormt?
    -ik begrijp python niet
    +Monty Python reference (noteer het plusje)
"""
