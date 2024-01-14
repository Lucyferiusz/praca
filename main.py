import pygame
import sys
from scripts.config import *
from scripts.sprites import *
from scripts.inventory import *
from scripts.EnemySpawner import *
from scripts.game_over_screen import *
from scripts.start_menu import *

class Game:
    def __init__(self):
        pygame.init()
        self.zoom_level = 1.0
        self.WIN_WIDTH = 1080
        self.WIN_HEIGHT = 720
        self.map_width = len(map_01[0])
        self.map_height = len(map_01)

        self.screen = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Nowe elementy inwentarza
        
        self.inventory = Inventory(self.screen,self)
        self.dragging_offset = (-20, -20)
        self.original_slot = None
        self.is_mouse_dragging = False


        rusted_sword = Weapon("Rusted sword",5,0)
        rusted_sword.set_image("assets/img/rust_sword.png")

        self.inventory.add_item(rusted_sword)  # Add the test weapon to the second slot


        self.character_spritesheet = Spritesheet('assets/img/character.png')
        self.enemies_spritesheet = Spritesheet('assets/img/enemy2.png')
        self.terrain_spritesheet = Spritesheet('assets/img/terrain.png')
        self.attack_spritesheet = Spritesheet('assets/img/attack.png')
        self.rats_spritesheet = Spritesheet('assets/img/rats.png')
        self.wildboar_spritesheet = Spritesheet('assets/img/wildboar.png')

        self.question_mark_image = pygame.image.load('assets/img/rat.png')
        self.dt = 0

        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.inventory_open = False

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

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
                    EnemySpawner(self,j,i,10*FPS,5,WildBoar)
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
                    NPC(self, j, i)
                elif column =='R':
                    # EnemySpawner(self,j,i,FPS*1,1,Rat)
                    EnemySpawnerPack(self,j,i,FPS*5,4)
                    Ground(self, j, i)
                elif column =='a':
                    Archer(self,j,i)
                    Ground(self, j, i)
                else:
                    Ground(self, j, i)

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.enemies_attacks = pygame.sprite.LayeredUpdates()
        self.player_group = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
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

                if event.key == pygame.K_e:
                    self.check_interactions()
                
            self.inventory.handle_events(event)
            self.test_add_items(event)

    def update(self):
        self.all_sprites.update()
                
        pygame.display.update()

    def test_add_items(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.inventory.add_test_items(1)
            if event.key == pygame.K_2:
                self.inventory.add_test_items(2)
            if event.key == pygame.K_3:
                self.inventory.add_test_items(3)

    def check_interactions(self):
        for npc in pygame.sprite.spritecollide(self.player, self.npcs, False):
            if npc.talkable:
                npc.initiate_dialogue()


    def draw(self):
        self.camera.update(self.player)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        self.attacks.draw(self.screen)
        self.player.draw_health_bar()

        if self.inventory_open:
            self.inventory.draw_inventory()
            if self.inventory.dragging_item:
                self.inventory.draw_item(
                    self.inventory.dragging_item,
                    pygame.mouse.get_pos()[0] + dragging_offset[0],
                    pygame.mouse.get_pos()[1] + dragging_offset[1]
                )
        pygame.display.flip()
        self.clock.tick(FPS)

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        game_over_screen = GameOverScreen(self.WIN_WIDTH, self.WIN_HEIGHT)
        game_over_screen.show()
        pass
    def intro_screen(self):  
        start_menu = StartMenu (self.WIN_WIDTH, self.WIN_HEIGHT)
        choice = start_menu.show()

        if choice == "start":
            self.new()
            while self.running:
                self.main()
                self.game_over()
        elif choice == "load":
            # Dodaj logikę wczytywania gry
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
