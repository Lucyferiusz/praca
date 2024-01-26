import pygame
import random
from scripts.config import *
from scripts.inventory import *

class Quest:
    def __init__(self, name, description, tasks, rewards):
        self.name = name
        self.description = description
        self.tasks = tasks
        self.rewards = rewards
        self.completed = False
        self.claim = False
        
        

    def check_completion(self, enemy_type = None,enemy_type_target=None, item=None, interacted=False):
        # Sprawdzanie, czy wszystkie zadania zostały ukończone
        
        if not any([enemy_type_target, item, interacted]):
            self.completed = all(task['completed'] for task in self.tasks)
        else:
            for task in self.tasks:
                
                if task.get('enemy_type') == enemy_type and task['type'] == 'kill' and not task['completed']:
                    task['current_count_kill'] += 1
                    task['completed'] = task['current_count_kill'] >= task['target_count_kill']
                elif task.get('item') == item and task['type'] == 'item' and not task['completed'] :
                    task['current_count_item'] += 1
                    task['completed'] = task['current_count_item'] >= task['target_count_item']
                elif task.get('type') == 'interact':
                    task['completed'] = interacted
            self.completed = all(task['completed'] for task in self.tasks)

    def claim_rewards(self, player):
        # Przyznawanie nagród graczowi za ukończenie questu
        if self.claim:
            return
        if self.completed:
            player.gain_xp(self.rewards['xp'])
            player.gold += self.rewards['gold']
            self.claim = True
            # Dodaj kod do dodawania przedmiotów do ekwipunku gracza itp.

    

class QuestLog:
    def __init__(self,game):

        self.active_quest = False
        self.quests = []
        self.complete_quests = []
        self.game = game

    def add_quest(self, quest):
        # Dodawanie nowego questu do QuestLogu
        if not self.active_quest:
            self.quests.append(quest)
            self.active_quest = True
    def remove_quest(self, quest):
        # Dodawanie nowego questu do QuestLogu
        self.quests.remove(quest)
        if quest.tasks[0]['type']=='kill' and quest.tasks[0]['enemy_type'] == "Rat":
            for rats in self.game.rat_spawner:
                rats.active_quest_rat = False
            pass
        if quest.tasks[0]['type']=='kill' and quest.tasks[0]['enemy_type'] == "Demon":
            print("win")
            for demon in self.game.demon_spawner:
                demon.active_quest_demon = False
            self.game.win_game = True
            pass
        self.active_quest = False

    def update(self, player,enemy_type = None,item = None):
        # Aktualizacja stanu questów w QuestLogu       
        for quest in self.quests:
            for task in quest.tasks:
                if task['type']== 'kill':
                    quest.check_completion(enemy_type= enemy_type, enemy_type_target=task['enemy_type'])
                elif task['type']== 'item':
                    quest.check_completion(item = item)
                    pass
            if quest.completed:
                quest.claim_rewards(player)
                self.remove_quest(quest)
                

    def display_quests(self, surface,current_quest):
        WIDTH = 800
        HEIGHT = 600
        pygame.draw.rect(surface, WHITE, (0, 0, WIDTH, HEIGHT))  # Rysuj białe tło

        font = pygame.font.Font(None, 36)
        y_offset = 50
        if not self.quests:
            # Zabezpieczenie dla braku questów
            no_quest_text = font.render("No quests available.", True, BLACK)
            surface.blit(no_quest_text, (50, y_offset))
            pygame.display.flip()
            return
        quest = self.quests[current_quest]
        text_quest = font.render(f"Quest: {quest.name}", True, BLACK)
        text_description = font.render(f"Description: {quest.description}", True, BLACK)
        surface.blit(text_quest, (50, y_offset))
        y_offset += 40
        surface.blit(text_description, (50, y_offset))
        y_offset += 40

        text_tasks = font.render("Tasks:", True, BLACK)
        surface.blit(text_tasks, (50, y_offset))
        y_offset += 40

        for task in quest.tasks:
            status = "Completed" if task['completed'] else "Incomplete"
            text_task = font.render(f" - {task['name']}: {status}", True, BLACK)
            if task['type']=='kill':
                progres = font.render(f"{task['current_count_kill'] } / {task['target_count_kill']}", True, BLACK)
                surface.blit(progres, (50+text_task.get_width()+10, y_offset))
            if task['type']=='item':
                progres = font.render(f"{task['current_count_item'] } / {task['target_count_item']}", True, BLACK)
                surface.blit(progres, (50+text_task.get_width()+10, y_offset))
            surface.blit(text_task, (50, y_offset))
            
            y_offset += 40

        text_rewards = font.render("Rewards:", True, BLACK)
        surface.blit(text_rewards, (50, y_offset))
        y_offset += 40

        text_xp = font.render(f" - XP: {quest.rewards['xp']}", True, BLACK)
        surface.blit(text_xp, (50, y_offset))
        y_offset += 40

        text_gold = font.render(f" - Gold: {quest.rewards['gold']}", True, BLACK)
        surface.blit(text_gold, (50, y_offset))
        y_offset += 40

        if 'potions' in quest.rewards:
            text_potions = font.render(f" - Potions: {quest.rewards['potions']}", True, BLACK)
            surface.blit(text_potions, (50, y_offset))
            y_offset += 40

        y_offset += 20  # Dodaj odstęp między zadaniami a kolejnym questem

        pygame.display.flip()  # Odśwież ekran po narysowaniu

