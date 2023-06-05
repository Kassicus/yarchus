import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pygame.font.init()

class Fonts():
    def __init__(self):
        self.regular = pygame.font.SysFont("Courier", 16)
        self.bold = pygame.font.SysFont("Courier", 16, bold = True)
        self.italic = pygame.font.SysFont("Courier", 16, italic = True)
        self.bold_italic = pygame.font.SysFont("Courier", 16, bold = True, italic = True)

class Colors():
    def __init__(self):
        self.black = pygame.Color(0, 0, 0)
        self.text = pygame.Color(255, 255, 255)
        self.command = pygame.Color(0, 255, 0)
        self.item = pygame.Color(255, 255, 255)
        self.weapon = pygame.Color(255, 0, 0)
        self.consumable = pygame.Color(0, 255, 255)
        self.debug = pygame.Color(255, 255, 0)
        self.field = pygame.Color(60, 60, 60)
    
item_keywords = [
    "item"
]
    
consumable_keywords = [
    "consumable"
]
    
weapon_keywords = [
    "weapon"
]

font = Fonts()
color = Colors()

events = None
delta_time = 0
framerate = 120