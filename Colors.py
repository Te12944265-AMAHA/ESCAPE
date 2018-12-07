'''
Created on 2018 M11 23

@author: Tina
'''
import pygame

class Color(object):
    blue = (107,101,217)
    red = (206,42,27)
    yellow = (255,239,0)
    green = (77,180,88)
    orange = (242,145,25)
    purple = (148,87,223)
    cyan = (62,130,196)
    pink = (241,156,189)
    black = (0,0,0)
    white = (255,255,255)
    gold = (254,212,0)
    silver = (160,160,160)
    gray = (115,115,115)
    
    @staticmethod
    def getAllColors():
        return [Color.blue,Color.red,Color.yellow,Color.green,Color.orange,
                Color.purple,Color.cyan,Color.pink,Color.black,Color.gold,Color.silver,Color.gray]