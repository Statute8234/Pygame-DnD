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
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), self.outlineSize)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.outlineSize = 2
        else:
            self.outlineSize = 1
# Inventory
class Inventory:
    def __init__(self, x, y, width, height, num_columns, num_rows, padding=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.padding = padding
        self.cells = []
        self.create_cells()
    
    def create_cells(self):
        cell_width = (self.width - self.padding * (self.num_columns - 1)) // self.num_columns
        cell_height = (self.height - self.padding * (self.num_rows - 1)) // self.num_rows
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                cell_x = self.x + col * (cell_width + self.padding)
                cell_y = self.y + row * (cell_height + self.padding)
                cell = InventorySlot(cell_x, cell_y, cell_width, cell_height, GRAY)
                self.cells.append(cell)

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)
    
    def update(self, new_x, new_y, width, height):
        self.x = new_x
        self.y = new_y
        self.width = width
        self.height = height
        cell_width = (self.width - self.padding * (self.num_columns - 1)) // self.num_columns
        cell_height = (self.height - self.padding * (self.num_rows - 1)) // self.num_rows
        # slots
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                idx = row * self.num_columns + col
                self.cells[idx].width = cell_width
                self.cells[idx].height = cell_height
                self.cells[idx].x = self.x + col * (cell_width + self.padding)
                self.cells[idx].y = self.y + row * (cell_height + self.padding)
    
    def handle_event(self, event):
        for cell in self.cells:
            cell.handle_event(event)
