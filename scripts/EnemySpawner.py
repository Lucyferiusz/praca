import pygame
import random
import math
from scripts.config import *
from scripts.inventory import *

# Attack Class
class MeleeAttackDemon(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target, damage):
        self.game = game
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.target = target
        self.damage = damage

        self._layer = ENEMY_LAYER + 1
        self.groups = self.game.enemies_attacks, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.attack_direction = None  # Nowa zmienna do przechowywania kierunku ataku

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        self.image = self.up_animations[0]  # Początkowy kierunek animacji
        self.rect = pygame.Rect(x, y, self.width, self.height)  # Utwórz rect tutaj

        # Wybierz kierunek ataku względem celu
        self.choose_attack_direction(target)

    def update(self):
        
        self.animate()
        self.check_player_collision()
        

    def choose_attack_direction(self, target):
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery

        if abs(dx) > abs(dy):
            if dx > 0:
                self.attack_direction = 'right'
                self.move_attack_to_position()
            else:
                self.attack_direction = 'left'
                self.move_attack_to_position()
        else:
            if dy > 0:
                self.attack_direction = 'down'
                self.move_attack_to_position()
            else:
                self.attack_direction = 'up'
                self.move_attack_to_position()

        self.set_attack_direction()

    def set_attack_direction(self):
        # Ustaw odpowiednią animację w zależności od kierunku ataku
        if self.attack_direction == 'up':
            self.image = self.up_animations[0]
        elif self.attack_direction == 'down':
            self.image = self.down_animations[0]
        elif self.attack_direction == 'left':
            self.image = self.left_animations[0]
        elif self.attack_direction == 'right':
            self.image = self.right_animations[0]

   
    def animate(self):
        frame_index = int(self.animation_loop)  # Użyj int() do indeksacji

        if self.attack_direction == 'right':
            self.image = self.right_animations[frame_index]
        elif self.attack_direction == 'left':
            self.image = self.left_animations[frame_index]
        elif self.attack_direction == 'down':
            self.image = self.down_animations[frame_index]
        elif self.attack_direction == 'up':
            self.image = self.up_animations[frame_index]

        self.animation_loop += 1/5

        if self.animation_loop >= 5:
            self.kill()
    def move_attack_to_position(self):
        # Przesuń atak na odpowiednią pozycję przed bandytą
        if self.attack_direction == 'up':
            self.rect.y -= TILESIZE
        elif self.attack_direction == 'down':
            self.rect.y += TILESIZE
        elif self.attack_direction == 'left':
            self.rect.x -= TILESIZE
        elif self.attack_direction == 'right':
            self.rect.x += TILESIZE

    def check_player_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        for player in hits:
            player.take_damage(self.damage)
            self.kill()  # Zabij atak po trafieniu gracza
class AttackBandit(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target, damage):
        self.game = game
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.target = target
        self.damage = damage

        self._layer = ENEMY_LAYER + 1
        self.groups = self.game.enemies_attacks, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.attack_direction = None  # Nowa zmienna do przechowywania kierunku ataku

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        self.image = self.up_animations[0]  # Początkowy kierunek animacji
        self.rect = pygame.Rect(x, y, self.width, self.height)  # Utwórz rect tutaj

        # Wybierz kierunek ataku względem celu
        self.choose_attack_direction(target)

    def update(self):
        
        self.animate()
        self.check_player_collision()
        

    def choose_attack_direction(self, target):
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery

        if abs(dx) > abs(dy):
            if dx > 0:
                self.attack_direction = 'right'
                self.move_attack_to_position()
            else:
                self.attack_direction = 'left'
                self.move_attack_to_position()
        else:
            if dy > 0:
                self.attack_direction = 'down'
                self.move_attack_to_position()
            else:
                self.attack_direction = 'up'
                self.move_attack_to_position()

        self.set_attack_direction()

    def set_attack_direction(self):
        # Ustaw odpowiednią animację w zależności od kierunku ataku
        if self.attack_direction == 'up':
            self.image = self.up_animations[0]
        elif self.attack_direction == 'down':
            self.image = self.down_animations[0]
        elif self.attack_direction == 'left':
            self.image = self.left_animations[0]
        elif self.attack_direction == 'right':
            self.image = self.right_animations[0]

   
    def animate(self):
        frame_index = int(self.animation_loop)  # Użyj int() do indeksacji

        if self.attack_direction == 'right':
            self.image = self.right_animations[frame_index]
        elif self.attack_direction == 'left':
            self.image = self.left_animations[frame_index]
        elif self.attack_direction == 'down':
            self.image = self.down_animations[frame_index]
        elif self.attack_direction == 'up':
            self.image = self.up_animations[frame_index]

        self.animation_loop += 1/5

        if self.animation_loop >= 5:
            self.kill()
    def move_attack_to_position(self):
        # Przesuń atak na odpowiednią pozycję przed bandytą
        if self.attack_direction == 'up':
            self.rect.y -= TILESIZE
        elif self.attack_direction == 'down':
            self.rect.y += TILESIZE
        elif self.attack_direction == 'left':
            self.rect.x -= TILESIZE
        elif self.attack_direction == 'right':
            self.rect.x += TILESIZE

    def check_player_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        for player in hits:
            player.take_damage(self.damage)
            self.kill()  # Zabij atak po trafieniu gracza

class AttackArcher(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target, damage):
        self.game = game
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.target = target
        self.damage = damage

        self._layer = ENEMY_LAYER + 1
        self.groups = self.game.enemies_attacks, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Oblicz kierunek ataku na podstawie pozycji gracza
        self.direction = self.calculate_direction()
        self.distance_travelled = 0

    def update(self):
        self.move()
        self.check_player_collision()
        self.check_disappear()

    def move(self):
        # Przesuń atak w kierunku gracza
        self.rect.x += self.direction[0] * TILESIZE/4
        self.rect.y += self.direction[1] * TILESIZE/4

        self.distance_travelled += TILESIZE/4

    def calculate_direction(self):
        # Oblicz kierunek ataku na podstawie pozycji gracza
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            return (dx / distance, dy / distance)
        else:
            return (0, 0)

    def check_player_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        for player in hits:
            player.take_damage(self.damage)
            self.kill()

    def check_disappear(self):
        # Znikaj po przebyciu 6 kratek od początkowej pozycji gracza
        if self.distance_travelled >= 6 * TILESIZE:
            self.kill()

