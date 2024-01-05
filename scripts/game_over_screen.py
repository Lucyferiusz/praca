import pygame
import sys

class GameOverScreen:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font = pygame.font.Font(None, 36)

    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.draw_text("Game Over", (255, 0, 0), self.screen.get_width() // 2, self.screen.get_height() // 2 - 50)
            self.draw_text("Press Q to Quit", (255, 255, 255), self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

            pygame.display.flip()

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
