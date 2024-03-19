import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame_gui
import random
import pygame_textinput
# hand made files
import inputBox
# color
def RANDOM_COLOR():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
# text
class Text:
    def __init__(self, text, font_size, color, position):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.position = position
        self.font = pygame.font.Font(None, self.font_size)  # You can specify a font file or use None for default font
        self.rendered_text = None

    def update(self, new_text):
        self.text = new_text
        self.rendered_text = None  # Clear the rendered text to update it

    def render(self, screen):
        if self.rendered_text is None:
            self.rendered_text = self.font.render(self.text, True, self.color)
        screen.blit(self.rendered_text, self.position)
# button
class Button:
    def __init__(self, x, y, width, height, text, active_color, inactive_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.textColor = BLACK
        self.font_size = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.font_size)
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 2)
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.color = self.active_color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
                    self.color = self.active_color
        else:
            self.color = self.inactive_color

    def reset(self):
        self.clicked = False
        self.color = self.inactive_color
# pause menu
class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title = Text("Menu", 100, BLACK, (50, 50))
        self.buttons = [Button(50,120,200,50,"Resume",RED,BLACK),
                        Button(50,180,200,50,"Options",RED,BLACK),
                        Button(50,240,200,50,"Quit",RED,BLACK),]
        self.backButton = Button(100,120,50,50,"Back",RED,BLACK)
        self.showSettings = False
        self.showLoadScreen = False
        self.settings()
        self.loadScreen()
    
    def loadScreen(self):
        self.loadSlots = [Button(50, (x * 60) + 200, 200, 50, "Slot", RED, BLACK) for x in range(5)]
        
    def settings(self):
        self.sound = Text("Music", 36, BLACK, (230, 200))
        self.sound_slider = Slider(self.screen, 230, 240, 200, 10, min=0, max=100, step=1, initial=100)
        self.sound_output = TextBox(self.screen, 440, 210, 50, 50, fontSize=25)
        self.sound_output.disable()
        self.sound_effects = Text("Sound Effects", 36, BLACK, (230, 300))
        self.sound_effects_slider = Slider(self.screen, 230, 340, 200, 10, min=0, max=100, step=1, initial=100)
        self.sound_effects_output = TextBox(self.screen, 440, 310, 50, 50, fontSize=25)
        self.sound_effects_output.disable()
        self.frame_rate = Text("Frame Rate", 36, BLACK, (230, 400))
        self.frame_rate_slider = Slider(self.screen, 230, 450, 128, 10, min=1, max=64, step=1, initial=64)
        self.frame_rate_output = TextBox(self.screen, 440, 413, 50, 50, fontSize=25)
        self.frame_rate_output.disable()
        self.brightness_text = Text("Brightness", 36, BLACK, (230, 500))
        self.brightness_slider = Slider(self.screen, 230, 550, 200, 10, min=0, max=1.0, step=0.1, initial=1.0)
        self.brightness_output = TextBox(self.screen, 440, 513, 50, 50, fontSize=25)
        self.brightness_output.disable()

    def updateData(self,Background_volume,soundEffect_volume,frameRate,brightness):
        Background_volume = self.sound_slider.getValue()
        soundEffect_volume = self.sound_effects_slider.getValue()
        frameRate = self.frame_rate_slider.getValue()
        brightness = round(self.brightness_slider.getValue(),2)
        return [Background_volume,soundEffect_volume,frameRate,brightness]

    def draw(self):
        self.screen.fill(WHITE)
        self.title.render(self.screen)
        if self.showSettings == False and self.showLoadScreen == False:
            for button in self.buttons:
                button.draw(self.screen)
        # settings
        if (self.showSettings):
            self.backButton.draw(self.screen)
            self.sound.render(self.screen)
            self.sound_slider.draw()
            self.sound_output.draw()
            self.sound_output.setText(self.sound_slider.getValue())

            self.sound_effects.render(self.screen)
            self.sound_effects_slider.draw()
            self.sound_effects_output.draw()
            self.sound_effects_output.setText(self.sound_effects_slider.getValue())

            self.frame_rate.render(self.screen)
            self.frame_rate_slider.draw()
            self.frame_rate_output.draw()
            self.frame_rate_output.setText(self.frame_rate_slider.getValue())

            self.brightness_text.render(self.screen)
            self.brightness_slider.draw()
            self.brightness_output.draw()
            self.brightness_output.setText(round(self.brightness_slider.getValue(),2))
    
    def update(self, screenHeight, screenWidth):
        self.title.position = ((screenHeight / 2) - 100, 50)

        button_x = (screenHeight / 2) - 100
        for button in self.buttons:
            button.x = button_x

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
            if button.color == button.active_color:
                button.textColor = button.active_color
            else:
                button.textColor = button.inactive_color
            if button.clicked:
                button.reset()
                if button.text == "Options":
                    self.showSettings = True
                else:
                    return button.text
            # back button
            pygame_widgets.update(event)
            self.backButton.handle_event(event)
            if self.backButton.clicked:
                if self.showSettings:
                    self.showSettings = False
                else:
                    self.showLoadScreen = False
                self.backButton.reset()
