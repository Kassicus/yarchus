import pygame

pygame.init()

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode([800, 800])
        pygame.display.set_caption("color_input")

        self.font = pygame.font.SysFont("Courier", 16)

        self.text = ""
        self.words = self.text.split()
        self.keywords = [
            "test",
            "cooper"
        ]
        self.rendered_words = []
        self.word_count = len(self.words)
        self.old_word_count = 0

        self.running = True
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()

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
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def render_words(self):
        self.rendered_words = []

        for word in self.words:
            if word in self.keywords:
                rendered_word = self.font.render(word, True, (0, 255, 255))
            else:
                rendered_word = self.font.render(word, True, (255, 255, 255))
            
            self.rendered_words.append(rendered_word)

    def draw_words(self, surface):
        offset = 100
        
        for word in self.rendered_words:
            surface.blit(word, (offset, 700))
            offset += word.get_width() + 10

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.draw_words(self.screen)

    def update(self):
        self.words = self.text.split()
        
        self.render_words()

        pygame.display.update()
        self.clock.tick(30)

if __name__ == '__main__':
    game = Game()
    game.start()
    pygame.quit()