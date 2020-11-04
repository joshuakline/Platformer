import pygame as pg
from pygame.locals import *
import sys
from rules import *

# Initialize pygame library and create screen
pg.init()
pg.display.set_caption('Record')
screenX = 1800
screenY = 1000
screen = pg.display.set_mode((screenX, screenY))
font = pg.font.SysFont(None, 50)

def record():
    # Open the record text file
    fread = open('record.txt', 'r')
    record_names = []
    record_times = []
    every_other = 1
    # Add all the times to one array, and the names to another
    for line in fread:
        if every_other % 2 == 0:
            record_times.append(int(line.strip('\n')))    
        else:
            record_names.append(line.strip('\n'))
        every_other += 1
    fread.close()

    # Create a library where the keys are the times and the values are the usernames
    leader_board = {}
    index = 0
    for time in record_times:
        leader_board[time] = record_names[index]
        index += 1

    # Set a few arbitrarily large values as the record times
    first = 10000000000
    second = 10000000000
    third = 10000000000
    fourth = 10000000000
    fifth = 10000000000

    # Look at each key in the library, and substitute the top 5 scores for the arbitrary values above
    for key in leader_board:
        if key <= first:
            fifth = fourth
            fourth = third
            third = second
            second = first
            first = key
        elif key <= second:
            fifth = fourth
            fourth = third
            third = second
            second = key
        elif key <= third:
            fifth = fourth
            fourth = third
            third = key
        elif key <= fourth:
            fifth = fourth
            fourth = key
        elif key<= fifth:
            fifth = key

    # Loop for blitting the record board
    click = False
    in_record = True
    while in_record:
        screen.fill((0,0,0))
        mouse_x, mouse_y = pg.mouse.get_pos()

        # If the user presses the main menue button it breaks out of this loop, therefore returning to main menu
        return_button = pg.Rect(20, 25, 175, 60)
        pg.draw.rect(screen, (0, 0, 100), return_button)
        if return_button.collidepoint((mouse_x, mouse_y)):
            if click:
                in_record = False

        # Blit the top 5 scores to the screen
        text_in_box('Main Menu', 30, 30, 30)
        text_in_box('TOP 5 RECORDS', 500, 100, 100)
        text_in_box(f'1. {leader_board[first]} - {first}s', 600, 300, 50)
        text_in_box(f'2. {leader_board[second]} - {second}s', 600, 400, 50)
        text_in_box(f'3. {leader_board[third]} - {third}s', 600, 500, 50)
        text_in_box(f'4. {leader_board[fourth]} - {fourth}s', 600, 600, 50)
        text_in_box(f'5. {leader_board[fifth]} - {fifth}s', 600, 700, 50)

        # Allow user to quit using exit button
        # Set click to True if user presses mouse button
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

