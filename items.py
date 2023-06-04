import pygame

import lib

class Item():
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

class Consumable(Item):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)

class Weapon(Item):
    def __init__(self, name: str, description: str, w_type: str, damage: int, durability: int):
        super().__init__(name, description)

        self.type = w_type
        self.damage = damage
        self.durability = durability