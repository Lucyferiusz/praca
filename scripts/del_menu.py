import pygame

class InventoryScreen:
    def __init__(self, game, player):
        self.pause_frame = False
        self.pause_duration= 200

        self.scroll_position = 0  # Pozycja przewijania
        self.menu_height = 11  # Maksymalna liczba przedmiotów na ekranie

        self.game = game
        self.player = player
        self.items = player.inventory
        self.selected_item = None if len(self.items)==0 else 0
        self.active_item = 0
        self.rect = pygame.Rect(
            game.WIN_WIDTH // 4,  # 25% szerokości ekranu
            game.WIN_HEIGHT // 4,  # 25% wysokości ekranu
            game.WIN_WIDTH // 2,  # 50% szerokości ekranu
            game.WIN_HEIGHT // 2  # 50% wysokości ekranu
        )
    def scroll_up(self):
        if self.scroll_position > 0:
            self.scroll_position -= 1

    def scroll_down(self):
        max_scroll = max(len(self.items) - self.menu_height, 0)
        if self.scroll_position < max_scroll:
            self.scroll_position += 1

    def draw(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.rect)

        # Oblicz indeksy przedmiotów do wyświetlenia na ekranie
        start_index = self.scroll_position
        end_index = min(start_index + self.menu_height, len(self.items))
        
        
        for i in range(start_index, end_index):
            item = self.items[i]
            item_rect = pygame.Rect(
                self.rect.left + 10,
                self.rect.top + 10 + (i - start_index) * 40,
                self.rect.width - 20,
                30
            )

            if i == self.active_item:
                pygame.draw.rect(self.game.screen, (255, 0, 0), item_rect, 2)  # Highlight selected item with a red border
            else:
                pygame.draw.rect(self.game.screen, (255, 255, 255), item_rect, 2)
            self.game.draw_text(
                f"{i+1} {item.name} - {item.description}",
                self.game.font,
                (255, 255, 255),
                item_rect.centerx,
                item_rect.centery
            )


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP8:
                self.select_previous_item()
                self.scroll_up()
            elif event.key == pygame.K_KP2:
                self.select_next_item()
                self.scroll_down()
            elif event.key == pygame.K_KP_ENTER:
                self.use_selected_item()
                self.scroll_position = 0
            self.handle_pause()


    def select_previous_item(self):
        if self.active_item is not None:
            self.active_item = max(0, self.active_item - 1)

    def select_next_item(self):
        if self.active_item is not None:
            self.active_item = min(len(self.items) - 1, self.active_item + 1)
    
    def use_selected_item(self):

        if not self.pause_frame:
            if self.active_item is not None:
                selected_item = self.items[self.active_item]
                print(selected_item.name)
                self.player.use_item(selected_item)
                self.pause_frame = True
                self.active_item = None if len(self.items)==0 else 0

            self.pause_timer = pygame.time.get_ticks()

    def handle_pause(self):  
        if self.pause_frame:
            now = pygame.time.get_ticks()
            if now - self.pause_timer >= self.pause_duration:
                self.pause_frame = False

