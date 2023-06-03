import pygame

import lib

class CommandPrompt():
    def __init__(self, x: int, y: int, width: int, height: int):

        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)

        self.active = True

        self.text = ""
        self.commands = self.text.split()
        self.rendered_commands = []

        self.commands_list = {
            "exit": ["no args", "ends the program"],
            "help": ["no args", "displays this prompt"],
            "inv": ["no args", "lists the items in the players inventory"],
            "des": ["arg: item name (case sensitive)", "describes the item entered"],
            "cons": ["arg: item name (case sensitive)", "consumes the item entered"]
        }

    def check_active(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.pos.x < mouse_x < self.pos.x + self.size.x:
            if self.pos.y < mouse_y < self.pos.y + self.size.y:
                if pygame.mouse.get_pressed()[0]:
                    self.active = True

    def text_input(self):
        for event in lib.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.process_command()
                else:
                    self.text += event.unicode

    def process_command(self):
        if len(self.commands) > 1:
            if self.commands[0] in self.commands_list:
                print("this was a command with a argument")
            else:
                print("invalid command")
        else:
            if self.commands[0] in self.commands_list:
                print("this was a command")
            else:
                print("invalid command")
        
        self.text = ""


    def render_commands(self):
        self.rendered_commands = []

        for command in self.commands:
            if command in self.commands_list:
                rendered_command = lib.font.bold.render(command, True, lib.color.command)
            else:
                rendered_command = lib.font.regular.render(command, True, lib.color.text)

            self.rendered_commands.append(rendered_command)

    def draw_commands(self, surface: pygame.Surface):
        offset = 10

        for command in self.rendered_commands:
            surface.blit(command, (offset, self.pos.y + 10))
            offset += command.get_width() + 10

    def update_commands(self):
        self.check_active()

        if self.active:
            self.text_input()
            self.commands = self.text.split()
            self.render_commands()
