import pygame
import random
from scripts.config import *
from scripts.inventory import *

class Quest:
    def __init__(self, name, description, reward):
        self.name = name
        self.description = description
        self.reward = reward
        self.completed = False

    def complete(self):
        self.completed = True
        print(f"Quest '{self.name}' completed! You receive: {self.reward}")


class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name="Bob", dialogue="TEST"):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x_change = 0
        self.y_change = 0
        self.facing = random.choice(['left', 'right', 'up'])
        self.movement_loop = 0

        self.name = name
        self.dialogue = dialogue
        self.talkable = False

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image_npc = self.game.npc_spritesheet.get_sprite(2, 2+32*3, self.width, self.height)
        self.image_npc_active = self.game.npc_spritesheet.get_sprite(2+32, 2+32*3, self.width, self.height)
        
        self.image = self.image_npc

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        # Sprawdź, czy gracz jest wystarczająco blisko, aby rozmawiać
        player = self.game.player
        distance_to_player = pygame.math.Vector2(player.rect.centerx - self.rect.centerx,
                                                 player.rect.centery - self.rect.centery).length()

        if distance_to_player <= 2 * TILESIZE:
            self.talkable = True
        else:
            self.talkable = False

        # Aktualizuj obraz NPC w zależności od tego, czy jest rozmowny
        if self.talkable:
            self.image = self.image_npc_active
        else:
            self.image = self.image_npc

    def initiate_dialogue(self):
        # Funkcja do rozpoczęcia dialogu
        if self.talkable:
            # Stwórz nową powierzchnię na tekst
            dialogue_surface = pygame.Surface((600, 300), pygame.SRCALPHA)
            pygame.draw.rect(dialogue_surface, (0, 0, 0, 128), dialogue_surface.get_rect())  # Czarny prostokąt z przezroczystością

            # Dodaj tekst do powierzchni
            font = pygame.font.Font(None, 36)
            text = font.render(f"Rozpoczęto dialog z NPC: {self.name}", True, (255, 255, 255))
            dialogue_surface.blit(text, (20, 20))

            # Dodaj informację o wyjściu
            exit_text = font.render("Naciśnij klawisz 'Wyjdz' aby zakończyć dialog.", True, (255, 255, 255))
            dialogue_surface.blit(exit_text, (20, 80))

            # Wyśrodkuj powierzchnię z tekstem na ekranie
            screen_rect = self.game.screen.get_rect()
            dialogue_rect = dialogue_surface.get_rect(center=screen_rect.center)

            # Wyświetl powierzchnię z tekstem
            self.game.screen.blit(dialogue_surface, dialogue_rect.topleft)
            pygame.display.flip()

            # Oczekuj na zamknięcie okna dialogowego po naciśnięciu klawisza 'Wyjdz'
            waiting_for_exit = True
            while waiting_for_exit:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:  # Naciśnięcie klawisza 'Wyjdz'
                        waiting_for_exit = False

                pygame.time.Clock().tick(30)  # Kontroluj szybkość pętli

            print("Zakończono dialog z NPC.")



class Healer(NPC):
    def __init__(self, game, x, y):
        
        super().__init__(game, x, y, name="Healer", dialogue="Witaj podróżniku! Potrzebujesz uzdrowienia?")
        self.image_npc = self.game.npc_spritesheet.get_sprite(2, 2+32*2, self.width, self.height)
        self.image_npc_active = self.game.npc_spritesheet.get_sprite(2+32, 2+32*2, self.width, self.height)

    def initiate_dialogue(self):
        # Funkcja do rozpoczęcia dialogu
        if self.talkable:
            # Stwórz nową powierzchnię na tekst
            dialogue_surface = pygame.Surface((600, 300), pygame.SRCALPHA)
            pygame.draw.rect(dialogue_surface, (0, 0, 0, 128), dialogue_surface.get_rect())  # Czarny prostokąt z przezroczystością

            # Dodaj tekst do powierzchni
            font = pygame.font.Font(None, 24)
            text = font.render(f"Witam podróżniku, jestem uzdrowicielem. Czy potrzebujesz leczenia?", True, (255, 255, 255))
            dialogue_surface.blit(text, (20, 20))

            # Dodaj opcje dialogowe
            options = ["Potrzebuję leczenia", "Chciałbym kupić miksturę", "Aktualnie nic nie potrzebuję, żegnaj"]
            for i, option in enumerate(options):
                option_text = font.render(f"{i + 1}. {option}", True, (255, 255, 255))
                dialogue_surface.blit(option_text, (20, 80 + i * 30))

            # Wyśrodkuj powierzchnię z tekstem na ekranie
            screen_rect = self.game.screen.get_rect()
            dialogue_rect = dialogue_surface.get_rect(center=screen_rect.center)

            # Wyświetl powierzchnię z tekstem
            self.game.screen.blit(dialogue_surface, dialogue_rect.topleft)
            pygame.display.flip()

            # Oczekuj na zamknięcie okna dialogowego po naciśnięciu klawisza 'Wyjdz'
            waiting_for_exit = True
            selected_option = None

            while waiting_for_exit:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if pygame.K_1 <= event.key <= pygame.K_3:
                            selected_option = event.key - pygame.K_1 + 1

                if selected_option:
                    self.handle_dialog_option(selected_option)
                    waiting_for_exit = False

                pygame.time.Clock().tick(30)  # Kontroluj szybkość pętli

            print("Zakończono dialog z NPC.")
    
    def handle_dialog_option(self, option):
        if option == 1:
            # Potrzebuję leczenia
            if self.game.player.gold >= 10:
                self.game.player.gold -= 10
                self.game.player.heal(20)
                print("Zostałeś uzdrowiony! Zapłacono 10 złota.")
            else:
                print("Nie masz wystarczająco złota na leczenie.")
        elif option == 2:
            # Chciałbym kupić miksturę
            if self.game.player.gold >= 5:
                self.game.player.gold -= 5
                potion = Potion("Mikstura HP")
                self.game.inventory.add_item(potion)
                print("Kupiłeś miksturę! Zapłacono 5 złota.")
            else:
                print("Nie masz wystarczająco złota na zakup mikstury.")
        elif option == 3:
            # Aktualnie nic nie potrzebuję, żegnaj
            print("Do widzenia!")



