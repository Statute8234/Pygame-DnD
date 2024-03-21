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
GRAY = (128,128,128)
# Inventory Slot
class InventorySlot:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.outlineSize = 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height), self.outlineSize)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.outlineSize = 2
        else:
            self.outlineSize = 1
# Inventory
class Inventory:
    def __init__(self, x, y, width, height, num_columns, num_rows,  padding=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.padding = padding
        self.cell_width = (width - padding * (num_columns - 1)) // num_columns
        self.cell_height = (height - padding * (num_rows - 1)) // num_rows
        self.cells = []
        self.create_cells()
    
    def create_cells(self):
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                cell_x = self.x + col * (self.cell_width + self.padding)
                cell_y = self.y + row * (self.cell_height + self.padding)
                cell_rect = InventorySlot(cell_x, cell_y, self.cell_width, self.cell_height, GRAY)
                self.cells.append(cell_rect)

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)
    
    def update(self, new_x, new_y, width, height):
        self.cell_width = (width - self.padding * (self.num_columns - 1)) // self.num_columns
        self.cell_height = (height - self.padding * (self.num_rows - 1)) // self.num_rows
        self.x = new_x
        self.y = new_y
        self.cells = []
        self.create_cells()
    
    def handle_event(self, event):
        for cell in self.cells:
            cell.handle_event(event)
