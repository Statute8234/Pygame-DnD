import pygame 
import sys

class InputBox:
    def __init__(self, x, y, width, height, textColor, active_color, inactive_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.textColor = textColor
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.base_font = pygame.font.Font(None, 30)
        self.user_text = ''  # Initialize user text as an empty string
        self.input_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.base_font.render(self.user_text, True, self.textColor)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.input_rect)
        screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))  # Offset text surface to avoid clipping

    def update(self):
        # Update text surface based on user input
        self.text_surface = self.base_font.render(self.user_text, True, self.textColor)
        # Limit text input width to the width of the input box
        self.input_rect.w = max(self.width, self.text_surface.get_width() + 10)  # Add 10 pixels for padding
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        # Handle key inputs if active
        elif self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif event.key == pygame.K_RETURN:
                print(self.user_text)  # Example: Print the user input when Enter is pressed
            else:
                if event.unicode:
                    self.user_text += event.unicode
        # Highlight the input box if active
        self.color = self.active_color if self.active else self.inactive_color
