import pygame
import random
import math
from scripts.config import *
from scripts.sprites import Enemy

                    


# W klasie Rat w skrypcie sprites.py
class Rat(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # Dodaj nowe właściwości dotyczące ataku
        self.attack_range = TILESIZE * 0.3  # Zakres ataku w pikselach
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
        # Dodaj nowe właściwości dotyczące ataku
        self.attack_range = TILESIZE * 1  # Zakres ataku w pikselach
        self.attack_damage = 15  # Obrażenia zadawane przez atak
        self.attack_cooldown = 60*1  # Cooldown ataku w klatkach
        self.attack_timer = 0  # Licznik czasu od ostatniego ataku
        self.image = self.game.wildboar_spritesheet.get_sprite(0, 0, self.width, self.height)


        self.charge_speed_multiplier = 1.5  # Mnożnik prędkości podczas szarży
        self.charge_cooldown = 500  # Czas odnowienia (w milisekundach) między kolejnymi szarżami
        self.last_charge_time = pygame.time.get_ticks()


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
        print("Dzik rozpoczyna szarżę!")
        self.speed *= self.charge_speed_multiplier
        # Ustaw timer na zakończenie szarży (np. po 2 sekundach)
        pygame.time.set_timer(pygame.USEREVENT, 500)

    def end_charge(self):
        print("Szarża dzika zakończona.")
        self.speed /= self.charge_speed_multiplier

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
        self.image = self.game.enemies_spritesheet.get_sprite(4, 6, self.width, self.height)
        self.hp = 30
    def movement(self):
        player_distance = math.sqrt((self.rect.x - self.game.player.rect.x)**2 + (self.rect.y - self.game.player.rect.y)**2)

        if player_distance < 3 * TILESIZE:
            # Gracz jest zbyt blisko, więc oddal się od gracza
            self.x_change += self.speed * 2 if self.rect.x < self.game.player.rect.x else -self.speed * 2
            self.y_change += self.speed * 2 if self.rect.y < self.game.player.rect.y else -self.speed * 2
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
    def attack(self):
        # Logika ataku dystansowego łucznika
        pass

class Bandit(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.enemies_spritesheet.get_sprite(6, 9, self.width, self.height)
        self.hp = 35

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
    def __init__(self, game, x, y, spawn_rate):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.spawn_rate = spawn_rate  # Określa, co ile klatek pojawi się nowy przeciwnik
        self.spawn_timer = 0

    def update(self):
        # Zliczaj klatki
        self.spawn_timer += 1

        # Sprawdź, czy przyszedł czas na stworzenie nowego przeciwnika
        if self.spawn_timer >= self.spawn_rate:
            # Wybierz losową klasę przeciwnika
            enemy_classes = [Rat, WildBoar, Archer, Bandit, Mage, Demon]
            enemy_class = random.choice(enemy_classes)

            # Stwórz nowego przeciwnika i ustaw go w losowym miejscu wokół spawnera
            enemy = enemy_class(self.game, self.x + random.randint(-2, 2) * TILESIZE,
                                self.y + random.randint(-2, 2) * TILESIZE)

            # Zresetuj licznik czasu spawnu
            self.spawn_timer = 0
