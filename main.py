import pygame as pg
from pygame.locals import *
import sys
from pygame import mixer
from game import *
from record import *
from rules import *

# Initializes pygame library and creates screen
pg.init()
pg.display.set_caption('Main Menu')
screenX = 1800
screenY = 1000
screen = pg.display.set_mode((screenX, screenY))
font = pg.font.SysFont(None, 50)

in_menu = True
click = False
def main_menu():

    # Play Background music
    mixer.music.load('../sound/background.wav')
    mixer.music.play(-1)

    # Loop for being in the main menu
    while in_menu:
        screen.fill((0,0,0))
        mouse_x, mouse_y = pg.mouse.get_pos()

        # If the user clicks play game, launch the game method
        # This method will begin the actual game
        play_button = pg.Rect(700, 390, 450, 120)
        pg.draw.rect(screen, (0, 0, 100), play_button)
        if play_button.collidepoint((mouse_x, mouse_y)):
            if click:
                ninjafruit()

        # If the user clicks rules, launch the rules method
        # This methods will blit a screen explaining the rules
        rules_button = pg.Rect(785, 540, 290, 120)
        pg.draw.rect(screen, (0, 0, 100), rules_button)
        if rules_button.collidepoint((mouse_x, mouse_y)):
            if click:
                rules()

        # If the user clicks record, launch the record method
        # This method will show the top 5 times and usernames
        leaderboard_button = pg.Rect(645, 690, 575, 120)
        pg.draw.rect(screen, (0, 0, 100), leaderboard_button)
        if leaderboard_button.collidepoint((mouse_x, mouse_y)):
            if click:
                record()

        # Blits text to the screen
        text_in_box('NINJA FRUIT', 400, 100, 150)
        text_in_box('PLAY GAME', 730, 400, 70)
        text_in_box('RULES', 815, 550, 70)
        text_in_box('LEADERBOARD', 675, 700, 70)

        # Give users the option to quit the game by presses exit button
        # set click to true if the mouse button has been pressed
        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Update the screen
        pg.display.update()

# Runs the method
main_menu()