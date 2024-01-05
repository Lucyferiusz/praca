import pygame
import sys
import random

# Inicjalizacja Pygame
pygame.init()

# Kolor tła i inicjalizacja ekranu
background_color = (255, 255, 255)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gra RPG")

# Inicjalizacja fontu
font = pygame.font.Font(None, 36)

# Inicjalizacja zmiennych
player_health = 100
player_attack = 10

enemies = [
    {"name": "Przeciwnik 1", "health": 60, "attack": 2},
    {"name": "Przeciwnik 2", "health": 80, "attack": 5},
    {"name": "Przeciwnik 3", "health": 70, "attack": 4},
]

# Grafika postaci i przeciwnika
player_image = pygame.Surface((50, 50))
player_image.fill((0, 128, 0))

enemy_image = pygame.Surface((50, 50))
enemy_image.fill((128, 0, 0))

# Pozycje postaci i przeciwnika na ekranie
player_x = 100
player_y = 200

enemies_positions = [(500, 200), (600, 300), (700, 200)]
enemies_target = [None, None, None]

# Aktualnie wybrany przeciwnik
current_enemy = None

# Funkcja do losowania przeciwnika
def random_enemy():
    return random.choice(enemies)

# Funkcja do wyświetlania tekstu
def draw_text(text, x, y):
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))

# Funkcja do sprawdzania, czy kliknięcie myszy jest na przeciwniku
def is_click_on_enemy(x, y, idx):
    if idx < len(enemies_positions):
        ex, ey = enemies_positions[idx]
        return ex <= x <= ex + 50 and ey <= y <= ey + 50
    return False

# Główna pętla gry
running = True
player_turn = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Lewy przycisk myszy
                x, y = event.pos
                for i in range(len(enemies_positions)):
                    if is_click_on_enemy(x, y, i):
                        idx = i
                        if player_turn and enemies_target[idx] is None:
                            # Szansa na trafienie przeciwnika
                            hit_chance = random.randint(1, 100)
                            if hit_chance <= 90:
                                # Atak gracza
                                damage = player_attack
                                enemy_name = enemies[idx]["name"]
                                enemies[idx]["health"] -= damage
                                if enemies[idx]["health"] <= 0:
                                    enemies_target[idx] = None
                                # Log walki
                                print(f"Gracz zaatakował {enemy_name} i zadał {damage} obrażeń!")
                                player_turn = False
                            else:
                                # Gracz nie trafił
                                print(f"Gracz chybił przeciwnika {enemy_name}!")
                                player_turn = False

    screen.fill(background_color)

    # Renderowanie postaci i przeciwników na ekranie
    screen.blit(player_image, (player_x, player_y))

    # Aktualizacja przeciwników
    for i in range(len(enemies_positions)):
        ex, ey = enemies_positions[i]
        screen.blit(enemy_image, (ex, ey))

    # Wyświetlanie informacji o tura
    if player_turn:
        draw_text("Tura gracza", 50, 50)
    else:
        draw_text("Tura przeciwnika", 50, 50)

    # Wyświetlanie informacji o zdrowiu gracza
    draw_text(f"Zdrowie gracza: {player_health}", 50, 100)

    # Wyświetlanie informacji o przeciwnikach
    for i in range(len(enemies_positions)):
        if enemies_target[i] is None:
            draw_text(f"Przeciwnik {i + 1}", 500, 50 + i * 100)
        else:
            draw_text(f"Przeciwnik {i + 1} (Zablokowany)", 500, 50 + i * 100)
        draw_text(f"Zdrowie przeciwnika: {enemies[i]['health']}", 500, 100 + i * 100)

    if all(enemy['health'] <= 0 for enemy in enemies):
        print("Wygrałeś!")
        running = False

    # Tura przeciwników
    if not player_turn:
        for i in range(len(enemies_positions)):
            if enemies[i]["health"] > 0 and enemies_target[i] is None:
                # Szansa na pominięcie tury przez przeciwnika
                skip_chance = random.randint(1, 100)
                if skip_chance <= 1:
                    print(f"Przeciwnik {enemies[i]['name']} ominął swoją turę!")
                else:
                    
                    # Szansa na trafienie przeciwnika
                    hit_chance = random.randint(1, 100)
                    if hit_chance <= 30:
                        # Atak gracza
                        enemy_damage = enemies[i]["attack"]
                        player_health -= enemy_damage                        
                        
                        print(f"Przeciwnik {enemies[i]['name']} zaatakował gracza i zadał {enemy_damage} obrażeń!")
                    else:
                        # Gracz nie trafił
                        print(f"Przeciwnik {enemies[i]['name']} chybił Gracza!")

                        player_turn = False
                    # Atak przeciwnika


                    # print(f"Przeciwnik {enemies[i]['name']} zaatakował gracza i zadał {enemy_damage} obrażeń!")


        player_turn = True

    pygame.display.flip()

pygame.quit()
sys.exit()
