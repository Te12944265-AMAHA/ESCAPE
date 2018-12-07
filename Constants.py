'''
Created on 2018 M11 28

@author: Tina
'''
import pygame
from Colors import *
pygame.font.init()
K_TO_DISPLAY = 1.6
totalScore = 0

myfont = pygame.font.Font('font/munro.ttf', 50)

def drawScore(surface):
    text = myfont.render("Your current score: %d"%totalScore, False, Color.black)
    surface.blit(text, (surface.get_rect().width/2-text.get_rect().width/2,surface.get_rect().height/2-text.get_rect().height/2))
    

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