# player sheet
class PlayerSheet:
    def __init__(self, screen):
        self.screen = screen
        self.character_limit = 9
        self.labels = {
            "name": Text("Name:", 36, BLACK, (10, 10)),
            "Level": Text("Level:", 36, BLACK, (10, 40)),
            "strength": Text("Strength:", 36, BLACK, (10, 70)),
            "dexterity": Text("Dexterity:", 36, BLACK, (10, 100)),
            "constitution": Text("Constitution:", 36, BLACK, (10, 130)),
            # Add more labels for other attributes as needed
        }
        self.textBox = inputBox.InputBox(100,10,100,25,BLACK,RED,GREEN)
        self.Resume = Button(50, 540, 50, 50, "Resume", RED, BLACK)

    def draw(self):
        for label in self.labels.values():
            label.render(self.screen)

        self.textBox.draw(self.screen)
        self.Resume.draw(self.screen)
        self.circleButton.draw(self.screen)

    def update(self, screenHeight, screenWidth):
        button_x = (screenHeight / 2) - 50
        self.Resume.x = button_x

        self.textBox.update()

    def handle_event(self, event):
        pygame_widgets.update(event)
        self.textBox.handle_event(event)
        # button
        self.Resume.handle_event(event)
        if self.Resume.clicked:
            self.Resume.reset()
            return self.Resume.text
# menu
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.title = Text("Menu", 100, BLACK, (50, 50))
        self.buttons = [Button(50,120,200,50,"New Game",RED,BLACK),
                        Button(50,180,200,50,"Load Game",RED,BLACK),
                        Button(50,240,200,50,"Continue",RED,BLACK),
                        Button(50,300,200,50,"Options",RED,BLACK),
                        Button(50,360,200,50,"Exit",RED,BLACK)]
        self.backButton = Button(100,120,50,50,"Back",RED,BLACK)
        self.showSettings = False
        self.showLoadScreen = False
        self.settings()
        self.loadScreen()
    
    def loadScreen(self):
        self.loadSlots = [Button(50, (x * 60) + 200, 200, 50, "Slot", RED, BLACK) for x in range(5)]
        
    def settings(self):
        self.sound = Text("Music", 36, BLACK, (230, 200))
        self.sound_slider = Slider(self.screen, 230, 240, 200, 10, min=0, max=100, step=1, initial=100)
        self.sound_output = TextBox(self.screen, 440, 210, 50, 50, fontSize=25)
        self.sound_output.disable()
        self.sound_effects = Text("Sound Effects", 36, BLACK, (230, 300))
        self.sound_effects_slider = Slider(self.screen, 230, 340, 200, 10, min=0, max=100, step=1, initial=100)
        self.sound_effects_output = TextBox(self.screen, 440, 310, 50, 50, fontSize=25)
        self.sound_effects_output.disable()
        self.frame_rate = Text("Frame Rate", 36, BLACK, (230, 400))
        self.frame_rate_slider = Slider(self.screen, 230, 450, 128, 10, min=1, max=64, step=1, initial=64)
        self.frame_rate_output = TextBox(self.screen, 440, 413, 50, 50, fontSize=25)
        self.frame_rate_output.disable()
        self.brightness_text = Text("Brightness", 36, BLACK, (230, 500))
        self.brightness_slider = Slider(self.screen, 230, 550, 200, 10, min=0, max=1.0, step=0.1, initial=1.0)
        self.brightness_output = TextBox(self.screen, 440, 513, 50, 50, fontSize=25)
        self.brightness_output.disable()

    def updateData(self,Background_volume,soundEffect_volume,frameRate,brightness):
        Background_volume = self.sound_slider.getValue()
        soundEffect_volume = self.sound_effects_slider.getValue()
        frameRate = self.frame_rate_slider.getValue()
        brightness = round(self.brightness_slider.getValue(),2)
        return [Background_volume,soundEffect_volume,frameRate,brightness]

    def draw(self):
        self.screen.fill(WHITE)
        self.title.render(self.screen)
        if self.showSettings == False and self.showLoadScreen == False:
            for button in self.buttons:
                button.draw(self.screen)
        # load game
        if (self.showLoadScreen):
            self.backButton.draw(self.screen)
            for loadSlot in self.loadSlots:
                loadSlot.draw(self.screen)
        # settings
        if (self.showSettings):
            self.backButton.draw(self.screen)
            self.sound.render(self.screen)
            self.sound_slider.draw()
            self.sound_output.draw()
            self.sound_output.setText(self.sound_slider.getValue())

            self.sound_effects.render(self.screen)
            self.sound_effects_slider.draw()
            self.sound_effects_output.draw()
            self.sound_effects_output.setText(self.sound_effects_slider.getValue())

            self.frame_rate.render(self.screen)
            self.frame_rate_slider.draw()
            self.frame_rate_output.draw()
            self.frame_rate_output.setText(self.frame_rate_slider.getValue())

            self.brightness_text.render(self.screen)
            self.brightness_slider.draw()
            self.brightness_output.draw()
            self.brightness_output.setText(round(self.brightness_slider.getValue(),2))
    
    def update(self, screenHeight, screenWidth):
        self.title.position = ((screenHeight / 2) - 100, 50)

        button_x = (screenHeight / 2) - 100
        for button in self.buttons:
            button.x = button_x
        # loadslot
        for loadSlot in self.loadSlots:
            loadSlot.x = button_x

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
            if button.color == button.active_color:
                button.textColor = button.active_color
            else:
                button.textColor = button.inactive_color
            if button.clicked:
                button.reset()
                if button.text == "Options":
                    self.showSettings = True
                if button.text == "Load Game":
                    self.showLoadScreen = True
                else:
                    return button.text
            # loadslot
            for loadSlot in self.loadSlots:
                loadSlot.handle_event(event)
                if loadSlot.color == loadSlot.active_color:
                    loadSlot.textColor = loadSlot.active_color
                else:
                    loadSlot.textColor = loadSlot.inactive_color
                if loadSlot.clicked:
                    loadSlot.reset()
            # back button
            pygame_widgets.update(event)
            self.backButton.handle_event(event)
            if self.backButton.clicked:
                if self.showSettings:
                    self.showSettings = False
                else:
                    self.showLoadScreen = False
                self.backButton.reset()
