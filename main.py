from termcolor import *

class Item():
    def __init__(self, name: str, description: str):
        self.raw_name = name
        self.name = colored(name, "white", attrs=["bold"])
        self.description = description    

class Consumable(Item):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.name = colored(name, "blue", attrs=["bold"])

class Weapon(Item):
    def __init__(self, name: str, description: str, w_type: str, damage: int, durability: int):
        super().__init__(name, description)
        self.name = colored(name, "red", attrs=["bold"])

        self.type = w_type
        self.damage = damage
        self.durability = durability

class Player():
    def __init__(self):
        self.inventory = []

    def add_to_inventory(self, item: Item):
        self.inventory.append(item)

    def list_inventory(self):
        for item in self.inventory:
            print("    " + item.name)

    def describe_item(self, name: str):
        for item in self.inventory:
            if item.raw_name == name:
                print(f"    {item.name}, {item.description}")

class Game():
    def __init__(self):

        self.running = True
        self.prompt = colored(" -> ", "green", attrs=["bold"])

        self.player = Player()

        self.items = {
            "sock": Item("Sock", "a test item")
        }

        self.consumables = {
            "milk": Consumable("Milk", "a test consumable")
        }

        self.weapons = {
            "knife": Weapon("Knife", "a test weapon", "melee", 1, 45)
        }

        self.commands = {
            "exit": ["ends the program", self.exit],
            "help": ["displays this help prompt", self.help],
            "inv": ["lists the items in the players inventory", self.player.list_inventory],
            "des": ["describes the item entered", self.player.describe_item]
        }

        self.player.add_to_inventory(self.items["sock"])
        self.player.add_to_inventory(self.consumables["milk"])
        self.player.add_to_inventory(self.weapons["knife"])

    def start(self):
        while self.running:
            inp = str(input(self.prompt))
            com = inp.split()
            
            if len(com) > 1:
                if com[0] in self.commands:
                    self.commands[com[0]][1](com[1])
                else:
                    cprint("  ! invalid command \n", "red", attrs=["bold"])
            else:
                if com[0] in self.commands:
                    self.commands[com[0]][1]()
                else:
                    cprint("  ! invalid command \n", "red", attrs=["bold"])

    def exit(self):
        self.running = False

    def help(self):
        print("    Command | Description")
        print("    ---------------------")
        for command in self.commands:
            print(f"    {command} | {self.commands[command][0]}")

    def copy_input_test(self, second_input: str):
        print(second_input)

if __name__ == "__main__":
    game = Game()
    game.start()