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

item_keywords = [] # this gets updated by a function later

consumable_keywords = [] # this gets updated by a function later

weapon_keywords = [] # this gets updated by a function later
    
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
    def __init__(self, text: str) -> object:
        """ creates a 'feedback line' displayed in the feedback prompt
        
        arguments:
        text: str - the text to be displayed in the feedback line
        """

        self.text = text
        self.words = self.text.split()

        self.line = [] # this is the important thing, we draw the words directly out of these containers
        self.parse_words()

    # this applies highlighting and font weight to words if they appear in the keyword lists
    def parse_words(self) -> None:
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

            self.line.append(p_word) # add each word to the line

class FeedbackPrompt():
    def __init__(self, x: int, y: int, width: int, height: int) -> object:
        """ creates a window in which to display all of the feedback lines
        
        arguments:
        x: int - the horizontal position of the window
        y: int - the vertical position of the window
        width: int - the width (horizontal) of the window
        height: int - the height (vertical) of the window
        """

        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)

        self.space = 8
        self.line_height = 30

        self.feedback_lines = [] # contains all of the FeedbackLine objects

    # this should probably be done without a standalone function, but its here in case this ever gets more complicated
    def reset_prompt(self) -> None:
        self.feedback_lines = []

    # draw all of the lines, manage the list first to never have more than 20 lines on screen
    def draw_feedback(self) -> None:
        self.manage_feedback_lines()

        # jenky offset stuff, it just creates the base point for spacing the words out
        horizontal_offset = 10 + self.pos.x
        vertical_offset = 10 + self.pos.y
        
        pygame.draw.rect(game.screen, C_FIELD, (self.pos.x, self.pos.y, self.size.x, self.size.y)) # background of the prompt

        for line in self.feedback_lines:
            horizontal_offset = 10 + self.pos.x # reset the x position for each vertical line

            # draw each word in each line to the screen, spacing by 8 pixels
            for word in line.line:
                game.screen.blit(word, (horizontal_offset, vertical_offset))
                horizontal_offset += word.get_width() + self.space

            vertical_offset += self.line_height # set the new offset for the next line

    # maintain a maximum of 20 lines of text on the screen at once, scroll the rest of the text vertically out of the window (delete them...)
    def manage_feedback_lines(self) -> None:
        if len(self.feedback_lines) > 20:
            self.feedback_lines.pop(0)

