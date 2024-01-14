import pygame
import random
import math
from scripts.config import *

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
        self.groups = self.game.attacks, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Oblicz kierunek ataku na podstawie pozycji gracza
        self.direction = self.calculate_direction()

    def update(self):
        self.move()
        self.check_player_collision()
        self.check_disappear()

    def move(self):
        # Przesuń atak w kierunku gracza
        self.rect.x += self.direction[0] * TILESIZE
        self.rect.y += self.direction[1] * TILESIZE

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
        # Znikaj po przebyciu 6 kratek od początkowej pozycji łucznika
        dx = self.rect.x - self.x
        dy = self.rect.y - self.y
        distance_travelled = math.sqrt(dx**2 + dy**2)

        if distance_travelled >= 6 * TILESIZE:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game,x,y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites,self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x_change = 0
        self.y_change = 0
        self.facing = random.choice(['left','right','up','down'])
        self.max_travel = random.randint(3*TILESIZE,5*TILESIZE)
        self.movement_loop =0

        self.hp = 50
        self.max_hp = self.hp
        self.speed = 1

        self.x = x* TILESIZE
        self.y = y* TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.enemies_spritesheet.get_sprite(2,3+128,self.width,self.height)

        self.immunity_timer = 0 
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        
    def take_damage(self, damage):
        if self.immunity_timer <= 0:
            self.hp -= damage
            print(f"{self.hp}/{self.max_hp}")
            if self.hp <= 0:
                self.kill()
            else:
                self.start_immunity(5*5+5) 
                

    def start_immunity(self, duration):
        self.image_org = self.image.copy() 
        self.immunity_timer = duration


    def update(self):

        
        self.movement()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0 
        self.y_change = 0

        
        if self.immunity_timer > 0:
            # Efekt podświetlenia w pierwszej klatce niesmiertelności
            if self.immunity_timer == 5 * 5 + 1:
                self.image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)  # Czerwony kolor z połową przezroczystości
            # Wyłącz efekt podświetlenia w ostatniej klatce niesmiertelności
            elif self.immunity_timer == 1:
                self.image.blit(self.image_org, (0, 0))
            self.immunity_timer -= 1
            
        pass
   
    def movement(self):
        player = self.game.player
        distance_to_player = math.sqrt((self.rect.x - player.rect.x)**2 + (self.rect.y - player.rect.y)**2)

        
        if distance_to_player < 1 * TILESIZE/2:
            
            self.x_change += self.speed  if self.rect.x > self.game.player.rect.x else -self.speed
            self.y_change += self.speed  if self.rect.y > self.game.player.rect.y else -self.speed
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



# W klasie Rat w skrypcie sprites.py
class Rat(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # Dodaj nowe właściwości dotyczące ataku
        self.attack_range = TILESIZE * 0.5  # Zakres ataku w pikselach
        self.attack_damage = 4  # Obrażenia zadawane przez atak
        self.attack_cooldown = 60*2  # Cooldown ataku w klatkach
        self.attack_timer = 0  # Licznik czasu od ostatniego ataku
        self.image = self.game.rats_spritesheet.get_sprite(0, 0, self.width, self.height)
    def update(self):
        super().update()
        self.attack_timer += 1

        # Sprawdź, czy gracz jest wystarczająco blisko i czy minął czas od ostatniego ataku
        if self.distance_to_player() <= self.attack_range and self.attack_timer >= self.attack_cooldown:
            self.attack_player()

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


# W klasie WildBoar w skrypcie sprites.py
class WildBoar(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # właściwości dotyczące ataku
        self.hp = 50
        self.attack_range = TILESIZE * 1  # Zakres ataku w pikselach
        self.attack_damage = 15  # Obrażenia zadawane przez atak
        self.attack_cooldown = 60*1  # Cooldown ataku w klatkach
        self.attack_timer = 0  # Licznik czasu od ostatniego ataku
        self.image = self.game.wildboar_spritesheet.get_sprite(0, 0, self.width, self.height)


        self.charge_speed_multiplier = 1.5  # Mnożnik prędkości podczas szarży
        self.charge_cooldown = 500  # Czas odnowienia (w milisekundach) między kolejnymi szarżami
        self.last_charge_time = pygame.time.get_ticks()
        self.charging = False 


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
        self.hp = 90
        self.max_hp = self.hp
        self.speed = 0.90
        self.image = self.game.enemies_spritesheet.get_sprite(4, 6, self.width, self.height)
        self.max_travel = 5*TILESIZE

        self.shoot_frequency = 60*5
        self.shoot_timer = random.randint(0, self.shoot_frequency)
        self.attacks = pygame.sprite.Group()
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



    def update(self):
        super().update()
        
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = self.shoot_frequency

        self.attacks.update()
        self.check_attack_collision()
    
class Bandit(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.enemies_spritesheet.get_sprite(6, 9, self.width, self.height)
        self.hp = 35

        self.attack_range = TILESIZE * 1  # Zakres ataku w pikselach
        self.attack_damage = 10  # Obrażenia zadawane przez atak
        self.attack_cooldown = 60  # Cooldown ataku w klatkach
        self.attack_timer = 0  # Licznik czasu od ostatniego ataku
    
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
    
    def update(self):
        super().update()
        self.attack_timer += 1

        # Sprawdź, czy gracz jest wystarczająco blisko i czy minął czas od ostatniego ataku
        if self.player_distance <= self.attack_range and self.attack_timer >= self.attack_cooldown:
            self.attack_player()

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
        self.image = self.game.enemies_spritesheet.get_sprite(8, 12, self.width, self.height)
        self.hp = 25

    def attack(self):
        # Logika ataku dystansowego maga
        pass

    def heal(self):
        # Logika leczenia pobliskiego wroga
        pass

    def area_attack(self):
        # Logika obszarowego ataku maga
        pass

class Demon(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.enemies_spritesheet.get_sprite(10, 15, self.width, self.height)
        self.hp = 50

    def attack(self):
        # Logika ataku dystansowego demona
        pass


class EnemySpawner(pygame.sprite.Sprite):
    def __init__(self, game, x, y, spawn_rate, max_spawn, enemy_class):
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
        elif len(self.spawned_enemies) == self.max_spawn:
            self.spawn_timer = 0
