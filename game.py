# Runs the Game Loop
def ninjafruit():
    import math
    import pygame as pg
    import sys
    from pygame import mixer
    from leaderboard import leaderboard

    # Game methods

    # Checks if the  euclidian distance between foe and player is less than 40 pixels
    def iscollision(playerX, playerY, foeX, foeY):
        distance = math.sqrt(((playerX) - (foeX))**2 + (playerY - foeY)**2)
        if distance < 40:
            return True

    # Defines the ovement of the shurikens
    def stars_move(stars):
        foes[stars][0] += foes[stars][2]
        if foes[stars][0] > screenX:
            foes[stars][0] = 0

    # Defines the movement of the dragon and bad guy ninja
    # Lets user input axis of travel (x or y)
    def foe_movement(foe, travel_axis, reverse_name):
        if reverse_name:
            foes[foe][travel_axis] += foes[foe][2]
        else:
            foes[foe][travel_axis] -= foes[foe][2]

    # Puts the bananas back to their original position when the player dies
    # references the arrays / libraries where current and reset positions are stored
    def reset_banana():  
        i = 0
        for banana in bananas:
            bananas[banana][0] = bananas_reset[i][0]
            bananas[banana][1] = bananas_reset[i][1]
            i += 1

    # Initialize the pg library
    pg.init()

    # Screen size
    screenX = 1800
    screenY = 1000

    # Creates the screen
    # Game title
    # Background
    # Loads all the images
    # Start tracking time
    screen = pg.display.set_mode((screenX, screenY))
    pg.display.set_caption("My First Platformer")
    background = pg.image.load('../images/building.jpg')
    player_model = pg.image.load('../images/ninja.png')
    flag = pg.image.load('../images/flag.png')
    bad_guy = pg.image.load('../images/ninja (2).png')
    stars1 = pg.image.load('../images/shuriken (2).png')
    stars2 = pg.image.load('../images/shuriken (2).png')
    bananasImg = pg.image.load('../images/bananas.png')
    dragon = pg.image.load('../images/dragon.png')
    start_time = pg.time.get_ticks()

    # Flag location
    flagX = 1630
    flagY = 136

    # Player character
    playerX = 50
    playerY = 936
    prev_playerX = 0
    prev_playerY = 1000
    player_speed = 5
    player_size = 64
    jump = False
    fall = False
    playerY_before_jump = 0

    # Bananas
    # Location to reset to when player dies
    bananas_reset =  [[120, 800], [1700, 400], [120, 128], [870, 428]]
    # Current location of bananas
    bananas = {
        # bananax : [x,    y]
        'bananas1': [120, 800],
        'bananas2': [1700, 400], 
        'bananas3': [120, 128], 
        'bananas4': [870, 428]
    }
    banana_count = 0

    # Foes array [x, y, speed]
    foes = {
        "stars1" : [0, 400, 5], 
        "stars2" : [-300, 820, 6], 
        "bad_guy" : [1600, 936, 4], 
        "dragon" : [450, 500, 3]
    }
    bad_guy_reverse = False
    dragon_reverse = False

    # Making boxes to platform onto
    color = (0, 0, 0)
    thickness = 3
    boxes = {
        #boxx :  [ x,   y,   w,  h]
        "box1" : [100, 872, 100, 20], #banana box
        "box2" : [400, 872, 100, 20], 
        "box3" : [250, 300, 50, 20],
        "box4" : [700, 750, 80, 20],
        "box5" : [400, 400, 80, 20], #bridge from banana to top left
        "box6" : [1200, 600, 80, 20],
        "box7" : [850, 500, 100, 20], #banana box
        "box8" : [1200, 520, 80, 20],
        "box9" : [1350, 400, 80, 20],
        "box10" : [1050, 200, 80, 20], #top right bridge
        "box11" : [700, 200, 80, 20], #top left bridge
        "box12" : [100, 200, 100, 20], #banana box
        "box13" : [1600, 200, 80, 20], #flag box
    }
    for box in boxes:
        pg.draw.rect(background, color, boxes[box], thickness)

    # Game loops iterates until user presses exit
    gameon = True
    while gameon:
        # Keeps track of current time
        current_time = pg.time.get_ticks()
        # Checks key events
        for event in pg.event.get():
            # Check if player is trying to exit the game
            if event.type == pg.QUIT:
                gameon = False
            # Check if player is pressing any keys
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if jump == False:
                        jump_sound = mixer.Sound('../sound/jump.wav')
                        jump_sound.play()
                        playerY_before_jump = playerY
                        jump = True
                        jump_start_time = pg.time.get_ticks()

        # Checks which keys are pressed, changes player X coordinate if L/R
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            playerX -= player_speed
        if keys[pg.K_RIGHT]:
            playerX += player_speed
        
        # Logic for performing a jump
        if jump == True:
            fall = False
            time_passed = (current_time - jump_start_time)/1000
            quadresult = 720*(time_passed - 0.5)**2 - 180
            playerY = (playerY_before_jump + quadresult)
            if playerY >= screenY - player_size + 1:
                jump = False
                playerY = screenY - player_size

        # Logic for falling after walking off a platform
        for box in boxes:
            if jump == False \
                and playerY == boxes[box][1] - 64 \
                and ((playerX +32) in range((boxes[box][0] - 10), boxes[box][0]) \
                or (playerX +32) in range((boxes[box][0] + boxes[box][2]), (boxes[box][0] + boxes[box][2] + 10))):
                fall_start_time = pg.time.get_ticks()
                playerY_before_fall = playerY
                fall = True

        if fall == True:
            time_passed = (current_time - fall_start_time)/1000
            quadresult = 720*(time_passed)**2
            playerY = (playerY_before_fall + quadresult)
            if playerY >= screenY - player_size + 1:
                fall = False
                playerY = screenY - player_size

        # Map boundaries (must come after jump logc)
        if playerX <= 0:
            playerX = 0
        if playerX >= screenX - player_size:
            playerX = screenX - player_size

        # Box collision
        for box in boxes: 
            if (prev_playerY + 64) < boxes[box][1] \
                and boxes[box][1] < (playerY + 64) \
                and boxes[box][0] < (playerX +32) \
                and (playerX + 32) < (boxes[box][0] + boxes[box][2]):
                playerY = boxes[box][1] - 64
                landing_sound = mixer.Sound('../sound/landing.wav')
                landing_sound.play()
                jump = False
                fall = False

        # Foe collision
        for foe in foes:
            if iscollision(playerX, playerY, foes[foe][0], foes[foe][1]):
                kill = mixer.Sound('../sound/kill.wav')
                kill.play()
                playerX = 50
                playerY = 936  
                banana_count = 0 
                reset_banana()
                jump = False
                fall = False

        # Banana Collision
        for banana in bananas:
            if iscollision(playerX, playerY, bananas[banana][0], bananas[banana][1]):
                chomp_sound = mixer.Sound('../sound/chomp.wav')
                chomp_sound.play()
                bananas[banana][0] = -200
                bananas[banana][1] = -200
                banana_count += 1
    

        # Check if the player has won the game
        if iscollision(playerX, playerY, flagX, flagY) and banana_count == len(bananas):
            end_time = pg.time.get_ticks()
            total_time = round((end_time - start_time)/1000)
            leaderboard(total_time)
            gameon = False

        # Bad Guy Movement
        foe_movement('bad_guy', 0, bad_guy_reverse)
        if foes['bad_guy'][0] <= 100:
            bad_guy_reverse = True
        elif foes['bad_guy'][0] >= screenX - player_size:
            bad_guy_reverse = False
        
        # Dragon Movement
        foe_movement('dragon', 1, dragon_reverse)
        if foes['dragon'][1] > 750: 
            dragon_reverse = False
        elif foes['dragon'][1] < 50:
            dragon_reverse = True
        
        # Stars Movement
        stars_move('stars1')
        stars_move('stars2')

        # Closing logic
        prev_playerX = playerX
        prev_playerY = playerY

        # Draw the Background and items in layers
        screen.blit(background, (0, 0))
        screen.blit(flag, (flagX, flagY))
        screen.blit(player_model, (playerX, playerY))
        screen.blit(bad_guy, (foes['bad_guy'][0], foes['bad_guy'][1]))
        screen.blit(dragon, (foes['dragon'][0], foes['dragon'][1]))
        screen.blit(stars1, (foes['stars1'][0], foes['stars1'][1]))
        screen.blit(stars2, (foes['stars2'][0], foes['stars2'][1]))
        for banana in bananas:
            screen.blit(bananasImg, (bananas[banana][0], bananas[banana][1]))
        
        # Upddate the screen at the very end of each iteration of the game loop
        pg.display.update()