# Tworzenie przykładowych questów
farmer_quest = Quest(
    name="Pomoc dla farmera",
    description="Pomóż farmerowi w polu.",
    tasks=[
        {'name': 'Pomoc w polu', 'completed': False}
    ],
    rewards={'xp': 100, 'gold': 40}
)


medic_quest = Quest(
    name="Zadanie dla medyka",
    description="Znajdź specjalne zioło dla medyka.",
    tasks=[
        {'name': 'Znajdź zioło', 'completed': False}
    ],
    rewards={'xp': 100, 'gold': 3}
)

item_quest = Quest(
    name="Zadanie ze zdobywaniem przedmiotów",
    description="Zdobądź określoną ilość przedmiotów.",
    tasks=[
        {'name': 'Zdobyć 5 birzuteri ', 'completed': False, 'item': 'jewellery', 'type': 'item', 'target_count_item': 5, 'current_count_item': 0},
    ],
    rewards={'xp': 100, 'gold': 40, 'item': 'example_reward_item'}
)
item_quest2 = Quest(
    name="Zadanie ze zdobywaniem przedmiotów",
    description="Zdobądź określoną ilość przedmiotów.",
    tasks=[
        {'name': 'Zdobyć 5 lether ', 'completed': False, 'item': 'lether', 'type': 'item', 'target_count_item': 50, 'current_count_item': 0},
    ],
    rewards={'xp': 100, 'gold': 40, 'item': 'example_reward_item'}
)
head_village_quest = Quest(
    name="Zadania dla Wodza Wioski",
    description="Pokonaj bandytów w okolicy.",
    tasks=[
        {'name': 'Pokonaj bandytów', 'completed': False, 'enemy_type': 'Bandit', 'type': 'kill', 'target_count_kill': 3, 'current_count_kill': 0},
        {'name': 'Oczyść wioskę ze łuczników', 'completed': False, 'enemy_type': 'Archer', 'type': 'kill', 'target_count_kill': 2, 'current_count_kill': 0},
        {'name': 'Oczyść wioskę ze magów', 'completed': False, 'enemy_type': 'Mage', 'type': 'kill', 'target_count_kill': 1, 'current_count_kill': 0},
    ],
    rewards={'xp': 500, 'gold': 400}
)
rat_nest_quest = Quest(
    name="Zadania dla Wodza Wioski",
    description="Oczyść wioskę ze szczurów.",
    tasks=[
        {'name': 'Oczyść wioskę ze szczurów', 'completed': False, 'enemy_type': 'Rat', 'type': 'kill', 'target_count_kill': 10, 'current_count_kill': 0},
    ],
    rewards={'xp': 100, 'gold': 50}
)
final_quest = Quest(
    name="Zadania dla Wodza Wioski",
    description="Zabij demona błąkającego się na świecie.",
    tasks=[
        {'name': 'Zabij demona błąkającego się na świecie', 'completed': False, 'enemy_type': 'Demon', 'type': 'kill', 'target_count_kill': 1, 'current_count_kill': 0},
    ],
    rewards={'xp': 1000, 'gold': 5000}
)

