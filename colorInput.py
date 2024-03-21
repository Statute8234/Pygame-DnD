import pygame 
import sys
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog
clock = pygame.time.Clock()
# color picker
class ColorPicker:
    def __init__(self, screenWidth, screenHeigh, ):
        self.ui_manager = pygame_gui.UIManager((screenWidth, screenHeigh))
        self.colour_picker_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                text='Pick Colour',
                                manager=self.ui_manager,
                                anchors={'left': 'right',
                                        'right': 'right',
                                        'top': 'bottom',
                                        'bottom': 'bottom'})
        self.time_delta = clock.tick(60) / 1000
        self.colour_picker = None                                    
        self.current_colour = pygame.Color(0, 0, 0)
        self.picked_colour_surface = pygame.Surface((400, 400))
        self.picked_colour_surface.fill(self.current_colour)
    
    def draw(self, screen):
        self.ui_manager.draw_ui(screen)
        
    def update(self):
        self.ui_manager.update(self.time_delta)
        return (self.current_colour[0],self.current_colour[1],self.current_colour[2])

    def handle_event(self, event):
        self.ui_manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.colour_picker_button:
            self.colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                self.ui_manager,
                                                window_title="Change Colour...",
                                                initial_colour=self.current_colour)
            self.colour_picker_button.disable()
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            self.current_colour = event.colour
            self.picked_colour_surface.fill(self.current_colour)
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            self.colour_picker_button.enable()
            self.colour_picker = None
# input box
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
        pygame.draw.rect(screen, self.color, self.input_rect, 2)
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