class RangedAttackDemon(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target, damage):
        self.game = game
        self.x = x
        self.y = y
        self.width = TILESIZE // 2
        self.height = TILESIZE // 2
        self.target = target
        self.damage = damage

        self._layer = ENEMY_LAYER + 1
        self.groups = self.game.enemies_attacks, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        self.image.fill((255, 0, 0))  # Czerwony kolor, dostosuj według potrzeb
        self.rect = pygame.Rect(x, y, self.width, self.height)
        

        # Oblicz kierunek ataku na podstawie pozycji gracza
        self.direction = self.calculate_direction()

        self.distance_travelled = 0

    def update(self):
        self.move()
        self.check_player_collision()
        self.check_disappear()

    def move(self):
        # Przesuń atak w kierunku gracza
        self.rect.x += self.direction[0] * TILESIZE/4
        self.rect.y += self.direction[1] * TILESIZE/4

        # Aktualizuj odległość przebytą
        self.distance_travelled += TILESIZE/4

    def calculate_direction(self):
        # Oblicz kierunek ataku na podstawie pozycji gracza
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            return (dx / distance, dy / distance)
        else:
            return (0, 0)

    def check_player_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        for player in hits:
            player.take_damage(self.damage)
            self.kill()

    def check_disappear(self):
        # Znikaj po przebyciu 6 kratek od początkowej pozycji gracza
        if self.distance_travelled >= 6 * TILESIZE:
            self.kill()
class AttackMage(pygame.sprite.Sprite):
    def __init__(self, game, x, y, target, damage):
        self.game = game
        self.x = x
        self.y = y
        self.width = TILESIZE // 2
        self.height = TILESIZE // 2
        self.target = target
        self.damage = damage

        self._layer = ENEMY_LAYER + 1
        self.groups = self.game.enemies_attacks, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        self.image.fill((255, 0, 0))  # Czerwony kolor, dostosuj według potrzeb
        self.rect = pygame.Rect(x, y, self.width, self.height)
        

        # Oblicz kierunek ataku na podstawie pozycji gracza
        self.direction = self.calculate_direction()

        self.distance_travelled = 0

    def update(self):
        self.move()
        self.check_player_collision()
        self.check_disappear()

    def move(self):
        # Przesuń atak w kierunku gracza
        self.rect.x += self.direction[0] * TILESIZE/4
        self.rect.y += self.direction[1] * TILESIZE/4

        # Aktualizuj odległość przebytą
        self.distance_travelled += TILESIZE/4

    def calculate_direction(self):
        # Oblicz kierunek ataku na podstawie pozycji gracza
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            return (dx / distance, dy / distance)
        else:
            return (0, 0)

    def check_player_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.player_group, False)
        for player in hits:
            player.take_damage(self.damage)
            self.kill()

    def check_disappear(self):
        # Znikaj po przebyciu 6 kratek od początkowej pozycji gracza
        if self.distance_travelled >= 6 * TILESIZE:
            self.kill()

