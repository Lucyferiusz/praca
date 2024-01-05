import pygame

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Stałe dotyczące inventory

SLOT_SIZE = 50
ITEM_SIZE = 40
INVENTORY_WIDTH = 3
INVENTORY_HEIGHT = 4
INVENTORY_SIZE = INVENTORY_WIDTH * INVENTORY_HEIGHT
INVENTORY_X = 200
INVENTORY_Y = 300

DEL_SLOT_X = INVENTORY_X + SLOT_SIZE * INVENTORY_WIDTH + 5
DEL_SLOT_Y = INVENTORY_Y + SLOT_SIZE * (INVENTORY_HEIGHT - 1)


ARMOR_SLOT_SIZE = 60
WEAPON_SLOT_SIZE = 60
dragging_offset = (-20, -20)
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

class Item:
    def __init__(self, name, image_color):
        self.name = name
        self.image = pygame.Surface((ITEM_SIZE, ITEM_SIZE), pygame.SRCALPHA)
        self.image.fill(image_color)
        self.rect = self.image.get_rect()
        self.slot = None

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_equipped_position(self, x, y, size):
        self.rect.x = x
        self.rect.y = y

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
        super().set_position(*calculate_armor_slot_position()[:2])

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
        super().set_position(*calculate_weapon_slot_position()[:2])

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
        super().set_position(*calculate_weapon_slot_position()[:2])

