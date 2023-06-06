import pygame

pygame.init()

#############
# CONSTANTS #
#############

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

C_BLACK = pygame.Color(0, 0, 0)
C_TEXT = pygame.Color(255, 255, 255)
C_COMMAND = pygame.Color(0, 255, 0)
C_ITEM = pygame.Color(255, 255, 255)
C_WEAPON = pygame.Color(255, 0, 0)
C_CONSUMABLE = pygame.Color(0, 255, 255)
C_DEBUG = pygame.Color(255, 255, 0)
C_FIELD = pygame.Color(60, 60, 60)

F_REGULAR = pygame.font.SysFont("Courier", 16)
F_BOLD = pygame.font.SysFont("Courier", 16, bold = True)
F_ITALIC = pygame.font.SysFont("Courier", 16, italic = True)
F_BOLD_ITALIC = pygame.font.SysFont("Courier", 16, bold = True, italic = True)

#################
# KEYWORD LISTS #
#################

item_keywords = [
    "item"
]

consumable_keywords = [
    "consumable"
]

weapon_keywords = [
    "weapon"
]
    
####################
# TERMINAL CLASSES #
####################

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
        horizontal_offset = 10 + self.pos.x
        vertical_offset = 10 + self.pos.y
        
        pygame.draw.rect(game.screen, C_FIELD, (self.pos.x, self.pos.y, self.size.x, self.size.y))

        for line in self.feedback_lines:
            horizontal_offset = 10 + self.pos.x

            for word in line.line:
                game.screen.blit(word, (horizontal_offset, vertical_offset))
                horizontal_offset += word.get_width() + 10

            vertical_offset += 30

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
                game.commands_list[self.commands[0]][2](self.commands[1])
            else:
                line = FeedbackLine("invalid command")
                game.feedback_prompt.feedback_lines.append(line)
        else:
            if self.commands[0] in game.commands_list:
                game.commands_list[self.commands[0]][2]()
            else:
                line = FeedbackLine("invalid command")
                game.feedback_prompt.feedback_lines.append(line)

        self.text = ""

    def render_commands(self):
        self.rendered_commands = []

        for command in self.commands:
            if command in game.commands_list:
                rendered_command = F_BOLD.render(command, True, C_COMMAND)
            else:
                rendered_command = F_REGULAR.render(command, True, C_TEXT)

            self.rendered_commands.append(rendered_command)

    def draw_commands(self):
        offset = 10 + self.pos.x

        pygame.draw.rect(game.screen, C_FIELD, (self.pos.x, self.pos.y, self.size.x, self.size.y))

        if self.active:
            pygame.draw.rect(game.screen, C_TEXT, (self.pos.x, self.pos.y, self.size.x, self.size.y), 1)

        for command in self.rendered_commands:
            game.screen.blit(command, (offset, 10 + self.pos.y))
            offset += command.get_width() + 10

    def update_commands(self):
        self.check_active()

        if self.active:
            self.commands = self.text.split()
            self.render_commands()

    
################
# ITEM CLASSES #
################

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
    
################
# PLAYER CLASS #
################

class Player():
    def __init__(self):
        self.inventory = []
        self.health = 10

    def add_to_inventory(self, item: Item):
        self.inventory.append(item)


###################
# MAIN GAME CLASS #
###################

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Project Yarchus")

        self.running = True
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.events = pygame.event.get()

        self.commands_list = {
            "test": ["no args", "testing the feedback prompt", self.command_test],
            "clear": ["no args", "clears the feedback prompt", self.command_clear]
        }

        self.feedback_prompt = FeedbackPrompt(50, 50, 700, 500)
        self.command_prompt = CommandPrompt(50, 600, 700, 50)

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

    def command_test(self):
        line = FeedbackLine("This will test item consumable and weapon highlighting")
        self.feedback_prompt.feedback_lines.append(line)
    
    def command_clear(self):
        self.feedback_prompt.reset_prompt()

    def draw(self):
        self.screen.fill(C_BLACK)

        self.feedback_prompt.draw_feedback()
        self.command_prompt.draw_commands()

    def update(self):
        self.command_prompt.update_commands()

        pygame.display.update()
        self.delta_time = self.clock.tick(120) / 1000

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()