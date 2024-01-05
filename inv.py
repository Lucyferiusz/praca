import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Stałe dotyczące ekranu
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Stałe dotyczące inventory
context_menu_active = False
context_menu_position = (0, 0)

SLOT_SIZE = 50
ITEM_SIZE = 40
INVENTORY_WIDTH = 7
INVENTORY_HEIGHT = 5
INVENTORY_SIZE = INVENTORY_WIDTH * INVENTORY_HEIGHT
INVENTORY_X = 50
INVENTORY_Y = 50

DEL_SLOT_X = INVENTORY_X + SLOT_SIZE * INVENTORY_WIDTH + 5
DEL_SLOT_Y = INVENTORY_Y + SLOT_SIZE * (INVENTORY_HEIGHT - 1)
DEL_RECT = pygame.Rect(DEL_SLOT_X, DEL_SLOT_Y, SLOT_SIZE, SLOT_SIZE)

ARMOR_SLOT_SIZE = 60
WEAPON_SLOT_SIZE = 60

# Zaktualizowane stałe dotyczące inventory
ARMOR_SLOT_MARGIN = 10
WEAPON_SLOT_MARGIN = 5




def calculate_armor_slot_position():
    armor_slot_x = INVENTORY_X + INVENTORY_WIDTH * SLOT_SIZE + ARMOR_SLOT_MARGIN
    armor_slot_y = INVENTORY_Y
    return armor_slot_x, armor_slot_y, pygame.Rect(armor_slot_x, armor_slot_y, ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE)


def calculate_weapon_slot_position():
    weapon_slot_x = INVENTORY_X + INVENTORY_WIDTH * SLOT_SIZE + ARMOR_SLOT_MARGIN + ARMOR_SLOT_SIZE + WEAPON_SLOT_MARGIN
    weapon_slot_y = INVENTORY_Y
    return weapon_slot_x, weapon_slot_y, pygame.Rect(weapon_slot_x, weapon_slot_y, WEAPON_SLOT_SIZE, WEAPON_SLOT_SIZE)


WEAPON_SLOT_RECT = pygame.Rect(0, 0, 0, 0)
ARMOR_SLOT_RECT = pygame.Rect(0, 0, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inventory System")
clock = pygame.time.Clock()


class Item:
    def __init__(self, name, image_color):
        self.name = name
        self.image = pygame.Surface((ITEM_SIZE, ITEM_SIZE), pygame.SRCALPHA)
        self.image.fill(image_color)
        self.rect = self.image.get_rect()
        self.slot = None

    def set_position(self, x, y):
        self.rect.x = x + (SLOT_SIZE - ITEM_SIZE) // 2
        self.rect.y = y + (SLOT_SIZE - ITEM_SIZE) // 2

    def set_equipped_position(self, x, y, size):
        self.rect.x = x + (size - ITEM_SIZE) // 2
        self.rect.y = y + (size - ITEM_SIZE) // 2


class Armor(Item):
    def __init__(self, name):
        super().__init__(name, (0, 0, 255))
        self.equipped = False

    def wear(self):
        if not self.equipped:
            print(f"Wearing armor: {self.name}")
            self.equipped = True
        else:
            print(f"Removing armor: {self.name}")
            self.equipped = False

    def set_equipped_position(self):
        super().set_position(*calculate_armor_slot_position()[:2])  # Użyj set_position

    def set_image(self, image_path):
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (ITEM_SIZE, ITEM_SIZE))
        self.image.set_colorkey((0, 0, 0)) 

class Weapon(Item):
    def __init__(self, name):
        super().__init__(name, (255, 255, 0))
        self.equipped = False

    def equip(self):
        if not self.equipped:
            print(f"Equipping weapon: {self.name}")
            self.equipped = True
        else:
            print(f"Unequipping weapon: {self.name}")
            self.equipped = False

    def set_equipped_position(self):
        super().set_position(*calculate_weapon_slot_position()[:2])  # Użyj set_position

    def set_image(self, image_path):
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (ITEM_SIZE, ITEM_SIZE))
        self.image.set_colorkey((0, 0, 0)) 


