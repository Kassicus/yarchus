import pygame

import lib

class FeedbackLine():
    def __init__(self, text: str):
        self.text = text

        self.words = self.text.split()

        self.line = []

        self.color_words()

    def color_words(self):
        for word in self.words:
            if word in lib.item_keywords:
                c_word = lib.font.bold.render(word, True, lib.color.item)
            elif word in lib.consumable_keywords:
                c_word = lib.font.bold.render(word, True, lib.color.consumable)
            elif word in lib.weapon_keywords:
                c_word = lib.font.bold.render(word, True, lib.color.weapon)
            else:
                c_word = lib.font.regular.render(word, True, lib.color.text)

            self.line.append(c_word)

class FeedbackPrompt():
    def __init__(self, x: int, y: int, width: int, height: int):
        
        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)

        self.feedback_lines = []

    def reset_prompt(self):
        self.feedback_lines = []

    def draw_feedback(self, surface: pygame.Surface):
        vert_offset = 10 + self.pos.x
        horiz_offset = 10 + self.pos.y

        pygame.draw.rect(surface, lib.color.field, (self.pos.x, self.pos.y, self.size.x, self.size.y))

        for line in self.feedback_lines:
            horiz_offset = 10 + self.pos.x

            for word in line.line:
                surface.blit(word, (horiz_offset, vert_offset))
                horiz_offset += word.get_width() + 10
            
            vert_offset += 30

    def update_feedback(self):
       pass

class CommandPrompt():
    def __init__(self, x: int, y: int, width: int, height: int, feedback_prompt: FeedbackPrompt):

        self.pos = pygame.math.Vector2(x, y)
        self.size = pygame.math.Vector2(width, height)

        self.active = False

        self.feedback_prompt = feedback_prompt

        self.text = ""
        self.commands = self.text.split()
        self.rendered_commands = []

        self.commands_list = {
            "exit": ["no args", "ends the program"],
            "help": ["no args", "displays this prompt"],
            "inv": ["no args", "lists the items in the players inventory", lib.player.show_inventory],
            "des": ["arg: item name (case sensitive)", "describes the item entered"],
            "cons": ["arg: item name (case sensitive)", "consumes the item entered"],
            "test": ["no args", "testing the command printing thingy", self.test],
            "clear": ["no args", "clears the feedback window", self.clear_feedback]
        }

    def test(self):
        line = FeedbackLine("this will test item consumable and weapon highligting")
        self.feedback_prompt.feedback_lines.append(line)

    def clear_feedback(self):
        self.feedback_prompt.reset_prompt()

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
                self.commands_list[self.commands[0]][2](self.commands[1])
            else:
                line = FeedbackLine("invalid command")
                self.feedback_prompt.feedback_lines.append(line)
        else:
            if self.commands[0] in self.commands_list:
                self.commands_list[self.commands[0]][2]()
            else:
                line = FeedbackLine("invalid command")
                self.feedback_prompt.feedback_lines.append(line)
        
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
        offset = self.pos.x + 10

        pygame.draw.rect(surface, lib.color.field, (self.pos.x, self.pos.y, self.size.x, self.size.y))

        if self.active:
            pygame.draw.rect(surface, lib.color.text, (self.pos.x, self.pos.y, self.size.x, self.size.y), 1)

        for command in self.rendered_commands:
            surface.blit(command, (offset, self.pos.y + 10))
            offset += command.get_width() + 10

    def update_commands(self):
        self.check_active()

        if self.active:
            self.text_input()
            self.commands = self.text.split()
            self.render_commands()
