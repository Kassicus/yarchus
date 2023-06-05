import pygame

import lib
import command

pygame.init()

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode([lib.SCREEN_WIDTH, lib.SCREEN_HEIGHT])
        pygame.display.set_caption("Project Yarchus")

        self.running = True
        self.clock = pygame.time.Clock()
        lib.events = pygame.event.get()

        self.feedback_prompt = command.FeedbackPrompt(50, 50, 700, 500)
        self.command_prompt = command.CommandPrompt(50, 650, 700, 40, self.feedback_prompt)
        
    def start(self):
        while self.running:
            self.events()
            self.draw()
            self.update()

    def events(self):
        lib.events = pygame.event.get()
        
        for event in lib.events:
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.fill(lib.color.black)

        self.feedback_prompt.draw_feedback(self.screen)
        self.command_prompt.draw_commands(self.screen)

    def update(self):
        self.feedback_prompt.update_feedback()
        self.command_prompt.update_commands()

        pygame.display.update()
        lib.delta_time = self.clock.tick(lib.framerate) / 1000

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()