class Potion(Item):
    def __init__(self, name):
        super().__init__(name, (255, 0, 0))
        self.equipped = False
        self.healing = 10
        original_image = pygame.image.load("assets\img\potion.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (ITEM_SIZE, ITEM_SIZE))
        self.image.set_colorkey((0, 0, 0)) 
        
    def drink(self):
        if not self.equipped:
            print(f"Wypiłeś: {self.name} uleczono {self.healing} HP")
            self.equipped = True

    def set_equipped_position(self):
        super().set_position(*calculate_weapon_slot_position()[:2])  # Użyj set_position



# Przykład użycia dla Armor
lether_armor = Armor("Custom Armor")
# rusted_sword.set_image("custom_weapon_image.png")

# Przykład użycia dla Weapon
rusted_sword = Weapon("Custom Weapon")
rusted_sword.set_image("assets/img/ust_sword.png")




class Inventory:
    def __init__(self):
        self.slots = [None] * (INVENTORY_SIZE + 2)

    def add_item(self, item, slot=None):
        if slot is not None:
            if self.slots[slot] is None:
                item.slot = slot
                self.slots[slot] = item
                return True
        else:
            for i, slot in enumerate(self.slots):
                if slot is None:
                    item.slot = i
                    self.slots[i] = item
                    return i
        return False

    def remove_item(self, slot):
        if self.slots[slot] is not None:
            item = self.slots[slot]
            item.slot = None
            self.slots[slot] = None
            return item
        return None


# Dodajemy funkcję, która obsługuje wypijanie potionu
def drink_potion(item,inventory):
    if isinstance(item,Potion):
        item.drink()
        inventory.remove_item(item.slot)


# Dodajemy funkcję, która obsługuje zakładanie zbroi
def equip_armor(item):
    if not item.equipped:
        print(f"Założono zbroję: {item.name}")
        item.equipped = True
    else:
        print(f"Zdjęto zbroję: {item.name}")
        item.equipped = False


# Dodajemy funkcję, która obsługuje zakładanie broni
def equip_weapon(item):
    if not item.equipped:
        print(f"Założono broń: {item.name}")
        item.equipped = True
    else:
        print(f"Zdjęto broń: {item.name}")
        item.equipped = False


def draw_context_menu(selected_item,inventory):
    global context_menu_active, context_menu_position  # Użyj zmiennych globalnych

    menu_options = ["Wypij"]
    font = pygame.font.Font(None, 24)

    menu_rect = pygame.Rect(context_menu_position, (120, len(menu_options)*45))
    pygame.draw.rect(screen, (55, 125, 23), menu_rect)

    for i, option in enumerate(menu_options):
        text = font.render(option, True, BLACK)
        text_rect = text.get_rect()
        text_rect.topleft = (menu_rect.x + 10, menu_rect.y + 10 + i * 30)
        screen.blit(text, text_rect)

    # Obsługa zdarzeń menu kontekstowego
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            option_index = (event.pos[1] - menu_rect.y - 10) // 30
            if 0 <= option_index < len(menu_options):
                selected_option = menu_options[option_index]
                if selected_option == "Wypij":
                    drink_potion(selected_item,inventory)
                    context_menu_active = False
                    
                

    # Sprawdź, czy menu zostało zamknięte (kliknięcie poza menu)
    if not menu_rect.collidepoint(pygame.mouse.get_pos()):
        context_menu_active = False


def draw_inventory(inventory):
    for row in range(INVENTORY_HEIGHT):
        for col in range(INVENTORY_WIDTH):
            slot_x = INVENTORY_X + col * SLOT_SIZE
            slot_y = INVENTORY_Y + row * SLOT_SIZE
            pygame.draw.rect(screen, WHITE, (slot_x, slot_y, SLOT_SIZE, SLOT_SIZE), 2)
            item = inventory.slots[row * INVENTORY_WIDTH + col]
            if item:
                screen.blit(item.image, (slot_x + 5, slot_y + 5))
    pygame.draw.rect(screen, WHITE, (DEL_SLOT_X, DEL_SLOT_Y, SLOT_SIZE, SLOT_SIZE), 2)


def draw_inventory_background():
    alpha_surface = pygame.Surface((SCREEN_WIDTH/5, SCREEN_HEIGHT), pygame.SRCALPHA)
    alpha_surface.fill(WHITE)  # Czarne tło z przezroczystością
    alpha_surface.set_alpha(128)
    screen.blit(alpha_surface, (0, 0))

    alpha_surface_inventory = pygame.Surface((INVENTORY_WIDTH * SLOT_SIZE, INVENTORY_HEIGHT * SLOT_SIZE),
                                             pygame.SRCALPHA)
    alpha_surface.fill((255, 0, 255, 128))  # Czarne tło z przezroczystością
    screen.blit(alpha_surface_inventory, (INVENTORY_X, INVENTORY_Y))

    alpha_surface_delete = pygame.Surface((SLOT_SIZE, SLOT_SIZE), pygame.SRCALPHA)
    alpha_surface.fill((255, 255, 255, 128))  # Czarne tło z przezroczystością
    screen.blit(alpha_surface_delete, (DEL_SLOT_X, DEL_SLOT_Y))

    alpha_surface_armor = pygame.Surface((ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE), pygame.SRCALPHA)
    alpha_surface.fill((255, 255, 255, 128))  # Czarne tło z przezroczystością
    screen.blit(alpha_surface_armor, calculate_armor_slot_position()[:2])

    alpha_surface_weapon = pygame.Surface((WEAPON_SLOT_SIZE, WEAPON_SLOT_SIZE), pygame.SRCALPHA)
    alpha_surface.fill((255, 255, 255, 128))  # Czarne tło z przezroczystością
    screen.blit(alpha_surface_weapon, calculate_weapon_slot_position()[:2])

def draw_extended_inventory(inventory):
    global ARMOR_SLOT_RECT, WEAPON_SLOT_RECT
    draw_inventory(inventory)

    # Sloty zbroi
    armor_slot_x, armor_slot_y, ARMOR_SLOT_RECT = calculate_armor_slot_position()
    pygame.draw.rect(screen, WHITE, (armor_slot_x, armor_slot_y, ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE), 2)
    armor_item = inventory.slots[INVENTORY_SIZE]
    if armor_item:
        draw_item(armor_item, armor_slot_x + 10, armor_slot_y + 10)
        armor_item.set_position(armor_slot_x+10, armor_slot_y+10)  # Użyj set_position

    # Sloty broni
    weapon_slot_x, weapon_slot_y, WEAPON_SLOT_RECT = calculate_weapon_slot_position()
    pygame.draw.rect(screen, WHITE, (weapon_slot_x, weapon_slot_y, WEAPON_SLOT_SIZE, WEAPON_SLOT_SIZE), 2)
    weapon_item = inventory.slots[INVENTORY_SIZE + 1]
    if weapon_item:
        draw_item(weapon_item, weapon_slot_x + 10, weapon_slot_y + 10)
        weapon_item.set_position(weapon_slot_x+10, weapon_slot_y+10)  # Użyj set_position

def draw_item(item, x, y):
    if item:
        screen.blit(item.image, (x, y))


def draw_button(button_color):
    pygame.draw.rect(screen, button_color, (650, 50, 100, 40))
    font = pygame.font.Font(None, 36)
    text = font.render("Dodaj", True, BLACK)
    screen.blit(text, (670, 60))


def draw_cursor_coordinates(pos):
    font = pygame.font.Font(None, 24)
    text = font.render(f"Kursor: {pos}", True, WHITE)
    screen.blit(text, (10, 10))

def main():
    global context_menu_active, context_menu_position, WEAPON_SLOT_RECT, ARMOR_SLOT_RECT
    inventory = Inventory()
    dragging_item = None
    dragging_offset = (-20, -20)
    original_slot = None
    is_mouse_dragging = False

        # Dodajemy zbroję testową do pierwszego slotu w inwentarzu
    test_armor = Armor("Zbroja Testowa")
    inventory.add_item(test_armor, 0)
    test_armor.set_position(
        INVENTORY_X + (0 % INVENTORY_WIDTH) * SLOT_SIZE,
        INVENTORY_Y + (0 // INVENTORY_WIDTH) * SLOT_SIZE
    )
    
    inventory.add_item(rusted_sword, 1)  # Add the test weapon to the second slot
    rusted_sword.set_position(
    INVENTORY_X + (1 % INVENTORY_WIDTH) * SLOT_SIZE,
    INVENTORY_Y + (1 // INVENTORY_WIDTH) * SLOT_SIZE
)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and 650 <= event.pos[0] <= 750 and 50 <= event.pos[1] <= 90 and not context_menu_active: #add button
                    new_item_added = inventory.add_item(Potion("Nowy Przedmiot"))
                    if new_item_added is not False:
                        new_item = inventory.slots[new_item_added]
                        new_item.set_position(
                            INVENTORY_X + (new_item_added % INVENTORY_WIDTH) * SLOT_SIZE,
                            INVENTORY_Y + (new_item_added // INVENTORY_WIDTH) * SLOT_SIZE
                        )
                elif event.button ==2 :
                    print(f"{inventory.slots = }")
                elif event.button == 1:
                    for i, item in enumerate(inventory.slots):
                        if item and item.rect.collidepoint(pygame.mouse.get_pos()):
                            dragging_item = inventory.remove_item(i)
                            is_mouse_dragging = True
                            original_slot = i
            elif event.type == pygame.MOUSEMOTION:
                if is_mouse_dragging and dragging_item:
                    if not context_menu_active:
                        dragging_item.rect.x = pygame.mouse.get_pos()[0] + dragging_offset[0]
                        dragging_item.rect.y = pygame.mouse.get_pos()[1] + dragging_offset[1]

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    for i, item in enumerate(inventory.slots):
                        if item and item.rect.collidepoint(pygame.mouse.get_pos()):
                            context_menu_position = (event.pos[0], event.pos[1])
                            selected_item_for_context_menu = item
                            if isinstance(selected_item_for_context_menu,Potion):
                                context_menu_active = True
                if event.button == 1:
                    is_mouse_dragging = False
                    if dragging_item:
                        slot_col = max(0, min(INVENTORY_WIDTH - 1, (pygame.mouse.get_pos()[0] - INVENTORY_X) // SLOT_SIZE))
                        slot_row = max(0, min(INVENTORY_HEIGHT - 1, (pygame.mouse.get_pos()[1] - INVENTORY_Y) // SLOT_SIZE))
                        slot_index = slot_row * INVENTORY_WIDTH + slot_col

                        # Usuń przedmiot z pierwotnego slotu
                        inventory.remove_item(original_slot)

                        if isinstance(dragging_item, Armor) and ARMOR_SLOT_RECT.collidepoint(pygame.mouse.get_pos()):
                            inventory.add_item(dragging_item, INVENTORY_SIZE)
                            dragging_item.set_equipped_position()

                        elif isinstance(dragging_item, Weapon) and WEAPON_SLOT_RECT.collidepoint(pygame.mouse.get_pos()):
                            inventory.add_item(dragging_item, INVENTORY_SIZE + 1)
                            dragging_item.set_equipped_position()

                        elif DEL_RECT.collidepoint(pygame.mouse.get_pos()):
                            # Nie dodawaj przedmiotu z powrotem, jeżeli wraca do miejsca początkowego
                            pass
                        elif 0 <= slot_index < INVENTORY_SIZE and inventory.slots[slot_index] is None:
                            inventory.add_item(dragging_item, slot_index)
                            dragging_item.set_position(
                                INVENTORY_X + (slot_index % INVENTORY_WIDTH) * SLOT_SIZE,
                                INVENTORY_Y + (slot_index // INVENTORY_WIDTH) * SLOT_SIZE
                            )
                        else:
                            # W przypadku, gdy przedmiot nie jest przenoszony do nowego slotu, wróć do pierwotnego
                            inventory.add_item(dragging_item, original_slot)
                            dragging_item.set_position(
                                INVENTORY_X + (original_slot % INVENTORY_WIDTH) * SLOT_SIZE,
                                INVENTORY_Y + (original_slot // INVENTORY_WIDTH) * SLOT_SIZE
                            )

                        dragging_item = None
                        original_slot = None





        screen.fill((0, 0, 0))
        draw_inventory_background()
        draw_extended_inventory(inventory)
        draw_button(WHITE)
        draw_cursor_coordinates(pygame.mouse.get_pos())
        draw_item(dragging_item, pygame.mouse.get_pos()[0] + dragging_offset[0],
                  pygame.mouse.get_pos()[1] + dragging_offset[1])

        if context_menu_active:
            draw_context_menu(selected_item_for_context_menu,inventory)
            
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()