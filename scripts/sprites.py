import pygame

from scripts.config import *
import math
import random
# Wczytywanie grafiki
class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert_alpha()
    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite
# Kamera
class Camera:
    def __init__(self, game, target):
        self.game = game
        self.camera = pygame.Rect(0, 0, self.game.WIN_WIDTH, self.game.WIN_HEIGHT)
        self.target = target

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.game.WIN_WIDTH / 2)
        y = -target.rect.centery + int(self.game.WIN_HEIGHT / 2)

        # Ograniczenie przesunięcia kamery, aby nie wychodziła poza granice mapy
        x = min(0, x)  # Kamery nie przesunięcie się w lewo poza początek mapy
        y = min(0, y)  # Kamery nie przesunięcie się w górę poza początek mapy
        x = max(-(self.game.map_width*32 - self.game.WIN_WIDTH), x)  # Kamery nie przesunięcie się w prawo poza koniec mapy
        y = max(-(self.game.map_height*32 - self.game.WIN_HEIGHT), y)  # Kamery nie przesunięcie się w dół poza koniec mapy

        self.camera = pygame.Rect(x, y, self.game.WIN_WIDTH, self.game.WIN_HEIGHT)

# Gracz
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.gold = 100
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites,self.game.player_group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.hp = 100  # Początkowa wartość HP
        self.attack = 5 # Początkowa wartość ataku
        self.armor = 0 # Początkowa wartość zbroji
        self.immunity_timer = 0


        self.max_hp = 100  # Maksymalna wartość HP
        self.hp_bar_length = 300  # Długość paska HP
        self.hp_color = (0, 255, 0)  # Kolor paska HP (zielony)

        self.invulnerable = False  # Czy gracz jest obecnie nietykalny
        self.invulnerable_duration = 1000  # Okres ochrony w milisekundach (2 sekundy)
        self.invulnerable_timer = 0  # Licznik czasu trwania nietykalności

        self.inventory = []  # Lista przedmiotów w ekwipunku

        self.PLAYER_SPEED = 3

        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.frame_index = 0  # Indeks bieżącej klatki animacji

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.frames = {
            'down': [self.game.character_spritesheet.get_sprite(2, 2, self.width, self.height),
                     self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                     self.game.character_spritesheet.get_sprite(67, 2, self.width, self.height)],
            'up': [self.game.character_spritesheet.get_sprite(2, 2 + 32, self.width, self.height),
                   self.game.character_spritesheet.get_sprite(35, 2 + 32, self.width, self.height),
                   self.game.character_spritesheet.get_sprite(67, 2 + 32, self.width, self.height)],
            'right': [self.game.character_spritesheet.get_sprite(2, 2 + 64, self.width, self.height),
                      self.game.character_spritesheet.get_sprite(35, 2 + 64, self.width, self.height),
                      self.game.character_spritesheet.get_sprite(67, 2 + 64, self.width, self.height)],
            'left': [self.game.character_spritesheet.get_sprite(2, 2 + 96, self.width, self.height),
                     self.game.character_spritesheet.get_sprite(35, 2 + 96, self.width, self.height),
                     self.game.character_spritesheet.get_sprite(67, 2 + 96, self.width, self.height)]
        }

        self.image = self.frames[self.facing][self.frame_index]
        
        self.rect = self.image.get_rect()

        self.rect.height*=0.95
        self.rect.width*=0.95
        self.rect.x = self.x
        self.rect.y = self.y

        self.animation_speed = 200
        self.last_update = 0

    def take_damage(self, damage):
        if self.immunity_timer <= 0:
            if self.armor <damage:
                self.hp -= (damage- self.armor)
                if self.hp <= 0:
                    self.game.game_over()  # Zakończ grę, gdy punkty życia gracza spadną do zera
                else:
                    self.start_immunity(5 * 5)
            else:
                self.hp -= 1
                if self.hp <= 0:
                    self.game.game_over()  # Zakończ grę, gdy punkty życia gracza spadną do zera
                else:
                    self.start_immunity(5 * 5)
    def heal(self, health):
        
        if self.hp < self.max_hp:
            if self.hp + health >= self.max_hp:
                self.hp = self.max_hp
            else:
                self.hp += health
            
    def start_immunity(self, duration):
        self.immunity_timer = duration
        
    def armor_update(self):
        if self.game.inventory.slots[-2]:
            self.game.player.armor = self.game.inventory.slots[-2].armor
        else:
            self.game.player.armor = 0
    def update(self):
        
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0
        self.check_x_keypress()
        self.handle_invulnerability()
        if self.immunity_timer > 0:
            self.immunity_timer -= 1
        self.armor_update()

    def handle_invulnerability(self):
        if self.invulnerable:
            now = pygame.time.get_ticks()
            if now - self.invulnerable_timer >= self.invulnerable_duration:
                self.invulnerable = False  # Zakończ nietykalność po upływie okresu ochrony
    def check_x_keypress(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            if not self.invulnerable:  # Sprawdź, czy gracz nie jest nietykalny
                self.hp -= 10
                self.invulnerable = True  # Ustaw nietykalność po otrzymaniu obrażeń
                self.invulnerable_timer = pygame.time.get_ticks()
    def draw_health_bar(self):
        # Oblicz długość paska HP w zależności od bieżącego stanu HP
        hp_length = int((self.hp / self.max_hp) * self.hp_bar_length)

        # Rysuj pasek HP
        if self.hp <= 0.30 * self.max_hp:
            pygame.draw.rect(self.game.screen, (255, 0, 0), (10, 10, hp_length, 30))
        else:
            pygame.draw.rect(self.game.screen, self.hp_color, (10, 10, hp_length, 30))

        # Rysuj ramkę paska HP
        pygame.draw.rect(self.game.screen, (255, 255, 255), (10, 10, self.hp_bar_length, 30), 2)

        # Dodaj tekst z aktualnym i maksymalnym HP na środku paska
        font = pygame.font.Font(None, 24)
        hp_text = f"{self.hp}/{self.max_hp}"
        text_surface = font.render(hp_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(10 + self.hp_bar_length / 2, 10 + 30 / 2))
        self.game.screen.blit(text_surface, text_rect)
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= self.PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += self.PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= self.PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += self.PLAYER_SPEED
            self.facing = 'down'
    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.facing])
            self.image = self.frames[self.facing][self.frame_index]
    def collide_blocks(self, direction):
        if direction =='x':
            hits = pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.x_change>0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change<0:
                    self.rect.x = hits[0].rect.right
        if direction =='y':
            hits = pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                if self.y_change>0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change<0:
                    self.rect.y = hits[0].rect.bottom

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self._layer = PLAYER_LAYER+1
        self.groups = self.game.attacks,self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    
        
    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            if self.game.inventory.slots[-1]:
                damage = self.game.player.attack + self.game.inventory.slots[-1].dmg
            else:
                damage = self.game.player.attack

            enemy.take_damage(damage)  
        
    def animate(self):
        direction = self.game.player.facing
        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        frame_index = int(self.animation_loop)  # Użyj int() do indeksacji
        if direction == 'up':
            self.image = up_animations[frame_index]
        elif direction == 'down':
            self.image = down_animations[frame_index]
        elif direction == 'left':
            self.image = left_animations[frame_index]
        elif direction == 'right':
            self.image = right_animations[frame_index]

        self.animation_loop += 1/5

        if self.animation_loop >= 5:

            self.kill()

# Bloki
class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960,576,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Wall(pygame.sprite.Sprite):
    def __init__(self,game,x,y,face):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        angle = self.get_angle(face)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(32*31,32*9,self.width,self.height)
        self.image = pygame.transform.rotate(self.image,angle) 
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    def get_angle(self,face):
        if face =='down':
            return 90
        if face =='right':
            return 90*2
        if face =='up':
            return 90*3
        if face =='left':
            return 0

class Ground(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.images = [self.game.terrain_spritesheet.get_sprite(0,352,self.width,self.height),self.game.terrain_spritesheet.get_sprite(32,352,self.width,self.height),self.game.terrain_spritesheet.get_sprite(64,352,self.width,self.height)]

        self.image = self.game.terrain_spritesheet.get_sprite(64,352,self.width,self.height)
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Gate(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        

        self.image = self.game.terrain_spritesheet.get_sprite(32*14,32*12,self.width,self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Field(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(96,608,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Bridge(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(32,416+32+32,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Ground_Water(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(896,96,self.width,self.height)
        self.image = self.game.terrain_spritesheet.get_sprite(896+20,96,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
       
class Water(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer =WATER_LAYER
        self.groups = self.game.all_sprites,self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(896,96,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

        