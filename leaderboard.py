def leaderboard(time):
    import pygame as pg
    import sys
    from rules import text_in_box

    # Initialize the pygame library, and define the screen
    pg.init()
    pg.display.set_caption('Main Menu')
    screenX = 1800
    screenY = 1000
    screen = pg.display.set_mode((screenX, screenY))
    font = pg.font.SysFont(None, 50)

    # Leader board loop
    click = False
    in_leaderboard = True
    active_input = False
    name = ''
    while in_leaderboard:
        screen.fill((0,0,0))
        mouse_x, mouse_y = pg.mouse.get_pos()
        
        # Creates a box for the user to cick on
        # Once clicked, active input allows the user to type their username
        input_button = pg.Rect(675, 410, 400, 60)
        pg.draw.rect(screen, (0, 0, 100), input_button)
        if input_button.collidepoint((mouse_x, mouse_y)):
            if click:
                active_input = True

        # Blits text to the screen
        text_in_box(f'YOU BEAT THE GAME IN {time}s!', 100, 200, 100)
        text_in_box("Username:", 400, 400, 50)
        text_in_box(name, 700, 400, 50)

        # Registers keystrokes
        click = False
        for event in pg.event.get():
            # Closes the program if exit button is clicked
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Sets click to true if mouse is clicked
            # This alows us to turn active input to true if click is on user input box
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            # Allows user to type in name if active input is set to true
            if event.type == pg.KEYDOWN:
                if active_input:
                    # Appends the users input and time to the record txt file
                    if event.key == pg.K_RETURN:
                        fappend = open('record.txt', 'a')
                        fappend.write(f"{name}\n")
                        fappend.write(f"{str(time)}\n")
                        fappend.close
                        in_leaderboard = False
                    elif event.key == pg.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
        pg.display.update()