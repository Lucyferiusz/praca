import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Stałe
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Klasa reprezentująca umiejętność
class Skill(pygame.sprite.Sprite):
    def __init__(self, name, description, image_path, unlock_level):
        super().__init__()
        self.name = name
        self.description = description
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.unlock_level = unlock_level
        self.locked = True

    def unlock(self):
        self.locked = False

# Klasa reprezentująca drzewko umiejętności
class SkillTree:
    def __init__(self):
        self.skills = [
            Skill("Atak Okrężny", "Atakuj we wszystkich kierunkach", "skill1.png", 1),
            Skill("Potężny Atak", "Zadaj podwójne obrażenia i atakuj 2 kratki do przodu", "skill2.png", 2),
            Skill("Przyspieszenie", "Premia do prędkości na 5 sekund, potem spowolnienie", "skill3.png", 3)
        ]
        self.level = 0

    def unlock_skill(self, skill_index):
        if skill_index < len(self.skills) and self.level >= self.skills[skill_index].unlock_level:
            self.skills[skill_index].unlock()
            print(f"Odblokowano umiejętność: {self.skills[skill_index].name}")
        else:
            print("Nie można odblokować tej umiejętności")

# Klasa reprezentująca ekran gry
class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.skill_tree = SkillTree()
        self.font = pygame.font.Font(None, 36)

    def draw_skills(self):
        for i, skill in enumerate(self.skill_tree.skills):
            text = self.font.render(f"{skill.name}: {'Odblokowana' if not skill.locked else 'Zablokowana'}", True, BLACK)
            self.screen.blit(text, (50, 50 + i * 40))

# Klasa reprezentująca inwentarz
class Inventory:
    def __init__(self, screen):
        self.screen = screen
        self.slots = [None] * 8  # Zakładamy, że mamy 8 slotów w inwentarzu
        self.skills = []  # Lista przechowująca umiejętności

    def add_skill(self, skill):
        self.skills.append(skill)

    def draw_inventory(self):
        # Rysowanie inwentarza
        # ...

        # Rysowanie umiejętności
        for i, skill in enumerate(self.skills):
            text = pygame.font.Font(None, 24).render(f"Umiejętność: {skill.name}", True, BLACK)
            self.screen.blit(text, (50, 300 + i * 30))

# Inicjalizacja ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Skill Tree and Inventory Demo")
clock = pygame.time.Clock()

# Inicjalizacja inwentarza
inventory = Inventory(screen)

# Pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Obsługa zdarzeń dla umiejętności
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            inventory.skill_tree.level += 1
            print(f"Zdobyto poziom! Aktualny poziom: {inventory.skill_tree.level}")

            if inventory.skill_tree.level == 2:
                inventory.skill_tree.unlock_skill(0)
            elif inventory.skill_tree.level == 4:
                inventory.skill_tree.unlock_skill(1)
            elif inventory.skill_tree.level == 6:
                inventory.skill_tree.unlock_skill(2)

    inventory.draw_inventory()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
