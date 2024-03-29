import pygame
import pygame.sprite
import sys
import random
# hand made files
import menu
# screen
pygame.init()
screenWidth, screenHeight = 600, 600
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
pygame.display.flip()
# color
def RANDOM_COLOR():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
# menus
mainMenu = menu.Menu(screen)
playerSheet = menu.PlayerSheet(screen)
pauseMenu = menu.PauseMenu(screen)
# buttons
pauseButton = menu.Button(10,10,100,50,"Pause",RED,BLACK)
playerSheetButton = menu.Button(120,10,100,50,"Player Sheet",RED,BLACK)
# display functions
brightness = 1.0
frameRate = 64
Background_volume = 1.0
soundEffect_volume = 1.0
show_MainMenu = True
show_MapMenu = False
# brightness
def adjust_brightness(surface, brightness):
    overlay = pygame.Surface((screenWidth, screenHeight))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(255 - int(brightness * 255))
    surface.blit(overlay, (0, 0))
# loop
show_pauseMenu = False
show_playerSheet = False
show_mainmenu = True
running = True
def main():
    global screenWidth, screenHeight, running, show_mainmenu, show_playerSheet, show_pauseMenu, Background_volume,soundEffect_volume,frameRate,brightness
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and show_mainmenu == False:
                    show_pauseMenu = True
                    show_playerSheet = False
            elif event.type == pygame.VIDEORESIZE:
                screenWidth, screenHeight = event.size
            # main menu events
            if show_mainmenu:
                mainMenu.handle_event(event)
                if mainMenu.handle_event(event) == "Exit":
                    running = False
                    sys.exit()
                if mainMenu.handle_event(event) == "New Game":
                    show_mainmenu = False
                    show_playerSheet = True
                if mainMenu.handle_event(event) == "Continue":
                    show_mainmenu = False
                    show_playerSheet = False
            # pause menu
            if show_pauseMenu:
                pauseMenu.handle_event(event)
                if pauseMenu.handle_event(event) == "Resume":
                    show_pauseMenu = False
                if pauseMenu.handle_event(event) == "Quit":
                    show_pauseMenu = False
                    show_mainmenu = True
            # player sheet
            if show_playerSheet:
                playerSheet.handle_event(event)
                if playerSheet.handle_event(event) == "Resume":
                    show_playerSheet = False
            if not(show_MainMenu and show_pauseMenu) and show_playerSheet == False:
                playerSheetButton.handle_event(event)
                if playerSheetButton.clicked:
                    playerSheetButton.reset()
                    show_playerSheet = True
                pauseButton.handle_event(event)
                if pauseButton.clicked:
                    pauseButton.reset()
                    show_pauseMenu = True
        # screen
        screen.fill(WHITE)
        if show_mainmenu:
            Background_volume,soundEffect_volume,frameRate,brightness = mainMenu.updateData(Background_volume, soundEffect_volume, frameRate, brightness)
            mainMenu.update(screenWidth, screenHeight)
            mainMenu.draw()
        elif show_playerSheet:
            playerSheet.update(screenWidth, screenHeight)
            playerSheet.draw()
        elif show_pauseMenu:
            Background_volume,soundEffect_volume,frameRate,brightness = pauseMenu.updateData(Background_volume, soundEffect_volume, frameRate, brightness)
            pauseMenu.update(screenWidth, screenHeight)
            pauseMenu.draw()
        else:
            pauseButton.draw(screen)
            playerSheetButton.draw(screen)
        # update
        adjust_brightness(screen, brightness)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(frameRate)
# main
if __name__ == "__main__":
    main()