# Dodanie questów do QuestLogu


# Przykładowa aktualizacja QuestLogu (tu wymaga dostępu do obiektu gracza, więc zakładam, że jest on dostępny)
# player = Player()  # Tworzenie obiektu gracza
# quest_log.update(player)


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
            text = font.render(f"Witam podróżniku, jestem uzdrowicielem. Czego potrzebujesz?", True, (255, 255, 255))
            dialogue_surface.blit(text, (20, 20))

            # Dodaj opcje dialogowe
            options = ["Potrzebuję leczenia (90 złota)", "Chciałbym kupić miksturę (50 złota)" , "Aktualnie nic nie potrzebuję, żegnaj"]
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

    
    def handle_dialog_option(self, option):
        if option == 1:
            # Potrzebuję leczenia
            if self.game.player.gold >= 90:
                self.game.player.gold -= 90
                self.game.player.heal(50)

        elif option == 2:
            # Chciałbym kupić miksturę
            if self.game.player.gold >= 50:
                self.game.player.gold -= 50
                potion = self.game.all_items['potion'].new()
                self.game.inventory.add_item(potion)

        elif option == 3:
            pass

class Farmer(NPC):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, name="Farmer", dialogue="Cześć! Mam świeże produkty prosto z pola.")
        self.image_npc = self.game.npc_spritesheet.get_sprite(2, 2, self.width, self.height)
        self.image_npc_active = self.game.npc_spritesheet.get_sprite(2+32, 2, self.width, self.height)
    def initiate_dialogue(self):
        pass