class MageHealAttack(pygame.sprite.Sprite):
    def __init__(self, game, mage, heal_amount):
        self.game = game
        self.mage = mage
        self.width = TILESIZE
        self.height = TILESIZE
        self.heal_amount = heal_amount

        self.target = pygame.Rect(0,0,0,0)

        self._layer = ENEMY_LAYER + 1
        self.groups = self.game.enemies_attacks, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.choose_random_enemy()


        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((0, 255, 0))  # Zielony kolor dla leczenia, dostosuj według potrzeb
        self.rect = pygame.Rect(self.target.x,self.target.y, self.width, self.height)

        
        self.distance_travelled = 0

            
    def choose_random_enemy(self):
        enemies_in_radius = [enemy for enemy in self.game.enemies ]
            
        enemies_in_radius.remove(self.mage)
        
        if enemies_in_radius:
            for e in enemies_in_radius:
                distance_to_mage = math.sqrt((e.rect.x - self.mage.rect.x) ** 2 + (e.rect.y - self.mage.rect.y) ** 2)
                if distance_to_mage>=3*TILESIZE:
                    enemies_in_radius.remove(e)

        if not enemies_in_radius:
            self.kill()
            return

        self.target = random.choice(enemies_in_radius)
        
        

   

    def check_enemy_collision(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            enemy.heal(self.heal_amount)
            self.kill()

    def update(self):
        self.check_enemy_collision()
        self.check_disappear()
        

    def check_disappear(self):
        if self.distance_travelled >= 6 * TILESIZE:
            self.kill()
            
            
# Enemy Class
            
class DamageAnimation(pygame.sprite.Sprite):
    def __init__(self, target, damage):
        super().__init__()
        self._layer = ENEMY_LAYER
        self.target = target
        self.damage = damage
        self.duration = 60  # Czas trwania animacji w klatkach
        self.create_image()

    def update(self):
        if self.target is not None:
            self.rect.center = self.target.rect.center
        self.duration -= 1

    def is_active(self):
        return self.duration > 0

    def create_image(self):
        # Utwórz powierzchnię animacji z przezroczystością
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)

        # Kopiuj kanał alfa z oryginalnego obrazu target
        self.image.fill((255, 0, 0, 128))  # Wypełnij czerwoną barwą, zachowując oryginalny kanał alfa

        # Utwórz maskę kolizji na podstawie nieprzezroczystych obszarów obrazu
        mask_surface = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        mask_surface.fill((255, 0,0))  # Ustaw kolor biały dla obszarów, które mają być uwzględnione w masce
        mask_surface.blit(self.target.image.convert_alpha(), (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.mask = pygame.mask.from_surface(mask_surface)
        self.image = mask_surface
        

        # Ustaw pozycję animacji na środek celu
        if self.target is not None:
            self.rect = self.image.get_rect(center=self.target.rect.center)
        else:
            self.rect = self.image.get_rect()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x_change = 0
        self.y_change = 0
        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.max_travel = random.randint(3 * TILESIZE, 5 * TILESIZE)
        self.movement_loop = 0

        self.hp = 50
        self.max_hp = self.hp
        self.speed = 1

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.archer_spritesheet.get_sprite(2, 3 + 128, self.width, self.height)

        self.immunity_timer = 0
        self.damage_animation = None

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def heal(self, amount):
        # Increase the enemy's health points when healed
        self.hp += amount

        # Ensure that the enemy's health points do not exceed the maximum
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    def drop_loot(self):
       pass
    def take_damage(self, damage):
        if not self.damage_animation:
            self.hp -= damage
            self.show_damage_animation()
            if self.hp <= 0:
                self.damage_animation.kill()
                self.drop_loot()
                self.kill()
                
            

    def start_immunity(self, duration):
        self.image_org = self.image.copy()
        self.immunity_timer = duration

    def show_damage_animation(self):
        self.damage_animation = DamageAnimation(self, damage=10)  # Przykładowe obrażenia (zmień na właściwe)
        self.game.all_sprites.add(self.damage_animation)
        



    def update_damage_animation(self):
        if self.damage_animation:
            self.damage_animation.update()
            if not self.damage_animation.is_active():
                self.damage_animation.kill()
                self.damage_animation = None

    def update(self):
        self.movement()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0

        self.update_damage_animation()


    def movement(self):
        player = self.game.player
        distance_to_player = math.sqrt((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2)

        if distance_to_player < 1 * TILESIZE / 2:
            self.x_change += self.speed if self.rect.x > self.game.player.rect.x else -self.speed
            self.y_change += self.speed if self.rect.y > self.game.player.rect.y else -self.speed
        elif distance_to_player <= 5 * TILESIZE:
            angle = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
            self.x_change = self.speed * math.cos(angle)
            self.y_change = self.speed * math.sin(angle)
        else:
            if self.facing == 'left':
                self.x_change -= self.speed
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = random.choice(['right', 'up', 'down'])
                    self.movement_loop = 0
            if self.facing == 'right':
                self.x_change += self.speed
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = random.choice(['left', 'up', 'down'])
                    self.movement_loop = 0
            if self.facing == 'up':
                self.y_change -= self.speed
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = random.choice(['left', 'right', 'down'])
                    self.movement_loop = 0
            if self.facing == 'down':
                self.y_change += self.speed
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = random.choice(['left', 'up', 'right'])
                    self.movement_loop = 0

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width

                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height

                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

class Rat(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # Dodaj nowe właściwości dotyczące ataku
        self.attack_range = TILESIZE * 0.5  # Zakres ataku w pikselach
        self.attack_damage = 4  # Obrażenia zadawane przez atak
        self.attack_cooldown = 60*2  # Cooldown ataku w klatkach
        self.attack_timer = 0  # Licznik czasu od ostatniego ataku
        self.image = self.game.rats_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.hp = 25
        self.max_hp = self.hp

        self.enemy_type = "Rat"
    def drop_loot(self):
        # Szansa 10% na skórę od szczura
        if random.randint(1, 10) == 1:
            loot_item = self.game.all_items['lether'].new()
            self.game.inventory.add_item(loot_item)
            self.game.inventory.count_lether +=1
            self.game.quest_log.update(self.game.player, item="lether")
        xp_amount = 5
        self.game.player.gain_xp(xp_amount)
        
    def update(self):
        super().update()
        self.attack_timer += 1

        # Sprawdź, czy gracz jest wystarczająco blisko i czy minął czas od ostatniego ataku
        if self.distance_to_player() <= self.attack_range and self.attack_timer >= self.attack_cooldown:
            self.attack_player()

    def kill(self) -> None:
        super().kill()
        self.game.quest_log.update(self.game.player, enemy_type=self.enemy_type)

    def attack_player(self):
        # Zadaj obrażenia graczowi
        self.game.player.take_damage(self.attack_damage)
        # Zresetuj licznik czasu ataku
        self.attack_timer = 0

    def distance_to_player(self):
        # Oblicz odległość do gracza
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
        return math.sqrt(dx**2 + dy**2)

class WildBoar(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # właściwości dotyczące ataku
        self.hp = 50
        self.max_hp = self.hp

        self.enemy_type = "WildBoar"

        self.attack_range = TILESIZE * 1  # Zakres ataku w pikselach
        self.attack_damage = 15  # Obrażenia zadawane przez atak
        self.attack_cooldown = 60*1  # Cooldown ataku w klatkach
        self.attack_timer = 0  # Licznik czasu od ostatniego ataku
        self.image = self.game.wildboar_spritesheet.get_sprite(0, 0, self.width, self.height)


        self.charge_speed_multiplier = 1.5  # Mnożnik prędkości podczas szarży
        self.charge_cooldown = 500  # Czas odnowienia (w milisekundach) między kolejnymi szarżami
        self.last_charge_time = pygame.time.get_ticks()
        self.charging = False 
    def drop_loot(self):
        # Szansa 10% na skórę od dzika
        if random.randint(1, 100) <= 100:
            loot_item = self.game.all_items['lether'].new()
            self.game.inventory.add_item(loot_item)
            self.game.inventory.count_lether +=1
            self.game.quest_log.update(self.game.player, item="lether")
        xp_amount = 10
        self.game.player.gain_xp(xp_amount)

    def update(self):
        super().update()
        self.attack_timer += 1

        # Sprawdź, czy gracz jest wystarczająco blisko i czy minął czas od ostatniego ataku
        if self.distance_to_player() <= self.attack_range and self.attack_timer >= self.attack_cooldown:
            self.attack_player()
        # Dodajmy obsługę szarży
        now = pygame.time.get_ticks()
        if now - self.last_charge_time > self.charge_cooldown:
            # Sprawdzamy, czy dzik jest w pobliżu gracza (możesz dostosować zasięg)
            if pygame.sprite.collide_rect(self, self.game.player):
                self.charge()
                self.last_charge_time = now

    def charge(self):
        player_distance = math.sqrt((self.rect.x - self.game.player.rect.x) ** 2 +
                                    (self.rect.y - self.game.player.rect.y) ** 2)
        

        

        if not self.charging and player_distance >= 2.5 * TILESIZE:
            self.charging = True  # Rozpocznij szarżę tylko jeżeli dzik nie jest w trakcie szarży i jest wystarczająco daleko od gracza
            self.charge_start_pos = (self.rect.x, self.rect.y)  # Zachowaj pozycję startową
            self.speed *= self.charge_speed_multiplier
        elif self.charging:
            self.rect.x += self.x_change
            self.collide_blocks('x')
            self.rect.y += self.y_change
            self.collide_blocks('y')

            # Sprawdź kolizję z graczem
            if self.rect.colliderect(self.game.player.rect):
                self.game.player.take_damage(10)  # Zadaj obrażenia graczowi
                self.end_charge()

            # Sprawdź odległość od pozycji startowej, aby zakończyć szarżę
            distance_from_start = math.sqrt((self.rect.x - self.charge_start_pos[0]) ** 2 +
                                            (self.rect.y - self.charge_start_pos[1]) ** 2)

            if distance_from_start >= 4 * TILESIZE:
                self.end_charge()
    def kill(self) -> None:
        super().kill()
        self.game.quest_log.update(self.game.player, enemy_type=self.enemy_type)

    def end_charge(self):
        self.charging = False
        self.speed /= self.charge_speed_multiplier  # Przywróć normalną prędkość po zakończeniu szarży

    def attack_player(self):
        # Zadaj obrażenia graczowi
        self.game.player.take_damage(self.attack_damage)
        # Zresetuj licznik czasu ataku
        self.attack_timer = 0

    def distance_to_player(self):
        # Oblicz odległość do gracza
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
        return math.sqrt(dx**2 + dy**2)

class Archer(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.hp = 35
        self.max_hp = self.hp

        self.enemy_type = "Archer"

        self.speed = 0.90
        self.image = self.game.archer_spritesheet.get_sprite(2, 2, self.width, self.height)
        self.max_travel = 5*TILESIZE

        self.shoot_frequency = 60*6
        self.shoot_timer = random.randint(0, self.shoot_frequency)
        self.attacks = pygame.sprite.Group()


        self.facing = 'down'
        self.frame_index = 0  # Indeks bieżącej klatki animacji
        self.animation_speed = 200
        self.last_update = 0

        self.frames = {
            'down': [self.game.archer_spritesheet.get_sprite(2, 2, self.width, self.height),
                     self.game.archer_spritesheet.get_sprite(35, 2, self.width, self.height),
                     self.game.archer_spritesheet.get_sprite(67, 2, self.width, self.height)],
            'up': [self.game.archer_spritesheet.get_sprite(2, 2 + 32, self.width, self.height),
                   self.game.archer_spritesheet.get_sprite(35, 2 + 32, self.width, self.height),
                   self.game.archer_spritesheet.get_sprite(67, 2 + 32, self.width, self.height)],
            'right': [self.game.archer_spritesheet.get_sprite(2, 2 + 64, self.width, self.height),
                      self.game.archer_spritesheet.get_sprite(35, 2 + 64, self.width, self.height),
                      self.game.archer_spritesheet.get_sprite(67, 2 + 64, self.width, self.height)],
            'left': [self.game.archer_spritesheet.get_sprite(2, 2 + 96, self.width, self.height),
                     self.game.archer_spritesheet.get_sprite(35, 2 + 96, self.width, self.height),
                     self.game.archer_spritesheet.get_sprite(67, 2 + 96, self.width, self.height)]
        }
        self.image = self.frames[self.facing][self.frame_index]

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.facing])
            self.image = self.frames[self.facing][self.frame_index]
    



    def movement(self):
        player_distance = math.sqrt((self.rect.x - self.game.player.rect.x) ** 2 +
                                    (self.rect.y - self.game.player.rect.y) ** 2)

        if player_distance < 3 * TILESIZE:
            # Gracz jest zbyt blisko, więc oddal się od gracza
            self.x_change += self.speed  if self.rect.x > self.game.player.rect.x else -self.speed
            self.y_change += self.speed  if self.rect.y > self.game.player.rect.y else -self.speed 

        else:
            # Gracz jest wystarczająco daleko, więc utrzymuj dystans
            if self.facing == 'left':
                self.x_change -= self.speed
            elif self.facing == 'right':
                self.x_change += self.speed
            elif self.facing == 'up':
                self.y_change -= self.speed
            elif self.facing == 'down':
                self.y_change += self.speed

            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left', 'right', 'up', 'down'])
                self.movement_loop = 0  

    def shoot(self):
        attack = AttackArcher(self.game, self.rect.x, self.rect.y, self.game.player, damage=10)
        self.attacks.add(attack)

    def check_attack_collision(self):
        hits = pygame.sprite.spritecollide(self.game.player, self.attacks, True)
        for hit in hits:
            self.game.player.take_damage(hit.damage)
    def drop_loot(self):
        # Gold w przedziale od 3 do 7
        gold_amount = random.randint(3, 7)
        self.game.player.gold += gold_amount


        # Skradziona biżuteria z 15% szansą
        if random.randint(1, 100) <= 100:
            loot_item = self.game.all_items['jewellery'].new()
            self.game.inventory.add_item(loot_item)
            # self.game.inventory.count_jewellery +=1
            self.game.quest_log.update(self.game.player, item="jewellery")
    

        # Strzały z 50% szansą
        if random.randint(1, 100) <= 50:
            loot_item = self.game.all_items['arrow'].new()
            self.game.inventory.add_item(loot_item)
            self.game.inventory.count_arrow +=1
            self.game.quest_log.update(self.game.player, item="arrow")
    
        xp_amount = 15
        self.game.player.gain_xp(xp_amount)


    def kill(self) -> None:
        super().kill()
        self.game.quest_log.update(self.game.player, enemy_type=self.enemy_type)


    def update(self):
        super().update()
        
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = self.shoot_frequency

        self.attacks.update()
        self.check_attack_collision()
        self.animate()
    
class Bandit(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.bandit_spritesheet.get_sprite(6, 9, self.width, self.height)
        self.hp = 50
        self.max_hp = self.hp

        self.attack_range = TILESIZE * 1  # Zakres ataku w pikselach
        self.attack_damage = 10  # Obrażenia zadawane przez atak
        self.attack_cooldown = 60  # Cooldown ataku w klatkach
        self.attack_timer = 0  # Licznik czasu od ostatniego ataku

        self.facing = 'down'
        self.frame_index = 0  # Indeks bieżącej klatki animacji
        self.animation_speed = 200
        self.last_update = 0

        self.enemy_type = "Bandit"

        self.frames = {
            'down': [self.game.bandit_spritesheet.get_sprite(2, 2, self.width, self.height),
                     self.game.bandit_spritesheet.get_sprite(35, 2, self.width, self.height),
                     self.game.bandit_spritesheet.get_sprite(67, 2, self.width, self.height)],
            'up': [self.game.bandit_spritesheet.get_sprite(2, 2 + 32, self.width, self.height),
                   self.game.bandit_spritesheet.get_sprite(35, 2 + 32, self.width, self.height),
                   self.game.bandit_spritesheet.get_sprite(67, 2 + 32, self.width, self.height)],
            'right': [self.game.bandit_spritesheet.get_sprite(2, 2 + 64, self.width, self.height),
                      self.game.bandit_spritesheet.get_sprite(35, 2 + 64, self.width, self.height),
                      self.game.bandit_spritesheet.get_sprite(67, 2 + 64, self.width, self.height)],
            'left': [self.game.bandit_spritesheet.get_sprite(2, 2 + 96, self.width, self.height),
                     self.game.bandit_spritesheet.get_sprite(35, 2 + 96, self.width, self.height),
                     self.game.bandit_spritesheet.get_sprite(67, 2 + 96, self.width, self.height)]
        }
        self.image = self.frames[self.facing][self.frame_index]

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.facing])
            self.image = self.frames[self.facing][self.frame_index]
    
    def movement(self):
        self.player_distance = math.sqrt((self.rect.x - self.game.player.rect.x) ** 2 +
                                    (self.rect.y - self.game.player.rect.y) ** 2)

        
        
        if self.player_distance <=1 * TILESIZE:
            
            self.x_change += 0
            self.y_change += 0
        
        elif self.player_distance < 4 * TILESIZE:
            
            self.x_change += -self.speed  if self.rect.x > self.game.player.rect.x else self.speed
            self.y_change += -self.speed  if self.rect.y > self.game.player.rect.y else self.speed 
        

        else:
            # Gracz jest wystarczająco daleko, więc utrzymuj dystans
            if self.facing == 'left':
                self.x_change -= self.speed
            elif self.facing == 'right':
                self.x_change += self.speed
            elif self.facing == 'up':
                self.y_change -= self.speed
            elif self.facing == 'down':
                self.y_change += self.speed

            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left', 'right', 'up', 'down'])
                self.movement_loop = 0
    def drop_loot(self):
        # Gold w przedziale od 5 do 10
        gold_amount = random.randint(5, 10)
        self.game.player.gold += gold_amount

        # Skradziona biżuteria z 20% szansą
        if random.randint(1, 100) <= 20:
            loot_item = self.game.all_items['jewellery'].new()
            self.game.inventory.add_item(loot_item)
            self.game.inventory.count_jewellery +=1
            self.game.quest_log.update(self.game.player, item="jewellery")
            
            

        # Złamany sztylet z 10% szansą
        if random.randint(1, 100) <= 10:
            loot_item = self.game.all_items['broken_dagger'].new()
            self.game.inventory.add_item(loot_item)
            self.game.inventory.count_broken_dagger +=1
            self.game.quest_log.update(self.game.player, item="broken_dagger")
            
        # XP za pokonanie bandyty
        xp_amount = 20
        self.game.player.gain_xp(xp_amount)
        
    def kill(self) -> None:
        super().kill()
        self.game.quest_log.update(self.game.player, enemy_type=self.enemy_type)    
    def update(self):
        super().update()
        self.attack_timer += 1

        # Sprawdź, czy gracz jest wystarczająco blisko i czy minął czas od ostatniego ataku
        if self.player_distance <= self.attack_range and self.attack_timer >= self.attack_cooldown:
            self.attack_player()
        self.animate()

    def attack_player(self):
            # Stwórz atak wroga skierowany w stronę gracza
            attack = AttackBandit(self.game, self.rect.x, self.rect.y, self.game.player, self.attack_damage)
            self.game.all_sprites.add(attack)
            self.game.attacks.add(attack)
            # Zresetuj licznik czasu ataku
            self.attack_timer = 0
            
class Mage(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.mage_spritesheet.get_sprite(4, 6, self.width, self.height)
        self.hp = 30
        self.max_hp = self.hp
        self.enemy_type = "Mage"

        self.distance_to_player = 4 * TILESIZE
        self.min_distance_to_player = 3 * TILESIZE  # Minimalna odległość, przy której zaczniemy się oddalać
        self.attack_cooldown = 0
        self.attack_cooldown_max = 60  *10

        self.heal_cooldown = 0
        self.heal_cooldown_max = 300  # Example cooldown time for the healing ability

        self.attacks = pygame.sprite.Group()

        self.facing = 'down'
        self.frame_index = 0  # Indeks bieżącej klatki animacji
        self.animation_speed = 200
        self.last_update = 0

        self.frames = {
            'down': [self.game.mage_spritesheet.get_sprite(2, 2, self.width, self.height),
                     self.game.mage_spritesheet.get_sprite(35, 2, self.width, self.height),
                     self.game.mage_spritesheet.get_sprite(67, 2, self.width, self.height)],
            'up': [self.game.mage_spritesheet.get_sprite(2, 2 + 32, self.width, self.height),
                   self.game.mage_spritesheet.get_sprite(35, 2 + 32, self.width, self.height),
                   self.game.mage_spritesheet.get_sprite(67, 2 + 32, self.width, self.height)],
            'right': [self.game.mage_spritesheet.get_sprite(2, 2 + 64, self.width, self.height),
                      self.game.mage_spritesheet.get_sprite(35, 2 + 64, self.width, self.height),
                      self.game.mage_spritesheet.get_sprite(67, 2 + 64, self.width, self.height)],
            'left': [self.game.mage_spritesheet.get_sprite(2, 2 + 96, self.width, self.height),
                     self.game.mage_spritesheet.get_sprite(35, 2 + 96, self.width, self.height),
                     self.game.mage_spritesheet.get_sprite(67, 2 + 96, self.width, self.height)]
        }
        self.image = self.frames[self.facing][self.frame_index]

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.facing])
            self.image = self.frames[self.facing][self.frame_index]
    def drop_loot(self):
        # Gold w przedziale od 7 do 15
        gold_amount = random.randint(7, 15)
        self.game.player.gold += gold_amount

        # Księga czarów z 10% szansą
        if random.randint(1, 10) == 1:
            loot_item = self.game.all_items['book'].new()
            self.game.inventory.add_item(loot_item)
            self.game.inventory.count_book +=1
            self.game.quest_log.update(self.game.player, item="book")
        xp_amount = 30
        self.game.player.gain_xp(xp_amount)
    def update(self):
        super().update()
        
        if self.attack_cooldown <= 0:
            self.attack_cooldown = self.attack_cooldown_max
            self.choose_random_attack()
        else:
            self.attack_cooldown -= 1
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        
            

        self.check_attack_collision()
        self.animate()

    def movement(self):
        player = self.game.player
        distance_to_player = pygame.math.Vector2(player.rect.centerx - self.rect.centerx,
                                                player.rect.centery - self.rect.centery).length()

        if distance_to_player < self.min_distance_to_player:
            # Jeśli jesteśmy wystarczająco blisko, zacznij się oddalać
            angle = math.atan2(self.rect.y - player.rect.y, self.rect.x - player.rect.x)
            self.x_change = self.speed * math.cos(angle)
            self.y_change = self.speed * math.sin(angle)

            # Ustal kierunek, w którym patrzy wróg na podstawie ruchu
            if abs(self.x_change) > abs(self.y_change):
                if self.x_change > 0:
                    self.facing = 'left'
                else:
                    self.facing = 'right'
            else:
                if self.y_change > 0:
                    self.facing = 'up'
                else:
                    self.facing = 'down'
        elif distance_to_player < self.distance_to_player:
            # Jeśli jesteśmy w przedziale odległości, zatrzymaj się
            self.x_change = 0
            self.y_change = 0
        elif distance_to_player < self.distance_to_player+1:
            # W przeciwnym razie poruszaj się w kierunku gracza
            angle = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
            self.x_change = self.speed * math.cos(angle)
            self.y_change = self.speed * math.sin(angle)

            # Ustal kierunek, w którym patrzy wróg na podstawie ruchu
            if abs(self.x_change) > abs(self.y_change):
                if self.x_change > 0:
                    self.facing = 'right'
                else:
                    self.facing = 'left'
            else:
                if self.y_change > 0:
                    self.facing = 'down'
                else:
                    self.facing = 'up'
        else:
            # Gracz jest wystarczająco daleko, więc utrzymuj dystans
            if self.facing == 'left':
                self.x_change -= self.speed
            elif self.facing == 'right':
                self.x_change += self.speed
            elif self.facing == 'up':
                self.y_change -= self.speed
            elif self.facing == 'down':
                self.y_change += self.speed

            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left', 'right', 'up', 'down'])
                self.movement_loop = 0
    def choose_random_attack(self):
        # Losowo wybierz atak
        # possible_attacks = ['heal','normal_attack']
        chosen_attack = None
        chance = random.randint(1,100)
        if chance <= 10:
            chosen_attack = "heal"
        else:
            chosen_attack= "normal_attack"

        if chosen_attack == 'heal':
            self.heal_ability()
        elif chosen_attack == 'normal_attack':
            self.attack()
    def choose_target(self):
        # Find the nearest enemy to the mage
        enemies = [enemy for enemy in self.game.enemies if isinstance(enemy, Enemy)]
        enemies.remove(self)
        if enemies:
            target = min(enemies, key=lambda enemy: pygame.math.Vector2(enemy.rect.centerx - self.rect.centerx,
                                                                        enemy.rect.centery - self.rect.centery).length())
            return target
        else:
            return None
        
    def heal_ability(self):
        # Check if healing ability is off cooldown
        if self.heal_cooldown <= 0:
            # Create an instance of MageHealAttack to perform the healing attack
            heal_attack = MageHealAttack(self.game, self, heal_amount=10)
            self.game.enemies_attacks.add(heal_attack)
            # Reset the cooldown
            self.heal_cooldown = self.heal_cooldown_max
    def kill(self) -> None:
        super().kill()
        self.game.quest_log.update(self.game.player, enemy_type=self.enemy_type)

    def attack(self):
        # Logika ataku dystansowego maga
        attack = AttackMage(self.game, self.rect.x, self.rect.y,self.game.player,damage = 10)
        self.game.enemies_attacks.add(attack)

    def area_attack(self):
        # Logika obszarowego ataku maga
        pass
    def check_attack_collision(self):
        hits = pygame.sprite.spritecollide(self.game.player, self.attacks, True)
        for hit in hits:
            self.game.player.take_damage(hit.damage)

class Demon(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.demon_spritesheet.get_sprite(10, 15, self.width, self.height)
        self.hp = 1#500
        self.max_hp = self.hp
        self.enemy_type = "Demon"

        self.distance_to_player = 5 * TILESIZE
        self.min_distance_to_player = 3 * TILESIZE
        self.attack_cooldown_melee = 0
        self.attack_cooldown_range = 0
        self.attack_cooldown_max = 60 * 1.5
        self.attack_cooldown_max2 = 60 * 3

        self.attacks = pygame.sprite.Group()

        self.attack_timer_melee = 60*1.5
        self.attack_timer_range = 60*1
        self.facing = 'down'
        self.frame_index = 0
        self.animation_speed = 200
        self.last_update = 0

        self.attack_range = 4

        self.frames = {
            'down': [self.game.demon_spritesheet.get_sprite(2, 2, self.width, self.height),
                     self.game.demon_spritesheet.get_sprite(35, 2, self.width, self.height),
                     self.game.demon_spritesheet.get_sprite(67, 2, self.width, self.height)],
            'up': [self.game.demon_spritesheet.get_sprite(2, 2 + 32, self.width, self.height),
                   self.game.demon_spritesheet.get_sprite(35, 2 + 32, self.width, self.height),
                   self.game.demon_spritesheet.get_sprite(67, 2 + 32, self.width, self.height)],
            'right': [self.game.demon_spritesheet.get_sprite(2, 2 + 64, self.width, self.height),
                      self.game.demon_spritesheet.get_sprite(35, 2 + 64, self.width, self.height),
                      self.game.demon_spritesheet.get_sprite(67, 2 + 64, self.width, self.height)],
            'left': [self.game.demon_spritesheet.get_sprite(2, 2 + 96, self.width, self.height),
                     self.game.demon_spritesheet.get_sprite(35, 2 + 96, self.width, self.height),
                     self.game.demon_spritesheet.get_sprite(67, 2 + 96, self.width, self.height)]
        }
        self.image = self.frames[self.facing][self.frame_index]

    def melee_attack_player(self):
        if self.player_distance <= 1.5 * TILESIZE:
            melee_attack = MeleeAttackDemon(self.game, self.rect.x, self.rect.y, self.game.player, damage=15)
            self.game.enemies_attacks.add(melee_attack)

    def range_attack_player(self):
        if self.player_distance >= 3 * TILESIZE:
            ranged_attack = RangedAttackDemon(self.game, self.rect.x, self.rect.y, self.game.player, damage=10)
            self.game.enemies_attacks.add(ranged_attack)

    def check_attack_collision(self):
        # Add demon-specific attack collision logic here
        pass

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.facing])
            self.image = self.frames[self.facing][self.frame_index]

    def drop_loot(self):
        gold_amount = random.randint(7, 15)
        self.game.player.gold += gold_amount

    
        loot_item = self.game.all_items['skull'].new()
        self.game.inventory.add_item(loot_item)
        self.game.inventory.count_book += 1
        self.game.quest_log.update(self.game.player, item="skull")
        xp_amount = 3000
        self.game.player.gain_xp(xp_amount)

    def kill(self) -> None:
        super().kill()
        self.game.quest_log.update(self.game.player, enemy_type=self.enemy_type)

    def update(self):
        super().update()
        self.player_distance = pygame.math.Vector2(self.game.player.rect.centerx - self.rect.centerx,
                                                   self.game.player.rect.centery - self.rect.centery).length()

        if self.attack_timer_melee <= 0 and self.player_distance <= 1.5 * TILESIZE:
            self.melee_attack_player()
            self.attack_timer_melee = self.attack_cooldown_melee

        # Corrected the attribute name here
        if self.attack_timer_range <= 0 and self.player_distance > 3 * TILESIZE:
            self.range_attack_player()
            self.attack_timer_range = self.attack_cooldown_range  # Use attack_cooldown_range here

        self.attack_timer_melee -= 1
        # Corrected the attribute name here
        self.attack_timer_range -= 1

        if self.attack_cooldown_melee <= 0:
            self.attack_cooldown_melee = self.attack_cooldown_max
        if self.attack_cooldown_range <= 0:
            self.attack_cooldown_range = self.attack_cooldown_max2

        self.check_attack_collision()
        self.animate()
    def movement(self):
        player = self.game.player
        distance_to_player = pygame.math.Vector2(player.rect.centerx - self.rect.centerx,
                                                player.rect.centery - self.rect.centery).length()

        if distance_to_player < self.min_distance_to_player:
            angle = math.atan2(self.rect.y - player.rect.y, self.rect.x - player.rect.x)
            self.x_change = self.speed * math.cos(angle)
            self.y_change = self.speed * math.sin(angle)

            if abs(self.x_change) > abs(self.y_change):
                if self.x_change > 0:
                    self.facing = 'left'
                else:
                    self.facing = 'right'
            else:
                if self.y_change > 0:
                    self.facing = 'up'
                else:
                    self.facing = 'down'
        elif distance_to_player < self.distance_to_player:
            self.x_change = 0
            self.y_change = 0
        elif distance_to_player < self.distance_to_player + 1:
            angle = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
            self.x_change = self.speed * math.cos(angle)
            self.y_change = self.speed * math.sin(angle)

            if abs(self.x_change) > abs(self.y_change):
                if self.x_change > 0:
                    self.facing = 'right'
                else:
                    self.facing = 'left'
            else:
                if self.y_change > 0:
                    self.facing = 'down'
                else:
                    self.facing = 'up'
        else:
            if self.facing == 'left':
                self.x_change -= self.speed
            elif self.facing == 'right':
                self.x_change += self.speed
            elif self.facing == 'up':
                self.y_change -= self.speed
            elif self.facing == 'down':
                self.y_change += self.speed

            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left', 'right', 'up', 'down'])
                self.movement_loop = 0




# Spawner Class
class EnemySpawner(pygame.sprite.Sprite):
    def __init__(self, game, x, y, spawn_rate, max_spawn, enemy_class):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        

        self.x_spawn=x
        self.y_spawn=y
        
        self.spawn_rate = spawn_rate  # Określa, co ile klatek pojawi się nowy przeciwnik
        self.spawn_timer = 0
        self.max_spawn = max_spawn  # Maksymalna liczba przeciwników jednocześnie
        self.enemy_class = enemy_class
        self.spawned_enemies = pygame.sprite.Group()  # Grupa do śledzenia spawned enemies
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def update(self):
        # Zliczaj klatki
        self.spawn_timer += 1
        # Sprawdź, czy przyszedł czas na stworzenie nowego przeciwnika
        if self.spawn_timer >= self.spawn_rate and len(self.spawned_enemies) < self.max_spawn:
            
                        
            # Stwórz nowego przeciwnika i ustaw go w losowym miejscu wokół spawnera
            enemy = self.enemy_class(self.game, self.x_spawn + 0 * TILESIZE,
                                self.y_spawn + 0 * TILESIZE)
            self.spawned_enemies.add(enemy)  # Dodaj przeciwnika do grupy spawned enemies
            self.game.all_sprites.add(enemy)  # Dodaj przeciwnika do ogólnej grupy all_sprites
            self.game.enemies.add(enemy)  # Dodaj przeciwnika do ogólnej grupy all_sprites

            # Zresetuj licznik czasu spawnu
            self.spawn_timer = 0
class RatSpawner(pygame.sprite.Sprite):
    def __init__(self, game, x, y, spawn_rate, max_spawn, enemy_class,active_quest = False):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.active_quest_rat = active_quest

        self.x_spawn=x
        self.y_spawn=y
        
        self.spawn_rate = spawn_rate  # Określa, co ile klatek pojawi się nowy przeciwnik
        self.spawn_timer = 0
        self.max_spawn = max_spawn  # Maksymalna liczba przeciwników jednocześnie
        self.enemy_class = enemy_class
        self.spawned_enemies = pygame.sprite.Group()  # Grupa do śledzenia spawned enemies
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def update(self):
        # Zliczaj klatki
        self.spawn_timer += 1
        # Sprawdź, czy przyszedł czas na stworzenie nowego przeciwnika
        if self.spawn_timer >= self.spawn_rate and len(self.spawned_enemies) < self.max_spawn and self.active_quest_rat:
            
                        
            # Stwórz nowego przeciwnika i ustaw go w losowym miejscu wokół spawnera
            enemy = self.enemy_class(self.game, self.x_spawn + 0 * TILESIZE,
                                self.y_spawn + 0 * TILESIZE)
            self.spawned_enemies.add(enemy)  # Dodaj przeciwnika do grupy spawned enemies
            self.game.all_sprites.add(enemy)  # Dodaj przeciwnika do ogólnej grupy all_sprites
            self.game.enemies.add(enemy)  # Dodaj przeciwnika do ogólnej grupy all_sprites

            # Zresetuj licznik czasu spawnu
            self.spawn_timer = 0
class DemonSpawner(pygame.sprite.Sprite):
    def __init__(self, game, x, y, spawn_rate, max_spawn, enemy_class,active_quest = False):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.active_quest_demon = active_quest

        self.x_spawn=x
        self.y_spawn=y
        
        self.spawn_rate = spawn_rate  # Określa, co ile klatek pojawi się nowy przeciwnik
        self.spawn_timer = 0
        self.max_spawn = max_spawn  # Maksymalna liczba przeciwników jednocześnie
        self.enemy_class = enemy_class
        self.spawned_enemies = pygame.sprite.Group()  # Grupa do śledzenia spawned enemies
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def update(self):
        # Zliczaj klatki
        self.spawn_timer += 1
        # Sprawdź, czy przyszedł czas na stworzenie nowego przeciwnika
        if self.spawn_timer >= self.spawn_rate and len(self.spawned_enemies) < self.max_spawn and self.active_quest_demon:
            
                        
            # Stwórz nowego przeciwnika i ustaw go w losowym miejscu wokół spawnera
            enemy = self.enemy_class(self.game, self.x_spawn + 0 * TILESIZE,
                                self.y_spawn + 0 * TILESIZE)
            self.spawned_enemies.add(enemy)  # Dodaj przeciwnika do grupy spawned enemies
            self.game.all_sprites.add(enemy)  # Dodaj przeciwnika do ogólnej grupy all_sprites
            self.game.enemies.add(enemy)  # Dodaj przeciwnika do ogólnej grupy all_sprites

            # Zresetuj licznik czasu spawnu
            self.spawn_timer = 0
class EnemySpawnerPack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, spawn_rate, max_spawn):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))  # Kolor czerwony dla spawnera
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.x_spawn=x
        self.y_spawn=y
        
        self.spawn_rate = spawn_rate  # Określa, co ile klatek pojawi się nowy przeciwnik
        self.spawn_timer = 0
        self.max_spawn = max_spawn  # Maksymalna liczba przeciwników jednocześnie
        self.enemy_classes = [Bandit,Archer,Mage]
        self.enemy_class = random.choice(self.enemy_classes)
        self.spawned_enemies = pygame.sprite.Group()  # Grupa do śledzenia spawned enemies
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def update(self):
        # Zliczaj klatki
        self.spawn_timer += 1
        # Sprawdź, czy przyszedł czas na stworzenie nowego przeciwnika
        if self.spawn_timer >= self.spawn_rate and len(self.spawned_enemies) < self.max_spawn:
            # Stwórz nowego przeciwnika i ustaw go w losowym miejscu wokół spawnera
            enemy = self.enemy_class(self.game, self.x_spawn + 0 * TILESIZE,
                                self.y_spawn + 0 * TILESIZE)
            self.spawned_enemies.add(enemy)  # Dodaj przeciwnika do grupy spawned enemies
            self.game.all_sprites.add(enemy)  # Dodaj przeciwnika do ogólnej grupy all_sprites
            self.game.enemies.add(enemy)  # Dodaj przeciwnika do ogólnej grupy all_sprites

            # Zresetuj licznik czasu spawnu
            self.spawn_timer = 0
            self.enemy_class = random.choice(self.enemy_classes)
        elif len(self.spawned_enemies) == self.max_spawn:
            self.spawn_timer = 0