class Farmer(NPC):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, name="Farmer", dialogue="Cześć! Mam świeże produkty prosto z pola.")
        self.image_npc = self.game.npc_spritesheet.get_sprite(2, 2, self.width, self.height)
        self.image_npc_active = self.game.npc_spritesheet.get_sprite(2+32, 2, self.width, self.height)
    def initiate_dialogue(self):
        print("Rozpoczęto dialog z Farmerem.")
        print("Farmer: Cześć! Mam świeże produkty prosto z pola.")

class Shopkeeper(NPC):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, name="Shopkeeper", dialogue="Witaj! Oferuję różne przedmioty. Co chciałbyś kupić?")
        self.image_npc = self.game.npc_spritesheet.get_sprite(2, 2+32, self.width, self.height)
        self.image_npc_active = self.game.npc_spritesheet.get_sprite(2+32, 2+32, self.width, self.height)
    def initiate_dialogue(self):
        # Funkcja do rozpoczęcia dialogu
        if self.talkable:
            # Stwórz nową powierzchnię na tekst
            dialogue_surface = pygame.Surface((600, 300), pygame.SRCALPHA)
            pygame.draw.rect(dialogue_surface, (0, 0, 0, 128), dialogue_surface.get_rect())  # Czarny prostokąt z przezroczystością

            # Dodaj tekst do powierzchni
            font = pygame.font.Font(None, 24)
            text = font.render(f"Witaj! Oferuję różne przedmioty. Co chciałbyś kupić?", True, (255, 255, 255))
            dialogue_surface.blit(text, (20, 20))

            # Dodaj opcje dialogowe
            options = ["Ostry Miecz [+10 Atak] (50 złota)", "Skurzana zbroja [+5 Obrona] (60 złota)", "Kolczugo +1 (300 złota)", "Nic, dzięki"]
            for i, option in enumerate(options):
                option_text = font.render(f"{i + 1}. {option}", True, (255, 255, 255))
                dialogue_surface.blit(option_text, (20, 80 + i * 30))

            # Wyśrodkuj powierzchnię z tekstem na ekranie
            screen_rect = self.game.screen.get_rect()
            dialogue_rect = dialogue_surface.get_rect(center=screen_rect.center)

            # Wyświetl powierzchnię z tekstem
            self.game.screen.blit(dialogue_surface, dialogue_rect.topleft)
            pygame.display.flip()

            # Oczekuj na zamknięcie okna dialogowego po naciśnięciu klawisza 'Wyjdz'
            waiting_for_exit = True
            selected_option = None

            while waiting_for_exit:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if pygame.K_1 <= event.key <= pygame.K_4:
                            selected_option = event.key - pygame.K_1 + 1

                if selected_option:
                    self.handle_dialog_option(selected_option)
                    waiting_for_exit = False

                pygame.time.Clock().tick(30)  # Kontroluj szybkość pętli

            print("Zakończono dialog z Shopkeeperem.")

    def handle_dialog_option(self, option):
        if option == 1:
            # Kup Miecz +1 (10 złota)
            self.buy_item("Ostry Miecz",Weapon,10, 10)
        elif option == 2:
            # Kup Zbroja +1 (15 złota)
            self.buy_item("Skurzana Zbroja",Armor,5, 15)
        elif option == 3:
            # Kup Hełm +1 (8 złota)
            self.buy_item("Kolczuga",Armor,10 ,8)
        elif option == 4:
            # Nic, dzięki
            print("Dzięki, wróć, jeśli coś będzie ci potrzebne.")

    def buy_item(self, item_name,item_type,stats, cost):
        
        if self.game.player.gold >= cost:
            self.game.player.gold -= cost
            if item_type == Weapon:
                print(item_type)
                new_item = Weapon(item_name,stats)  # Assuming you have an Item class defined
            if item_type == Armor:
                print(item_type)
                new_item = Armor(item_name,stats)  # Assuming you have an Item class defined
            if item_type == Tool:
                print(item_type)
                new_item = Tool(item_name,stats)  # Assuming you have an Item class defined
            
            self.game.inventory.add_item(new_item)
            print(f"Kupiłeś {item_name}! Zapłacono {cost} złota.")
        else:
            print("Nie masz wystarczająco złota na zakup tego przedmiotu.")