class Shopkeeper(NPC):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, name="Shopkeeper", dialogue="Witaj! Oferuję różne przedmioty. Co chciałbyś kupić?")
        self.image_npc = self.game.npc_spritesheet.get_sprite(2, 2+32, self.width, self.height)
        self.image_npc_active = self.game.npc_spritesheet.get_sprite(2+32, 2+32, self.width, self.height)
    def initiate_dialogue(self):
        # Funkcja do rozpoczęcia dialogu
        if self.talkable:
            # Stwórz nową powierzchnię na tekst
            dialogue_surface = pygame.Surface((600, 400), pygame.SRCALPHA)
            pygame.draw.rect(dialogue_surface, (0, 0, 0, 128), dialogue_surface.get_rect())  # Czarny prostokąt z przezroczystością

            # Dodaj tekst do powierzchni
            font = pygame.font.Font(None, 24)
            text = font.render(f"Witaj! Oferuję różne przedmioty. Co chciałbyś kupić?", True, (255, 255, 255))
            dialogue_surface.blit(text, (20, 20))

            # Dodaj opcje dialogowe
            options = [
                "Ostry Miecz [+10 Atak] (50 złota)",#1
                "Skurzana zbroja [+5 Obrona] (60 złota)", #2
                "Kolczuga [+15 Obrona] (300 złota)", #3
                "Szabla [+15 Atak] (200 złota)", #4
                "Metalowa maczuga [+20 Atak] (1000 złota)", #5
                "Zbroja płytowa [+20 Obrona] (1500 złota)", #6
                "Zapytaj o misję",#7
                "Nic, dzięki"]#8
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
            
            selected_option = None
            waiting_for_exit = True
            while waiting_for_exit:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if pygame.K_1 <= event.key <= pygame.K_8:
                            selected_option = event.key - pygame.K_1 + 1

                if selected_option:
                    self.handle_dialog_option(selected_option)
                    waiting_for_exit = False

                pygame.time.Clock().tick(30)  # Kontroluj szybkość pętli

            print("Zakończono dialog z Shopkeeperem.")

    def handle_dialog_option(self, option):
        if option == 1:
            
            self.buy_item('sword',50)
        elif option == 2:

            self.buy_item('lether_armor', 60)
        elif option == 3:
            self.buy_item('chain_armor',300)
        if option == 4:
    
            self.buy_item('saber', 200)
        elif option == 5:
            self.buy_item('club', 1000)
        elif option == 6:

            self.buy_item('plate_armor',1500)
        elif option == 7:
            self.waiting_for_exit= False
            self.ask_about_quest()
        elif option == 8:
            # Nic, dzięki
            print("Dzięki, wróć, jeśli coś będzie ci potrzebne.")

    def buy_item(self,item_type, cost):        
        if self.game.player.gold >= cost:
            self.game.player.gold -= cost
            new_item = self.game.all_items[item_type].new()
            self.game.inventory.add_item(new_item)


    def ask_about_quest(self):
        # Zamknij okno sklepu
        # Pytanie o misję
        print("Czy masz jakieś zadania dla mnie?")

        # Tutaj możesz dodać logikę dotyczącą przyznawania nowych zadań dla gracza
        # Przykład logiczny: Załóżmy, że masz listę dostępnych zadań `available_quests`
        # available_quests = ["Pokonaj bandytów", "Zdobądź skarby", "Pozbądź się szczurów z wioski"]
        available_quests =[
            {'name':"Pokonaj bandytów",'quest':head_village_quest,'active_rat':False,'demon_active':False},
            {'name':"Pozbądź się gniazda szczurów",'quest':rat_nest_quest,'active_rat':True,'demon_active':False},
            {'name':"Zdobądź skarby",'quest':item_quest,'active_rat':False,'demon_active':False}
                           ]
        
        if self.game.player.level == 3:
            available_quests = [
            {'name':"Zabij demona",'quest':final_quest,'active_rat':False,'demon_active':True}
                           ]

        #["Pokonaj bandytów", "Zdobądź skarby", "Pozbądź się szczurów z wioski"]
        if available_quests and not self.game.quest_log.active_quest:
            selected_quest = random.choice(available_quests)
            quest_text = f"Jasne, mam dla ciebie zadanie: {selected_quest['name']}"
            options = ["Chętnie pomogę!", "Może później"]
            self.show_quest_dialog(quest_text, options,selected_quest)
        else:
            # Brak dostępnych zadań
            quest_text = f"Niestety, nie mam dla ciebie żadnych zadań."
            options = ["Żegnaj"]
            self.show_quest_dialog(quest_text, options)
            print("Niestety, nie mam dla ciebie żadnych zadań.")

    def show_quest_dialog(self, quest_text, options,quest = None):
        # Stwórz nową powierzchnię na tekst
        quest_surface = pygame.Surface((600, 300), pygame.SRCALPHA)
        pygame.draw.rect(quest_surface, (0, 0, 0, 255), quest_surface.get_rect())  # Czarny prostokąt z przezroczystością

        # Dodaj tekst do powierzchni
        font = pygame.font.Font(None, 24)
        text = font.render(quest_text, True, (255, 255, 255))
        quest_surface.blit(text, (20, 20))

        # Dodaj opcje dialogowe
        for i, option in enumerate(options):
            option_text = font.render(f"{i + 1}. {option}", True, (255, 255, 255))
            quest_surface.blit(option_text, (20, 80 + i * 30))

        # Wyśrodkuj powierzchnię z tekstem na ekranie
        screen_rect = self.game.screen.get_rect()
        quest_rect = quest_surface.get_rect(center=screen_rect.center)

        # Wyświetl powierzchnię z tekstem
        self.game.screen.blit(quest_surface, quest_rect.topleft)
        pygame.display.flip()

        # Oczekuj na zamknięcie okna dialogowego po naciśnięciu klawisza
        waiting_for_exit = True
        selected_option = None

        while waiting_for_exit:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_2:
                        selected_option = event.key - pygame.K_1 + 1

            if selected_option == 1:
                self.game.quest_log.add_quest(quest['quest'])
                if quest['active_rat']:
                    for rats in self.game.rat_spawner:
                        rats.active_quest_rat = True
                    pass
                if quest['demon_active']:
                    for demon in self.game.demon_spawner:
                        demon.active_quest_demon = True
                    pass
                waiting_for_exit = False
            elif selected_option == 2:
                waiting_for_exit = False

            pygame.time.Clock().tick(30)  # Kontroluj szybkość pętli

        return selected_option
    
    