class Inventory:
    def __init__(self, screen,game):
        self.screen = screen
        self.slots = [None] * (INVENTORY_SIZE + 2)
        self.dragging_item = None
        self.game = game
        self.context_menu_active = False
        _,_,self.WEAPON_SLOT_RECT = calculate_weapon_slot_position()
        _,_,self.ARMOR_SLOT_RECT = calculate_armor_slot_position()
        self.DEL_RECT = pygame.Rect(DEL_SLOT_X, DEL_SLOT_Y, SLOT_SIZE, SLOT_SIZE)
    
    
    def add_test_items(self, item_type):
        if item_type == 1:
            # Dodaj potion
            potion = Potion("Test Potion")
            self.add_item(potion)
        elif item_type == 2:
            # Dodaj armor
            armor = Armor("Test Armor")
            self.add_item(armor)
        elif item_type == 3:
            # Dodaj weapon
            weapon = Weapon("Test Weapon")
            self.add_item(weapon)
            
    def add_item(self, item, slot=None):
        if slot is not None:
            if self.slots[slot] is None:
                item.slot = slot
                self.slots[slot] = item
                # Oblicz automatycznie pozycję i rect
                row = slot // INVENTORY_WIDTH
                col = slot % INVENTORY_WIDTH
                item.set_position(INVENTORY_X + 5 + col * SLOT_SIZE, INVENTORY_Y +5 + row * SLOT_SIZE)
                item.rect.topleft = item.rect.x , item.rect.y 
                return True
        else:
            for i, slot in enumerate(self.slots):
                if slot is None:
                    item.slot = i
                    self.slots[i] = item
                    # Oblicz automatycznie pozycję i rect
                    row = i // INVENTORY_WIDTH
                    col = i % INVENTORY_WIDTH
                    item.set_position(INVENTORY_X + 5 + col * SLOT_SIZE, INVENTORY_Y +5 + row * SLOT_SIZE)
                    item.rect.topleft = item.rect.x , item.rect.y 
                    return i
        return False

    def remove_item(self, slot):
        if self.slots[slot] is not None:
            item = self.slots[slot]
            item.slot = None
            self.slots[slot] = None
            return item
        return None

    def draw_context_menu(self, selected_item):
        
        menu_options = ["Drop"]
        if isinstance(selected_item, Potion):
            menu_options.append("Drink")
        elif isinstance(selected_item, (Weapon, Armor)):
            if selected_item.equipped:
                menu_options.append("Unequip")
            else:
                menu_options.append("Equip")

        font = pygame.font.Font(None, 24)

        menu_rect = pygame.Rect(self.context_menu_position, (120, len(menu_options)*45))
        pygame.draw.rect(self.screen, (55, 125, 23), menu_rect)

        for i, option in enumerate(menu_options):
            text = font.render(option, True, BLACK)
            text_rect = text.get_rect()
            text_rect.topleft = (menu_rect.x + 10, menu_rect.y + 10 + i * 30)
            self.screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                option_index = (event.pos[1] - menu_rect.y - 10) // 30
                if 0 <= option_index < len(menu_options):
                    selected_option = menu_options[option_index]
                    if selected_option == "Drop":
                        self.remove_item(selected_item.slot)
                        self.context_menu_active = False
                    elif selected_option == "Drink" and isinstance(selected_item, Potion):
                        selected_item.drink()
                        self.context_menu_active = False
                    elif selected_option == "Equip" and isinstance(selected_item, (Weapon, Armor)):
                        self.equip_item()
                        
                        self.context_menu_active = False
                    elif selected_option == "Unequip" and isinstance(selected_item, (Weapon, Armor)):
                        self.unequip_item()
                        self.context_menu_active = False


        if not menu_rect.collidepoint(pygame.mouse.get_pos()):
            self.context_menu_active = False

    def draw_inventory(self):
        self.draw_inventory_background()
        for row in range(INVENTORY_HEIGHT):
            for col in range(INVENTORY_WIDTH):
                slot_x = INVENTORY_X + col * SLOT_SIZE
                slot_y = INVENTORY_Y + row * SLOT_SIZE
                pygame.draw.rect(self.screen, WHITE, (slot_x, slot_y, SLOT_SIZE, SLOT_SIZE), 2)
                item = self.slots[row * INVENTORY_WIDTH + col]
                if item and item != self.dragging_item:  # Draw only non-dragging items
                    self.screen.blit(item.image, item.rect.topleft)

        # Draw the dragging item last
        if self.dragging_item:
            self.screen.blit(self.dragging_item.image, (self.dragging_item.rect.x, self.dragging_item.rect.y))

        # Draw other UI elements
        pygame.draw.rect(self.screen, WHITE, (DEL_SLOT_X, DEL_SLOT_Y, SLOT_SIZE, SLOT_SIZE), 2)

        # Draw the context menu
        if self.context_menu_active and self.selected_item_for_context_menu:
            self.draw_context_menu(self.selected_item_for_context_menu)

    def draw_inventory_background(self):
        alpha_surface = pygame.Surface((INVENTORY_WIDTH * SLOT_SIZE + 2 * 25 + 2 * 60 + 10, INVENTORY_HEIGHT * SLOT_SIZE + 2 * 25), pygame.SRCALPHA)
        alpha_surface.fill(WHITE)
        alpha_surface.set_alpha(128)
        self.screen.blit(alpha_surface, (INVENTORY_X - 25, INVENTORY_Y - 25))

        alpha_surface_inventory = pygame.Surface((INVENTORY_WIDTH * SLOT_SIZE, INVENTORY_HEIGHT * SLOT_SIZE), pygame.SRCALPHA)
        alpha_surface_inventory.fill((255, 0, 255, 128))
        self.screen.blit(alpha_surface_inventory, (INVENTORY_X, INVENTORY_Y))

        alpha_surface_armor = pygame.Surface((ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE), pygame.SRCALPHA)
        alpha_surface_armor.fill((255, 255, 255, 128))
        armor_slot_x, armor_slot_y, _ = calculate_armor_slot_position()
        self.screen.blit(alpha_surface_armor, (armor_slot_x, armor_slot_y))

        alpha_surface_weapon = pygame.Surface((WEAPON_SLOT_SIZE, WEAPON_SLOT_SIZE), pygame.SRCALPHA)
        alpha_surface_weapon.fill((255, 255, 255, 128))
        weapon_slot_x, weapon_slot_y, _ = calculate_weapon_slot_position()
        self.screen.blit(alpha_surface_weapon, (weapon_slot_x, weapon_slot_y))

        alpha_surface_delete = pygame.Surface((SLOT_SIZE, SLOT_SIZE), pygame.SRCALPHA)
        alpha_surface_delete.fill((255, 255, 255, 128))
        self.screen.blit(alpha_surface_delete, (DEL_SLOT_X, DEL_SLOT_Y))

    def draw_extended_inventory(self):
        
        self.draw_inventory()

        armor_slot_x, armor_slot_y, self.ARMOR_SLOT_RECT = calculate_armor_slot_position()
        pygame.draw.rect(self.screen, WHITE, (armor_slot_x, armor_slot_y, ARMOR_SLOT_SIZE, ARMOR_SLOT_SIZE), 2)
        armor_item = self.slots[INVENTORY_SIZE]
        if armor_item:
            self.draw_item(armor_item, armor_item.rect.x, armor_item.rect.y)

        weapon_slot_x, weapon_slot_y, self.WEAPON_SLOT_RECT = calculate_weapon_slot_position()
        pygame.draw.rect(self.screen, WHITE, (weapon_slot_x, weapon_slot_y, WEAPON_SLOT_SIZE, WEAPON_SLOT_SIZE), 2)
        weapon_item = self.slots[INVENTORY_SIZE + 1]
        if weapon_item:
            self.draw_item(weapon_item , weapon_item.rect.x, weapon_item.rect.y)

    def draw_item(self, item, x, y):
        if item:
            self.screen.blit(item.image, (x, y))


    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                print(f"{self.slots = }")
            if event.button == 1 and not self.game.is_mouse_dragging:
                for i, item in enumerate(self.slots):
                    if item and item.rect.collidepoint(pygame.mouse.get_pos()):
                        self.dragging_item = self.remove_item(i)
                        self.game.is_mouse_dragging = True
                        self.original_slot = i
                        break
            elif event.button == 3:  # Right mouse button
                for i,item in enumerate(self.slots):
                    if item and item.rect.collidepoint(pygame.mouse.get_pos()):
                        self.context_menu_active = True
                        self.context_menu_position = (event.pos[0]-10, event.pos[1]-10)
                        self.selected_item_for_context_menu = item
                        self.original_slot = i
                        self.draw_context_menu(item)
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.game.is_mouse_dragging :
                self.game.is_mouse_dragging = False
                if self.dragging_item:
                    slot_col = max(0, min(INVENTORY_WIDTH - 1, (pygame.mouse.get_pos()[0] - INVENTORY_X) // SLOT_SIZE))
                    slot_row = max(0, min(INVENTORY_HEIGHT - 1, (pygame.mouse.get_pos()[1] - INVENTORY_Y) // SLOT_SIZE))
                    slot_index = slot_row * INVENTORY_WIDTH + slot_col

                    if isinstance(self.dragging_item, Armor) and self.ARMOR_SLOT_RECT.collidepoint(pygame.mouse.get_pos()):
                            self.add_item(self.dragging_item, INVENTORY_SIZE)
                            self.dragging_item.set_equipped_position()
                    elif isinstance(self.dragging_item, Weapon) and self.WEAPON_SLOT_RECT.collidepoint(pygame.mouse.get_pos()):
                            self.add_item(self.dragging_item, INVENTORY_SIZE + 1)
                            self.dragging_item.set_equipped_position()
                            self.dragging_item.equip()
                            self.dragging_item = self.remove_item(self.original_slot)

                    elif self.DEL_RECT.collidepoint(pygame.mouse.get_pos()):
                        self.remove_item(self.original_slot)
                    elif self.add_item(self.dragging_item, slot_index) is False:
                        self.add_item(self.dragging_item, self.original_slot)
                            

                    
                    self.dragging_item = None
                    self.original_slot = None

        elif event.type == pygame.MOUSEMOTION:
            if self.game.is_mouse_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.dragging_item.set_position(mouse_x + dragging_offset[0], mouse_y + dragging_offset[1])
#TODO : przedmot zmika ale jest a jak jest to w 2 miejscajc
    
    def equip_item(self):
        if self.selected_item_for_context_menu:
            
            # Check the type of the item (Armor, Weapon, etc.)
            if isinstance(self.selected_item_for_context_menu, Armor):
                self.selected_item_for_context_menu.wear()
            elif isinstance(self.selected_item_for_context_menu, Weapon):
                
                weapon_slot_index = INVENTORY_SIZE + 1
                weapon_slot_item = self.slots[weapon_slot_index]
                
                if weapon_slot_item:  # If the weapon slot is occupied, swap items
                    self.remove_item(weapon_slot_index)
                    self.add_item(weapon_slot_item, self.original_slot)
                    

                self.selected_item_for_context_menu.equip()
                self.add_item(self.selected_item_for_context_menu, weapon_slot_index)
                self.selected_item_for_context_menu.set_equipped_position()
                print(f"{self.original_slot = } removved" )
                self.remove_item(self.original_slot)
    
    def unequip_item(self):
        if isinstance(self.selected_item_for_context_menu, Weapon) and self.selected_item_for_context_menu.equipped:
            self.selected_item_for_context_menu.equip()
            weapon_slot_index = INVENTORY_SIZE + 1

            # Remove the equipped weapon from the weapon slot
            self.remove_item(self.original_slot)

            # Find the first available slot in the inventory
            empty_slot = None
            for i, slot_item in enumerate(self.slots):
                if i != weapon_slot_index and slot_item is None:
                    empty_slot = i
                    break

            if empty_slot is not None:
                self.add_item(self.selected_item_for_context_menu)