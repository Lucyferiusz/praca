import pygame
import sys

class StartMenu:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font = pygame.font.Font(None, 36)

    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.is_clicked(mouse_x, mouse_y, self.screen.get_width() // 2, self.screen.get_height() // 2 - 50):
                        return "start"
                    
                    elif self.is_clicked(mouse_x, mouse_y, self.screen.get_width() // 2, self.screen.get_height() // 2 + 50):
                        pygame.quit()
                        sys.exit()

            self.screen.fill((0, 0, 0))
            self.draw_text("Start Game", (255, 255, 255), self.screen.get_width() // 2, self.screen.get_height() // 2 - 50)
            self.draw_text("Quit", (255, 255, 255), self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)

            pygame.display.flip()

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_x, mouse_y, button_x, button_y):
        button_rect = pygame.Rect(button_x - 75, button_y - 15, 150, 30)  # Ustawienia prostokąta przycisku
        return button_rect.collidepoint(mouse_x, mouse_y)
