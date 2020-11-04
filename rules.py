import pygame as pg
from pygame.locals import *
import sys

# Initialize the pygame library and create the screen
pg.init()
pg.display.set_caption('Rules')
screenX = 1800
screenY = 1000
screen = pg.display.set_mode((screenX, screenY))
font = pg.font.SysFont(None, 50)

# Allows user to pass a string, x and y coords, and a size for text to blit to the screen
# This method gets called on in many of the other files
def text_in_box(message, x, y, size):
    pg.font.init()
    myfont = pg.font.SysFont('Comic Sans MS', size)
    textsurface = myfont.render(message, False, (220, 100, 0))
    screen.blit(textsurface, (x, y))

# This methods runs the loop that will display the rules
def rules():
    click = False
    in_rules = True
    while in_rules:
        screen.fill((0,0,0))
        mouse_x, mouse_y = pg.mouse.get_pos()

        # Allows user to click return to main menu, which breaks out of the current loop
        return_button = pg.Rect(20, 25, 175, 60)
        pg.draw.rect(screen, (0, 0, 100), return_button)
        if return_button.collidepoint((mouse_x, mouse_y)):
            if click:
                in_rules = False

        # Blits all of the rules an headings to the screen
        text_in_box('Main Menu', 30, 30, 30)
        text_in_box('RULES', 200, 200, 100)
        text_in_box('1. Collect all 4 Bananas', 100, 400, 50)
        text_in_box('2. Reach the Flag to Win', 100, 500, 50)
        text_in_box('3. Restart if hit by Foe', 100, 600, 50)
        text_in_box('4. Try to Beat the High Score', 100, 700, 50)

        # Blits all the controls to the screen
        text_in_box('CONTROLS', 1050, 200, 100)
        text_in_box('L/R ARROWS - move', 1080, 400, 50)
        text_in_box('SPACE - jump', 1080, 500, 50)

        # Allows user to press red exit button to terminate the program
        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            # Sets click to true if mouse is clicked
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Updated the screen
        pg.display.update()