class CommandPrompt():
    def __init__(self, x: int, y: int, width: int, height: int) -> object:
        """ creates the main command prompt
         
        arguments:
        x: int - the horizontal position of the command prompt
        y: int - the vertical position of the command prompt
        width: int - the width (horizontal) of the command prompt
        height: int - the height (vertical) of the command prompt
        """

        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)

        self.active = False

        self.space = 8

        self.text = ""
        self.commands = self.text.split()
        self.rendered_commands = [] # similar to the feedback lines in the feedback prompt, but containing all of the words in the current command

    def check_active(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # gross logic loop to determine if the box is active or not
        # TODO: figure out if this is absolutely necessary, we could probably get rid of it if there is nothing we need to click on
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

    # this whole function is a mess, but it works and thats what matters
    def process_command(self) -> None:
        # if we have more than one 'command' present (more than one word)
        if len(self.commands) > 1:
            if self.commands[0] in game.commands_list: # check if the first command is present in our command list
                try:
                    game.commands_list[self.commands[0]][2](self.commands[1]) # if it is, try to pass the second command as an argument
                except:
                    # if for whatever reason this fails, let the user know that they have an invalid argument
                    # this wont catch everything, but it allows the user to fix the problem
                    # TODO: make this more granular, figure out what the error is and give better feedback to the player
                    line = FeedbackLine("INVALID: argument")
                    game.feedback_prompt.feedback_lines.append(line)
            else:
                # if the command isnt present, let the user know. (commands also get highlighted in real time, they should notice if they have it wrong)
                line = FeedbackLine("INVALID: command")
                game.feedback_prompt.feedback_lines.append(line)

                blank_line = FeedbackLine(" ")
                game.feedback_prompt.feedback_lines.append(blank_line)
        else: # this is now running commands that don't have arguments present, much simpler here
            if self.commands[0] in game.commands_list:
                game.commands_list[self.commands[0]][2]()
            else:
                # same as before, if the command doesnt match, we let the user know
                line = FeedbackLine("INVALID: command")
                game.feedback_prompt.feedback_lines.append(line)

                blank_line = FeedbackLine(" ")
                game.feedback_prompt.feedback_lines.append(blank_line)

        self.text = "" # after the command has been processed, reset the text in the command prompt

    # similar to parsing words in the feedback line, this will color the commands in real-time to provide input feedback
    def render_commands(self) -> None:
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

            self.rendered_commands.append(rendered_command) # create a list of all of the newly colored and font-sized commands

    # draw each word in the command string to the command line
    def draw_commands(self) -> None:
        offset = 10 + self.pos.x

        pygame.draw.rect(game.screen, C_FIELD, (self.pos.x, self.pos.y, self.size.x, self.size.y)) # draw the background

        # if we are the active prompt, draw a white highlight around the prmopt
        if self.active:
            pygame.draw.rect(game.screen, C_TEXT, (self.pos.x, self.pos.y, self.size.x, self.size.y), 1)

        # draw each word in the command string and offset by the space
        for command in self.rendered_commands:
            game.screen.blit(command, (offset, 10 + self.pos.y + 6))
            offset += command.get_width() + self.space

    # update the command prompt
    def update_commands(self):
        self.check_active()

        # only accept new command input if the command prompt is active
        if self.active:
            self.commands = self.text.split()
            self.render_commands()

"""
###################################################################################################

ITEM CLASSES

###################################################################################################
"""

# the base item that everything becomes (not sure if these all need to be items, but it allows me to treat them all the same)
class Item():
    def __init__(self, name: str, description: str) -> object:
        """ the base item, used for objects without special abilities, and as the base for special items
        
        arguments:
        name: str - the name of the object
        description: str - the description of the object
        """

        self.name = name
        self.description = description

# these are specifically items that can be consumed by the player, think food or potions
class Consumable(Item):
    def __init__(self, name: str, description: str) -> Item:
        """ the base consumable, extensds the item
        
        arguments:
        name: str - the name of the consumable
        description: str - the description of the consumable
        """

        super().__init__(name, description)

# these are specifically items that do damage
class Weapon(Item):
    def __init__(self, name: str, description: str, w_type: str, damage: int, durability: int) -> Item:
        """ the base weapon, extends the item
        
        arguments:
        name: str - the name of the weapon
        description: str - the description of the weapon
        w_type: str - the damage type of the weapon (melee, ranged, magic)
        damage: int - the amount of damage the weapon does
        durability: int - the amount of uses the weapon has
        """

        super().__init__(name, description)
        
        self.type = w_type
        self.damage = damage
        self.durability = durability

"""
###################################################################################################

ITEMS

###################################################################################################
"""

# prefix items with an i for Item, c for Consumable and w for Weapon
i_sock = Item("Sock", "A Random Sock")

c_milk = Consumable("Milk", "Some questionable bottled dairy")

w_knife = Weapon("Knife", "A rusty butterknife", "melee", 3, 65)
w_wrench = Weapon("Wrench", "A shiny cresent wrench", "melee", 1, 100)

"""
###################################################################################################

ITEM CONTAINERS

###################################################################################################
"""

# manually adding all items to this master container, these are not accessible to the player directly
items_container = [
    i_sock
]

# manually adding all consumables to this master container, these are not accessible to the player directly    
consumables_container = [
    c_milk
]
    
# manually adding all weapons to this master container, these are not accessible to the player directly    
weapons_container = [
    w_knife,
    w_wrench
]

# TODO: make all of these import automatically from a text or json file?
# autofill the keywords so the player does not have to manually put things in 3 places...
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
    def __init__(self, name: str, lock_state: str) -> object:
        """ creates a container 
        
        attributes:
        name: str - the name of the container, (chest, footlocker, ect)
        lock_state: str - the current state of the lock on the container (locked, unlocked)
        """
        
        self.name = name

        self.lock_state = lock_state

        self.items = []

    # TODO: create the logic to allow the player to unlock the container (requires lockpicks? bruteforce?)

    # handles all logic for searching a container
    def search_container(self) -> None:
        # if the container is unlocked, we print all of the items present in the container
        if self.lock_state == "unlocked":
            header_line = FeedbackLine('you find...')
            game.feedback_prompt.feedback_lines.append(header_line)

            if len(self.items) > 0:
                for item in self.items:
                    line = FeedbackLine(f"{item.name}")
                    game.feedback_prompt.feedback_lines.append(line)
            # if the container is empty we just print this blank line
            else:
                blank_line = FeedbackLine(" ")
                game.feedback_prompt.feedback_lines.append(blank_line)
        # if the container is locked we let the user know that the container is unlocked
        else:
            error_line = FeedbackLine(f" the {self.name} is locked")
            game.feedback_prompt.feedback_lines.append(error_line)


"""
###################################################################################################

ROOM CLASS

###################################################################################################
"""

class Room():
    def __init__(self, name: str, description: str, items: list) -> object:
        """ creates a room
        
        arguments:
        name: str - the name of the room
        description: str - the description of the room
        items: list - the items found not in containers in the room
        """
        
        self.name = name
        self.description = description

        self.items = items
        self.containers = []
        self.doors = []

    # handles the picking up of items present anywhere in the room, including its containers
    def pickup(self, item_name: str):
        for item in self.items:
            if item.name == item_name: # we just match the items name with the string that was given, if there is no match we do nothing
                game.player.add_to_inventory(item)
                line = FeedbackLine(f"you picked up {item.name}")
                game.feedback_prompt.feedback_lines.append(line)
                self.items.remove(item)

        for container in self.containers:
            if container.lock_state == "unlocked": # the container must be unlocked to be included in this pickup list
                for item in container.items: # same logic as above, just for the items in each container
                    if item.name == item_name:
                        game.player.add_to_inventory(item)
                        line = FeedbackLine(f"you picked up {item.name}")
                        game.feedback_prompt.feedback_lines.append(line)
                        container.items.remove(item)

        # blank line for cleanliness
        blank_line = FeedbackLine(" ")
        game.feedback_prompt.feedback_lines.append(blank_line)

    # shows all of the floor items as well as all of the containers and their states
    def search_room(self):
        header_line = FeedbackLine("you find...")
        game.feedback_prompt.feedback_lines.append(header_line)

        # show the state of all containers
        for container in self.containers:
            line = FeedbackLine(f"a {container.name} that appears to be {container.lock_state}")
            game.feedback_prompt.feedback_lines.append(line)

        # list all items on the floor
        for items in self.items:
            line = FeedbackLine(f"a {items.name} on the ground")
            game.feedback_prompt.feedback_lines.append(line)

        # blank line for cleanliness
        blank_line = FeedbackLine(" ")
        game.feedback_prompt.feedback_lines.append(blank_line)

    # search an individual container
    def search_container(self, container_name: str):
        for container in self.containers:
            if container.name == container_name:
                container.search_container()

"""
###################################################################################################

ROOM CONTAINER

###################################################################################################
"""

# manual list of the rooms in the game
rooms = {
    "spawn": Room("Spawn Room", "The room where you spawn... duh", [i_sock])
}

# TODO: make this system better
# for now we are manually adding the containers and items in the containers to the rooms, should probably create a helper function for this?
rooms["spawn"].containers.append(Container("chest", "unlocked"))
rooms["spawn"].containers.append(Container("footlocker", "locked"))
rooms["spawn"].containers[0].items.append(w_knife)

"""
###################################################################################################

PLAYER CLASS

###################################################################################################
"""

class Player():
    def __init__(self) -> object:
        """ creates the player (this should only be instanced once) """

        self.inventory = []
        self.health = 10

    # add an item to inventory, this requires the actual Item type not a string
    def add_to_inventory(self, item: Item) -> None:
        self.inventory.append(item)

        # blank line for cleanliness
        blank_line = FeedbackLine(" ")
        game.feedback_prompt.feedback_lines.append(blank_line)

    def list_inventory(self) -> None:
        header_line = FeedbackLine("your inventory contains...")
        game.feedback_prompt.feedback_lines.append(header_line)

        # if there is anything in the inventory, then print each inventory item on its own line
        if len(self.inventory) > 0:
            for item in self.inventory:
                line = FeedbackLine(item.name)
                game.feedback_prompt.feedback_lines.append(line)
        else:
            # otherwise draw a blank line for cleanliness
            blank_line = FeedbackLine(" ")
            game.feedback_prompt.feedback_lines.append(blank_line)

"""
###################################################################################################

MAIN GAME CLASS

###################################################################################################
"""

class Game():
    def __init__(self) -> object:
        """ the main game class (should only be instanced once) """

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

        # all of the current commands in the game, formatted as "string": ["args", "description", function] the function gets called '()' later
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

    def start(self) -> None:
        # if the game is running, do all of the shit
        while self.running:
            self.event_loop()
            self.draw()
            self.update()

    def event_loop(self) -> None:
        self.events = pygame.event.get() # update the event list

        # handle all of the events
        for event in self.events:
            # kill the game if we get the quit event (equivilent of hitting the x)
            if event.type == pygame.QUIT:
                self.running = False
            
            # keyboard logic, currently just used to enter text in the command prompt
            if event.type == pygame.KEYDOWN:
                if self.command_prompt.active:
                    # TODO: make the backspace remove characters if its held down?
                    if event.key == pygame.K_BACKSPACE:
                        self.command_prompt.text = self.command_prompt.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.command_prompt.process_command()
                    else:
                        self.command_prompt.text += event.unicode

    # prints all of the commands to the feedback prompt
    def command_help(self) -> None:
        # loose structure description in header line
        header_line = FeedbackLine("Command | Arguments | Description")
        self.feedback_prompt.feedback_lines.append(header_line)

        # create the feedback line from each command entry in the commands dict
        for command in self.commands_list:
            line = FeedbackLine(f"{command} | {self.commands_list[command][0]} | {self.commands_list[command][1]}")
            self.feedback_prompt.feedback_lines.append(line)

        # blank line for cleanliness
        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    # adds any item as long as it exists
    def command_admin_add(self, keyword: str) -> None:
        added_item = None # this is a placeholder for the item, things break if we dont init it first

        # check against the items container
        for item in items_container:
            if item.name == keyword:
                added_item = item

        # check against the consumables
        for consumable in consumables_container:
            if consumable.name == keyword:
                added_item = consumable

        # check against the weapons
        for weapon in weapons_container:
            if weapon.name == keyword:
                added_item = weapon

        # by this point we should have an item
        # TODO: this has the potential for issues if we don't have a match and I don't think we are handling that
        self.player.add_to_inventory(added_item)

        # create the feedback line that we added the item
        line = FeedbackLine(f"DEBUG: Added {added_item.name} to player inventory")
        self.feedback_prompt.feedback_lines.append(line)

        # blank line for cleanliness
        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    # list all items in the game that can be added with the admin command
    # TODO: create a grid layout version for this or we will run out of space with only having 20 lines. We might need to make things scrollable?
    def command_admin_list(self) -> None:
        # header line to break up categories
        header_line = FeedbackLine("Items: (name, description)")
        self.feedback_prompt.feedback_lines.append(header_line)

        # loop through items and add all items
        for item in items_container:
            line = FeedbackLine(f"{item.name} , {item.description}")
            self.feedback_prompt.feedback_lines.append(line)

        # header line to break up categories
        header_line = FeedbackLine("Consumables: (name, description)")
        self.feedback_prompt.feedback_lines.append(header_line)
        
        # loop through all consumables
        for consumable in consumables_container:
            line = FeedbackLine(f"{consumable.name} , {consumable.description}")
            self.feedback_prompt.feedback_lines.append(line)

        # header line to break up weapons
        header_line = FeedbackLine("Weapons: (name, description, type, damage)")
        self.feedback_prompt.feedback_lines.append(header_line)
        
        # loop through all the weapons
        for weapon in weapons_container:
            line = FeedbackLine(f"{weapon.name} , {weapon.description} , {weapon.type} , {weapon.damage}")
            self.feedback_prompt.feedback_lines.append(line)

        # blank line for cleanliness
        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    # kills the program
    def command_exit(self) -> None:
        self.running = False

    # tells the player what room they are in
    def command_whereami(self) -> None:
        line = FeedbackLine(f"you are in {self.current_room.name}")
        self.feedback_prompt.feedback_lines.append(line)

        # break line for cleanliness
        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    # describes the room the player is in
    def command_desc_room(self) -> None:
        line = FeedbackLine(f"the room you are in is {self.current_room.description}")
        self.feedback_prompt.feedback_lines.append(line)

        # blank line for cleanliness
        blank_line = FeedbackLine(" ")
        self.feedback_prompt.feedback_lines.append(blank_line)

    # draws everything, which isnt that much
    def draw(self):
        self.screen.fill(C_BLACK) # fill the screen to black every frame

        # draw everything new
        self.feedback_prompt.draw_feedback()
        self.command_prompt.draw_commands()

    # udpates everyting, also not much
    def update(self):
        # allow the command prompt to get the
        self.command_prompt.update_commands()

        pygame.display.update()
        self.delta_time = self.clock.tick(120) / 1000 # this might not be necessary, but we calc delta time anyways

"""
###################################################################################################

LAUNCH GAME

###################################################################################################
"""

# typical python do shit if you are the main function
if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()