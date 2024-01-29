import pygame
import sys

class IntroDialog:
    def __init__(self,width,height):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Text Example")

        # Set up fonts
        self.font_size = 24
        self.font = pygame.font.Font(None, self.font_size)

        # Set up colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        # Load background images
        self.bg_player = pygame.image.load("img1.png")
        self.bg_villager = pygame.image.load("img2.png")

        # Create a surface
        self.surface = pygame.Surface((1080, 240))
        self.surface.fill(self.white)

        # Dialog dictionary
        self.dialog = [
        {"name": "Wilhelm", "dialog": "Hej! Gdzie ja jestem? Co to za miejsce?"},
        {"name": "Edmund", "dialog": "... Witaj, Podróżniku. Obudziłeś się nieopodal wioski, sprowadziły Ciebie tu fale."},
        {"name": "Wilhelm", "dialog": "Wioski? Co to za miejsce?"},
        {"name": "Edmund", "dialog": "To jedno z wielu miejsc na Wyspie Azarot. Niestety, to smutna wyspa opanowana przez bandytów i zarządzana przez demona, który czasami budzi się ze snu."},
        {"name": "Wilhelm", "dialog": "Demon? To brzmi groźnie. Musimy coś z tym zrobić!"},
        {"name": "Edmund", "dialog": "Tak, niestety. Ale nie martw się, jest kilka rzeczy, które możemy zrobić. Wiesz, aby przetrwać tutaj, potrzebujesz złota."},
        {"name": "Wilhelm", "dialog": "Złota? Skąd mam wiedzieć, jak zdobyć złoto na tej wyspie?"},
        {"name": "Edmund", "dialog": "Nieopodal jest wioska. Możesz tam pójść i porozmawiać ze sklepikarzem. Zazwyczaj mają zadania, za które płacą złotem. To może być dobry sposób na zarobienie pieniędzy."},
        {"name": "Wilhelm", "dialog": "Dobra, spróbuję. Może tam dowiem się więcej o tym demonie i jak mu przeciwdziałać."},
        {"name": "Edmund", "dialog": "Tak, to dobry pomysł. Powodzenia, Podróżniku!"}
]


        self.end_printing = False

    # Function to render text slowly

    def render_dialog_slowly(self, current_line):
        character = self.dialog[current_line]["name"]
        line = self.dialog[current_line]["dialog"]
        if self.end_printing:
            pass
        else:
            for i in range(len(line) + 1):
                self.end_printing = i + 1 == len(line) + 1
                self.surface.fill(self.white)  # Clear the surface
                text_render = self.font.render(f"{character}: {line[:i]}", True, self.black)  # Render partial text
                text_rect = text_render.get_rect(center=(480, 100))
                self.surface.blit(text_render, text_rect)

                # Display background image based on current_line
                if character == "Wilhelm":
                    self.screen.blit(self.bg_player, (0, 0))
                else:
                    self.screen.blit(self.bg_villager, (0, 0))

                self.screen.blit(self.surface, (0, 480))  # Draw the surface on the screen
                pygame.display.flip()  # Update the display
                pygame.time.delay(100)  # Add a delay (adjust the value as needed)
                pygame.event.pump()  # Allow Pygame to process events


    # Main game loop
    def show(self):
        current_line = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    current_line += 1
                    self.end_printing = False
                    if current_line == len(self.dialog):
                        return

            self.render_dialog_slowly(current_line)  # Call the function to render dialog slowly

            # Control the frame rate
            pygame.time.Clock().tick(60)


# Instantiate and run the IntroDialog class
# intro_dialog = IntroDialog()
# intro_dialog.run()
