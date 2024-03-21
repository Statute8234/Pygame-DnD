import pygame
import random
# color
def RANDOM_COLOR():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
# inventory slot
class InventorySlot():
    def __init__(self, name, pos, image_path, size=(50, 50)):
        self.name = name
        self.pos = pos
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.font = pygame.font.Font(None, 20)
        self.count = 0
    
    def draw(self, screen):
        nameText = self.font.render(str(self.count), True, BLACK)
        screen.blit(self.image, self.rect)
        screen.blit(nameText, self.rect.midright)
# Inventory
class Inventory():
    def __init__(self, pos, image_path, size=(600, 50)):
        self.x, self.y = pos
        self.slots = []
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.slots.append(InventorySlot("coin",(self.rect.left + 10,self.y - 25),r"Assets\coin.png"))
        self.slots.append(InventorySlot("healing potion",(self.rect.left + 80,self.y - 25),r"Assets\game.png"))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for slot in self.slots:
            slot.draw(screen)