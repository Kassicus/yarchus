import pygame

pygame.init()

"""
###################################################################################################

CONSTANTS

###################################################################################################
"""

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

C_BLACK = pygame.Color(0, 0, 0)
C_TEXT = pygame.Color(255, 255, 255)
C_COMMAND = pygame.Color(210, 179, 255)
C_ITEM = pygame.Color(228, 255, 179)
C_WEAPON = pygame.Color(255, 179, 179)
C_CONSUMABLE = pygame.Color(179, 232, 255)
C_DEBUG = pygame.Color(255, 240, 179)
C_FIELD = pygame.Color(60, 60, 60)

F_REGULAR = pygame.font.Font("assets/fonts/Regular.ttf", 14)
F_BOLD = pygame.font.Font("assets/fonts/Bold.ttf", 14)
F_ITALIC = pygame.font.Font("assets/fonts/Italic.ttf", 14)
F_BOLD_ITALIC = pygame.font.Font("assets/fonts/BoldItalic.ttf", 14)

"""
###################################################################################################

KEYWORD LISTS

###################################################################################################
"""

item_keywords = []

consumable_keywords = []

weapon_keywords = []
    
dev_keywords = [
    "DEBUG:",
    "INVALID:"
]
    
"""
###################################################################################################

TERMINAL CLASSES

###################################################################################################
"""

class FeedbackLine():
    def __init__(self, text: str):
        self.text = text
        self.words = self.text.split()

        self.line = []
        self.parse_words()

    def parse_words(self):
        for word in self.words:
            if word in item_keywords:
                p_word = F_BOLD.render(word, True, C_ITEM)
            elif word in consumable_keywords:
                p_word = F_BOLD.render(word, True, C_CONSUMABLE)
            elif word in weapon_keywords:
                p_word = F_BOLD.render(word, True, C_WEAPON)
            elif word in dev_keywords:
                p_word = F_BOLD.render(word, True, C_DEBUG)
            else:
                p_word = F_REGULAR.render(word, True, C_TEXT)

            self.line.append(p_word)

class FeedbackPrompt():
    def __init__(self, x: int, y: int, width: int, height: int):
        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)

        self.feedback_lines = []

    def reset_prompt(self):
        self.feedback_lines = []

    def draw_feedback(self):
        self.manage_feedback_lines()

        horizontal_offset = 10 + self.pos.x
        vertical_offset = 10 + self.pos.y
        
        pygame.draw.rect(game.screen, C_FIELD, (self.pos.x, self.pos.y, self.size.x, self.size.y))

        for line in self.feedback_lines:
            horizontal_offset = 10 + self.pos.x

            for word in line.line:
                game.screen.blit(word, (horizontal_offset, vertical_offset))
                horizontal_offset += word.get_width() + 8

            vertical_offset += 30

    def manage_feedback_lines(self):
        if len(self.feedback_lines) > 20:
            self.feedback_lines.pop(0)

