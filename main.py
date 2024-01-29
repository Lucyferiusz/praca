import pygame
import sys
from scripts.config import *
from scripts.sprites import *
from scripts.inventory import *
from scripts.EnemySpawner import *
from scripts.Quest import *
from scripts.game_over_screen import *
from scripts.start_menu import *
from scripts.Skill import *

# !!!!!
from dev import *
# !!!!!


class Game:
    def __init__(self):

        

        pygame.init()
        pygame.mixer.init()
        background_music_path = "assets/music/1.mp3"
        pygame.mixer.music.load(background_music_path)
        pygame.mixer.music.set_volume(0.02)
        pygame.mixer.music.play(-1)

        # Poziom przybliżenia i wymiary okna gry
        self.zoom_level = 1.0
        self.WIN_WIDTH = 1080
        self.WIN_HEIGHT = 720
        self.map_width = len(map_01[0])
        self.map_height = len(map_01)

        # Inicjalizacja ekranu i zegara
        self.screen = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.win_game = False

        self.attacks = pygame.sprite.LayeredUpdates()
        self.spawners = pygame.sprite.LayeredUpdates()

        # Nowe elementy inwentarza
        self.inventory = Inventory(self.screen,self)
        self.dragging_offset = (-20, -20)
        self.original_slot = None
        self.is_mouse_dragging = False
        # Elementy SkillTree
        skills = [
            MultiAttack(self,'assets/img/skill1.png', 'Wielo krotny atak',(0,0),500,1),
            SpeedBust(self,"assets/img/skill2.png", "Rycerski Błysk", (0,0),1000,2),
            ImmortalDefence(self,"assets/img/skill3.png", "Nieśmiertelna tarcza", (350, 100),2000,3),
        ]
        self.skillTree= SkillTree(self ,self.screen,skills)
        self.skillTree_open = False
        # Przykładowa broń dodana do inwentarza
        #itemy
        
        self.all_items ={
            #weapon
            "rusted_sword": Weapon("Zardzewiały miecz","assets/img/rust_sword.png",5,0),
            "sword":Weapon("Ostry miecz","assets/img/sword_1.png",10,25),
            "saber":Weapon("Szabla","assets/img/sword_2.png",15,100),
            "club":Weapon("Metalowa maczuga","assets/img/club.png",20,500),
            #armor
            "lether_armor":Armor("Skurzana zbroja","assets/img/lether_armor.png",5,30),
            "chain_armor":Armor("Kolczuga","assets/img/chain.png",15,150),
            "plate_armor":Armor("Zbroja płytowa","assets/img/plate_armor.png",20,750),
            
            #item
            "potion": Potion("Potion","assets/img/potion.png",20),
            "lether": Item("Skóra","assets/img/lether.png",2),
            "jewellery": Item("Birzuteria","assets/img/jewellery.png",15),
            "arrow": Item("Strzały","assets/img/arrow.png",1),
            "book": Item("Księga","assets/img/book.png",5),
            "skull": Item("Czaszka","assets/img/demon_skull.png",1000),
            "broken_dagger": Item("Złamany miecz","assets/img/broken_dagger.png",8)


        }
        
        
        self.inventory.add_item(self.all_items['rusted_sword'].new())  # Dodanie testowej broni do drugiego slotu
        # self.inventory.add_item(self.all_items['skull'].new())  # Dodanie testowego przedmiotu

        
        

        # Inicjalizacja spritesheets
        self.character_spritesheet = Spritesheet('assets/img/character.png')
        self.mage_spritesheet = Spritesheet('assets/img/mage.png')
        self.bandit_spritesheet = Spritesheet('assets/img/bandit.png')
        self.archer_spritesheet = Spritesheet('assets/img/archer.png')
        self.npc_spritesheet = Spritesheet('assets/img/npc.png')
        self.terrain_spritesheet = Spritesheet('assets/img/terrain.png')
        self.attack_spritesheet = Spritesheet('assets/img/attack.png')
        self.rats_spritesheet = Spritesheet('assets/img/rats.png')
        self.wildboar_spritesheet = Spritesheet('assets/img/wildboar.png')
        self.demon_spritesheet = Spritesheet('assets/img/demon32.png')

        # Inne elementy i ustawienia
        self.question_mark_image = pygame.image.load('assets/img/rat.png')
        self.dt = 0
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.inventory_open = False
        # self.dialogue_box = False
        
        # Questy
        
        self.killed_enemies = []
        self.rat_spawner = []
        self.demon_spawner = []
        self.current_quest = 0
        self.quest_log_open = False
        self.quest_log = QuestLog(self)
        
    def kill_enemy(self, enemy_type):
        # Metoda wywoływana po zabiciu przeciwnika
        self.killed_enemies.append(enemy_type)

    # Metoda rysująca tekst na ekranie
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Metoda tworząca mapę z kafelkami
    def createTilemap(self):
        self.map_width = int(self.map_width * self.zoom_level)
        self.map_height = int(self.map_height * self.zoom_level)
        for i, row in enumerate(map_01):
            for j, column in enumerate(row):
                if column == '~':
                    Water(self, j, i)
                elif column == 'B':
                    Bridge(self, j, i)
                    pass
                elif column == '0':
                    Ground(self, j, i)
                elif column == "P":
                    self.player = Player(self, j, i)
                    self.camera = Camera(self, self.player)
                    Ground(self, j, i)
                elif column == "D":
                    EnemySpawner(self,j,i,5*FPS,5,WildBoar)
                    Ground(self, j, i)
                elif column == "N":
                    NPC(self, j, i)
                    Ground(self, j, i)
                elif column == 'f':
                    Field(self, j, i)
                elif column == 'W':
                    Ground(self, j, i)
                    Wall(self, j, i, 'left')
                elif column == 'V':
                    Ground(self, j, i)
                    Wall(self, j, i, 'right')
                elif column == 'w':
                    Ground(self, j, i)
                    Wall(self, j, i, 'up')
                elif column == 'v':
                    Ground(self, j, i)
                    Wall(self, j, i, 'down')
                elif column == 'G':
                    Ground(self, j, i)
                    Gate(self, j, i)
                elif column == 'h':
                    Ground(self, j, i)
                    Healer(self, j, i)
                elif column == 'F':
                    Ground(self, j, i)
                    Farmer(self, j, i)
                elif column == '$':
                    Ground(self, j, i)
                    Shopkeeper(self, j, i)
                elif column =='R':
                    self.rat_spawner.append(RatSpawner(self,j,i,FPS*4,5,Rat,False))
                    Ground(self, j, i)
                elif column =='^':
                    self.demon_spawner.append(DemonSpawner(self,j,i,FPS*4,1,Demon,False))
                    Ground(self, j, i)
                elif column =='?':
                    EnemySpawnerPack(self,j,i,FPS*5,4)
                    Ground(self, j, i)
                else:
                    Ground(self, j, i)

    # Metoda inicjująca nową grę
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        
        self.enemies_attacks = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.LayeredUpdates()
        self.damage_frame_group = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    # Metoda obsługująca zdarzenia
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP2:
                    if self.current_quest == 0:
                        self.current_quest=0
                    else:
                        self.current_quest-=1
                if event.key == pygame.K_KP8:
                    if self.current_quest == len(self.quest_log.quests)-1:
                        self.current_quest=len(self.quest_log.quests)-1
                    else:
                        self.current_quest+=1
                        
                    
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        self.attack0 = Attack(self, self.player.rect.x ,self.player.rect.y-TILESIZE )
                    if self.player.facing == 'down':
                        self.attack0 = Attack(self, self.player.rect.x ,self.player.rect.y+TILESIZE )
                    if self.player.facing == 'left':
                        self.attack0 = Attack(self, self.player.rect.x - TILESIZE ,self.player.rect.y)
                    if self.player.facing == 'right':
                        self.attack0 = Attack(self, self.player.rect.x +TILESIZE,self.player.rect.y)
                        
           # Dodaj obsługę klawisza "I" dla otwierania inwentarza
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.inventory_open = not self.inventory_open

                    if self.inventory_open:
                        self.inventory.draw_inventory()
                if event.key == pygame.K_q:
                    self.quest_log_open = not self.quest_log_open

                if event.key == pygame.K_e:
                    self.check_interactions()
                if event.key == pygame.K_u:
                    self.skillTree_open = not self.skillTree_open
                    if self.skillTree_open:
                        self.skillTree.handle_mouse_click(event)
                if event.key == pygame.K_1:
                    MultiAttack.use(self.skillTree.skills[0])
                if event.key == pygame.K_2:
                    self.skillTree.skills[1].use()
                if event.key == pygame.K_3:
                    self.skillTree.skills[2].use()
            
            if self.inventory_open:
                self.inventory.handle_events(event)
            if self.skillTree_open:
                self.skillTree.handle_mouse_click(event)
            
            

    # Metoda aktualizująca stan gry
    def update(self):
        self.all_sprites.update()
                
        pygame.display.update()
        self.skillTree.skills[2].update()

    # Metoda sprawdzająca interakcje z NPC
    def check_interactions(self):
        for npc in pygame.sprite.spritecollide(self.player, self.npcs, False):
            if npc.talkable:
                npc.initiate_dialogue()

    # Metoda rysująca obiekty na ekranie
    def draw(self):
        self.camera.update(self.player)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.damage_frame_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        self.attacks.draw(self.screen)
        self.player.draw_health_bar()
        self.player.draw_level_bar()

        if self.inventory_open:
            self.inventory.draw_inventory()
            if self.inventory.dragging_item:
                self.inventory.draw_item(
                    self.inventory.dragging_item,
                    pygame.mouse.get_pos()[0] + self.dragging_offset[0],
                    pygame.mouse.get_pos()[1] + self.dragging_offset[1]
                )
        if self.skillTree_open:
            self.skillTree.draw()
        if self.quest_log_open == True:
            self.quest_log.display_quests(self.screen,self.current_quest)
        
        self.skillTree.skills[1].update()
        pygame.display.flip()
        self.clock.tick(FPS)

    # Główna pętla gry
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if self.win_game:
                self.game_win()
            
        self.running = False

    # Metoda wyświetlająca ekran końca gry
    def game_over(self):
        game_over_screen = GameOverScreen(self.WIN_WIDTH, self.WIN_HEIGHT)
        game_over_screen.show()
        pass
    def game_win(self):
        game_over_screen = GameOverScreen(self.WIN_WIDTH, self.WIN_HEIGHT)
        game_over_screen.show()
        pass
    def intro_dialog_screen(self):
        #!!!!!
        test = IntroDialog(self.WIN_WIDTH,self.WIN_HEIGHT)
        test.show()
        #!!!!!


    
    # Ekran początkowy gry
    def intro_screen(self):  
        start_menu = StartMenu (self.WIN_WIDTH, self.WIN_HEIGHT)
        choice = start_menu.show()

        if choice == "start":
            self.new()
            while self.running:
                self.intro_dialog_screen()
                self.main()
                self.game_over()
        elif choice == "load":
            pass
        elif choice == "quit":
            pygame.quit()
            sys.exit()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
