import pygame
import sys
from scripts.config import *
from scripts.sprites import *
# from scripts.sprites import At

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

class Skill:
    def __init__(self, image_path, name, position, xp_required, level_required):
        self.image = pygame.image.load(image_path)
        self.name = name
        self.unlocked = False
        self.rect = pygame.Rect(position[0], position[1], 100, 100)
        self.xp_required = xp_required
        self.level_required = level_required

class MultiAttack(Skill):
    def __init__(self, game, image_path, name, position,xp_required,level_required):
        super().__init__(image_path, name, position,xp_required,level_required)
        self.attacks_generated = False
        self.game = game
        self.last_attack_time = 0
        self.attack_delay = 1000*5  # Opóźnienie w milisekundach (5 sekund)

    def handle_keypress(self, event):
        if event.key == pygame.K_9:
            self.use()

    def use(self):
        current_time = pygame.time.get_ticks()

        if not self.unlocked or self.attacks_generated or (current_time - self.last_attack_time) < self.attack_delay:
            return

        # Wywołaj 4 ataki w każdym kierunku
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            if direction == 'up':
                attack = Attack(self.game, self.game.player.rect.x, self.game.player.rect.y - TILESIZE)
            elif direction == 'down':
                attack = Attack(self.game, self.game.player.rect.x, self.game.player.rect.y + TILESIZE)
            elif direction == 'left':
                attack = Attack(self.game, self.game.player.rect.x - TILESIZE, self.game.player.rect.y)
            elif direction == 'right':
                attack = Attack(self.game, self.game.player.rect.x + TILESIZE, self.game.player.rect.y)

            self.game.attacks.add(attack)

        self.last_attack_time = current_time  # Zapisz czas ostatniego ataku


class SpeedBust(Skill):
    def __init__(self, game, image_path, name, position,xp_required,level_required):
        super().__init__(image_path, name, position,xp_required,level_required)
        self.game = game
        self.cooldown_duration = 14000  # 14 sekund w milisekundach
        self.duration = 3000  # 3 sekundy w milisekundach
        self.original_speed = None
        self.last_use_time = 0
        self.duration_timer = None  # Zmieniłem na None

    def handle_keypress(self, event):
        if event.key == pygame.K_8:
            self.use()

    def use(self):
        self.current_time = pygame.time.get_ticks()

        if not self.unlocked  or self.duration_timer:
            return

        # Zapisz oryginalną prędkość gracza przed zwiększeniem
        self.original_speed = self.game.player.PLAYER_SPEED

        # Zwiększ prędkość gracza 2 razy
        self.game.player.PLAYER_SPEED *= 2

        # Rozpocznij odliczanie czasu trwania efektu
        self.duration_timer = pygame.time.get_ticks()

    def update(self):
        self.current_time = pygame.time.get_ticks()

        # Sprawdź, czy upłynął czas trwania efektu
        if self.duration_timer and self.current_time - self.duration_timer > self.duration:
            # Przywróć oryginalną prędkość gracza
            self.game.player.PLAYER_SPEED = self.original_speed

            # Zresetuj zmienne
            self.duration_timer = None
            self.last_use_time = self.current_time

class ImmortalDefence(Skill):
    def __init__(self, game, image_path, name, position,xp_required,level_required):
        super().__init__(image_path, name, position,xp_required,level_required)
        self.game = game
        self.cooldown_duration = 2000  # 10 sekund w milisekundach
        self.duration = 4000  # 4 sekundy w milisekundach
        self.immortal_timer = 0  # Licznik czasu trwania niesmiertelności
        self.cooldown_timer = 0  # Licznik czasu trwania cooldownu

    def use(self):
        current_time = pygame.time.get_ticks()

        if not self.unlocked or (current_time - self.cooldown_timer) < self.cooldown_duration or self.immortal_timer > 0:
            return

        self.game.player.start_immunity(60*4)
        self.immortal_timer = current_time  # Ustaw timer niesmiertelnosci
        self.cooldown_timer = current_time  # Ustaw timer cooldownu

    def update(self):
        current_time = pygame.time.get_ticks()
        # Sprawdź, czy niesmiertelnosc powinna być aktywowana
        if self.immortal_timer > 0 and current_time - self.immortal_timer > self.duration:
            # self.game.player.disable_immortal()  # Wyłącz niesmiertelnosc
            self.immortal_timer = 0  # Zresetuj timer niesmiertelnosci

        # Sprawdź, czy cooldown powinien być zakończony
        if self.cooldown_timer > 0 and current_time - self.cooldown_timer > self.cooldown_duration:
            self.cooldown_timer = 0  # Zresetuj timer cooldownu



class SkillTree:
    def __init__(self, game, screen, skills):
        self.skills = skills
        self.game = game
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.background.fill((255, 255, 255, 128))

        

    def draw(self):
        self.screen.blit(self.background, (0, 0))  # Rysowanie półprzezroczystego tła
        text = self.font.render("Umiejętności: Drzewko Umiejętności", True, BLACK)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 10))
        self.screen.blit(text, text_rect)

        # Rysowanie kwadratów z obrazkami i nazwami umiejętności
        x = 50
        y = 100
        gap = 300
        for skill in self.skills:
            skill.rect.x = x
            skill.rect.y = y
            if skill.unlocked:
                color = WHITE
            else:
                color = RED_GRAY
            # Dodaj pasek postępu (o ile umiejętność nie jest odblokowana)
            
            progress_width = (self.game.player.xp_total / skill.xp_required) * 100  # Szerokość paska postępu
            if progress_width >=100:
                progress_width = 100
                
            pygame.draw.rect(self.screen, GREEN, (x, y + 130, progress_width, 10))
            pygame.draw.rect(self.screen, GREEN, (x, y + 130, 100, 10),2)
            pygame.draw.rect(self.screen, color, skill.rect)
            image = pygame.transform.scale(skill.image, (100, 100))
            self.screen.blit(image, (x, y))
            text = self.font.render(skill.name, True, BLACK)
            self.screen.blit(text, (x, y + 110))
            x += gap

    def handle_mouse_click(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Lewy przycisk myszy
            for skill in self.skills:
                if not skill.unlocked and skill.rect.collidepoint(mouse_pos):
                    # Sprawdź warunki odblokowania dla konkretnej zdolności
                    if (
                        skill.name == "Wielo krotny atak"
                        and self.game.player.xp_total >= skill.xp_required
                        and self.game.player.level >= skill.level_required
                    ):
                        # Odblokuj zdolność
                        skill.unlocked = True
                        self.draw()
                        # Sprawdź warunki odblokowania dla konkretnej umiejętności
                    
                    if (
                        skill.name == "Rycerski Błysk"
                        and self.game.player.xp_total >= skill.xp_required
                        and self.game.player.level >= skill.level_required
                    ):
                        # Odblokuj umiejętność
                        skill.unlocked = True
                        self.draw()  # Przerysuj drzewko umiejętności
                        # Tutaj możesz dodać inne akcje lub warunki, które chcesz zrealizować po odblokowaniu umiejętności
                    elif (
                        skill.name == "Nieśmiertelna tarcza"
                        and self.game.player.xp_total >= skill.xp_required
                        and self.game.player.level >= skill.level_required
                    ):
                        # Odblokuj umiejętność
                        skill.unlocked = True
                        self.draw()  # Przerysuj drzewko umiejętności
                        # Tutaj możesz dodać inne akcje lub warunki, które chcesz zrealizować po odblokowaniu umiejętności