class CommandPrompt():
    def __init__(self, x: int, y: int, width: int, height: int):
        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)

        self.active = False

        self.text = ""
        self.commands = self.text.split()
        self.rendered_commands = []

    def check_active(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.pos.x < mouse_x < self.pos.x + self.size.x:
            if self.pos.y < mouse_y < self.pos.y + self.size.y:
                if pygame.mouse.get_pressed()[0]:
                    self.active = True
            else:
                if pygame.mouse.get_pressed()[0]:
                    self.active = False
        else:
            if pygame.mouse.get_pressed()[0]:
                self.active = False

    def process_command(self):
        if len(self.commands) > 1:
            if self.commands[0] in game.commands_list:
                try:
                    game.commands_list[self.commands[0]][2](self.commands[1])
                except:
                    line = FeedbackLine("INVALID: argument")
                    game.feedback_prompt.feedback_lines.append(line)
            else:
                line = FeedbackLine("INVALID: command")
                game.feedback_prompt.feedback_lines.append(line)

                blank_line = FeedbackLine(" ")
                game.feedback_prompt.feedback_lines.append(blank_line)
        else:
            if self.commands[0] in game.commands_list:
                game.commands_list[self.commands[0]][2]()
            else:
                line = FeedbackLine("INVALID: command")
                game.feedback_prompt.feedback_lines.append(line)

                blank_line = FeedbackLine(" ")
                game.feedback_prompt.feedback_lines.append(blank_line)

        self.text = ""

    def render_commands(self):
        self.rendered_commands = []

        for command in self.commands:
            if command in game.commands_list:
                rendered_command = F_BOLD_ITALIC.render(command, True, C_COMMAND)
            elif command in item_keywords:
                rendered_command = F_BOLD.render(command, True, C_ITEM)
            elif command in consumable_keywords:
                rendered_command = F_BOLD.render(command, True, C_CONSUMABLE)
            elif command in weapon_keywords:
                rendered_command = F_BOLD.render(command, True, C_WEAPON)
            else:
                rendered_command = F_REGULAR.render(command, True, C_TEXT)

            self.rendered_commands.append(rendered_command)

    def draw_commands(self):
        offset = 10 + self.pos.x

        pygame.draw.rect(game.screen, C_FIELD, (self.pos.x, self.pos.y, self.size.x, self.size.y))

        if self.active:
            pygame.draw.rect(game.screen, C_TEXT, (self.pos.x, self.pos.y, self.size.x, self.size.y), 1)

        for command in self.rendered_commands:
            game.screen.blit(command, (offset, 10 + self.pos.y + 6))
            offset += command.get_width() + 8

    def update_commands(self):
        self.check_active()

        if self.active:
            self.commands = self.text.split()
            self.render_commands()

"""
###################################################################################################

ITEM CLASSES

###################################################################################################
"""

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

"""
###################################################################################################

ITEMS

###################################################################################################
"""

i_sock = Item("Sock", "A Random Sock")

c_milk = Consumable("Milk", "Some questionable bottled dairy")

w_knife = Weapon("Knife", "A rusty butterknife", "melee", 3, 65)
w_wrench = Weapon("Wrench", "A shiny cresent wrench", "melee", 1, 100)

"""
###################################################################################################

ITEM CONTAINERS

###################################################################################################
"""

items_container = [
    i_sock
]
    
consumables_container = [
    c_milk
]
    
weapons_container = [
    w_knife,
    w_wrench
]

for item in items_container:
    item_keywords.append(str(item.name))

for consumable in consumables_container:
    consumable_keywords.append(str(consumable.name))

for weapon in weapons_container:
    weapon_keywords.append(str(weapon.name))
    
"""
###################################################################################################

CONTAINER CLASS

###################################################################################################
"""

class Container():
    def __init__(self, name: str, lock_state: str):
        self.name = name

        self.lock_state = lock_state

        self.items = []

    def search_container(self):
        if self.lock_state == "unlocked":
            header_line = FeedbackLine('you find...')
            game.feedback_prompt.feedback_lines.append(header_line)

            if len(self.items) > 0:
                for item in self.items:
                    line = FeedbackLine(f"{item.name}")
                    game.feedback_prompt.feedback_lines.append(line)
            else:
                blank_line = FeedbackLine(" ")
                game.feedback_prompt.feedback_lines.append(blank_line)
        else:
            error_line = FeedbackLine(f" the {self.name} is locked")
            game.feedback_prompt.feedback_lines.append(error_line)


"""
###################################################################################################

ROOM CLASS

###################################################################################################
"""

class Room():
    def __init__(self, name: str, description: str, items: list):
        self.name = name
        self.description = description

        self.items = items
        self.containers = []
        self.doors = []

    def pickup(self, item_name: str):
        for item in self.items:
            if item.name == item_name:
                game.player.add_to_inventory(item)
                line = FeedbackLine(f"you picked up {item.name}")
                game.feedback_prompt.feedback_lines.append(line)
                self.items.remove(item)

        for container in self.containers:
            if container.lock_state == "unlocked":
                for item in container.items:
                    if item.name == item_name:
                        game.player.add_to_inventory(item)
                        line = FeedbackLine(f"you picked up {item.name}")
                        game.feedback_prompt.feedback_lines.append(line)
                        container.items.remove(item)

        blank_line = FeedbackLine(" ")
        game.feedback_prompt.feedback_lines.append(blank_line)

    def search_room(self):
        header_line = FeedbackLine("you find...")
        game.feedback_prompt.feedback_lines.append(header_line)

        for container in self.containers:
            line = FeedbackLine(f"a {container.name} that appears to be {container.lock_state}")
            game.feedback_prompt.feedback_lines.append(line)

        for items in self.items:
            line = FeedbackLine(f"a {items.name} on the ground")
            game.feedback_prompt.feedback_lines.append(line)

        blank_line = FeedbackLine(" ")
        game.feedback_prompt.feedback_lines.append(blank_line)

    def search_container(self, container_name: str):
        for container in self.containers:
            if container.name == container_name:
                container.search_container()

"""
###################################################################################################

ROOM CONTAINER

###################################################################################################
"""

rooms = {
    "spawn": Room("Spawn Room", "The room where you spawn... duh", [i_sock])
}

rooms["spawn"].containers.append(Container("chest", "unlocked"))
rooms["spawn"].containers.append(Container("footlocker", "locked"))
rooms["spawn"].containers[0].items.append(w_knife)

"""
###################################################################################################

PLAYER CLASS

###################################################################################################
"""

class Player():
    def __init__(self):
        self.inventory = []
        self.health = 10

    def add_to_inventory(self, item: Item):
        self.inventory.append(item)

        blank_line = FeedbackLine(" ")
        game.feedback_prompt.feedback_lines.append(blank_line)

    def list_inventory(self):
        header_line = FeedbackLine("your inventory contains...")
        game.feedback_prompt.feedback_lines.append(header_line)

        if len(self.inventory) > 0:
            for item in self.inventory:
                line = FeedbackLine(item.name)
                game.feedback_prompt.feedback_lines.append(line)
        else:
            blank_line = FeedbackLine(" ")
            game.feedback_prompt.feedback_lines.append(blank_line)

"""
###################################################################################################

MAIN GAME CLASS

###################################################################################################
"""

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Project Yarchus")

        self.running = True
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.events = pygame.event.get()

        self.player = Player()
        self.current_room = rooms["spawn"]

        self.feedback_prompt = FeedbackPrompt(50, 50, 900, 600)
        self.command_prompt = CommandPrompt(50, 700, 900, 50)

        self.commands_list = {
            "admin_add": ["item: Item", "adds the entered item to the player inventory", self.command_admin_add],
            "admin_list": ["n/a", "lists all items in the game", self.command_admin_list],
            "help": ["n/a", "displays this prompt", self.command_help],
            "clear": ["n/a", "clears the feedback prompt", self.feedback_prompt.reset_prompt],
            "inv": ["n/a", "lists the players inventory", self.player.list_inventory],
            "exit": ["n/a", "ends the program", self.command_exit],
            "whereami": ["n/a", "tells you what room you are in", self.command_whereami],
            "desc_room": ["n/a", "describes the current room you are in", self.command_desc_room],
            "search_room": ["n/a", "searches the current room you are in", self.current_room.search_room],
            "search_container": ["container: Container", "searches the entered container", self.current_room.search_container],
            "pickup": ["item: Item", "picks up the entered item", self.current_room.pickup]
        }

    def start(self):
        while self.running:
            self.event_loop()
            self.draw()
            self.update()

    def event_loop(self):
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.command_prompt.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.command_prompt.text = self.command_prompt.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.command_prompt.process_command()
                    else:
                        self.command_prompt.text += event.unicode

    def command_help(self):
        header_line = FeedbackLine("Command | Arguments | Description")
        self.feedback_prompt.feedback_lines.append(header_line)

        for command in self.commands_list:
            line = FeedbackLine(f"{command} | {self.commands_list[command][0]} | {self.commands_list[command][1]}")
            self.feedback_prompt.feedback_lines.append(line)

        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    def command_admin_add(self, keyword: str):
        added_item = None

        for item in items_container:
            if item.name == keyword:
                added_item = item

        for consumable in consumables_container:
            if consumable.name == keyword:
                added_item = consumable

        for weapon in weapons_container:
            if weapon.name == keyword:
                added_item = weapon

        self.player.add_to_inventory(added_item)

        line = FeedbackLine(f"DEBUG: Added {added_item.name} to player inventory")
        self.feedback_prompt.feedback_lines.append(line)

        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    def command_admin_list(self):
        header_line = FeedbackLine("Items: (name, description)")
        self.feedback_prompt.feedback_lines.append(header_line)

        for item in items_container:
            line = FeedbackLine(f"{item.name} , {item.description}")
            self.feedback_prompt.feedback_lines.append(line)

        header_line = FeedbackLine("Consumables: (name, description)")
        self.feedback_prompt.feedback_lines.append(header_line)
        
        for consumable in consumables_container:
            line = FeedbackLine(f"{consumable.name} , {consumable.description}")
            self.feedback_prompt.feedback_lines.append(line)

        header_line = FeedbackLine("Weapons: (name, description, type, damage)")
        self.feedback_prompt.feedback_lines.append(header_line)
        
        for weapon in weapons_container:
            line = FeedbackLine(f"{weapon.name} , {weapon.description} , {weapon.type} , {weapon.damage}")
            self.feedback_prompt.feedback_lines.append(line)

        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    def command_exit(self):
        self.running = False

    def command_whereami(self):
        line = FeedbackLine(f"you are in {self.current_room.name}")
        self.feedback_prompt.feedback_lines.append(line)

        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    def command_desc_room(self):
        line = FeedbackLine(f"the room you are in is {self.current_room.description}")
        self.feedback_prompt.feedback_lines.append(line)

        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    def draw(self):
        self.screen.fill(C_BLACK)

        self.feedback_prompt.draw_feedback()
        self.command_prompt.draw_commands()

    def update(self):
        self.command_prompt.update_commands()

        pygame.display.update()
        self.delta_time = self.clock.tick(120) / 1000

"""
###################################################################################################

LAUNCH GAME

###################################################################################################
"""

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()