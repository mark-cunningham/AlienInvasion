# Alien Invasio

import pygame, sys
from pygame.locals import *
import random

# Define the colours
BLACK = (0, 0, 0)
LIGHT_YELLOW = (255, 255, 204)
WHITE = (255, 255, 255)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
SCOREBOARDMARGIN = 4

MISSILEPLATFORM = 30
MISSILESPEED = 5

UFOSPEED = 5
RANDOMUFOMIN = 20
RANDOMUFOMAX = 150

# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Alien Invasion")
pygame.key.set_repeat(10, 20)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)

def main():


    # Load images
    base_image = pygame.image.load("base.png").convert()
    background_image = pygame.image.load("background.png").convert()
    missile_image = pygame.image.load("missile.png").convert()
    missile_fired_image = pygame.image.load("missile_fired.png").convert()

    ufo_image = pygame.image.load("ufo.png").convert()
    ufo_explode_image = pygame.image.load("ufo_exploded.png").convert()

    # Initialise variables

    base_rectangle = base_image.get_rect()
    base_height = base_rectangle.height
    base_y = SCREENHEIGHT - base_height - 3
    base_x = 180

    ufo_rectangle = ufo_image.get_rect()
    ufo_width = ufo_rectangle.width
    ufo_height = ufo_rectangle.height
    ufo_1_y = random.randint(RANDOMUFOMIN, RANDOMUFOMAX)

    ufo_1_loc = [SCREENWIDTH - ufo_width, ufo_1_y]
    ufo_1_dir = "L"
    ufo_1_hit = False



    missile_firing = False

    ufo_explode_count = 0



    missile_rectangle = missile_image.get_rect()
    missile_width = missile_rectangle.width
    missile_height = missile_rectangle.height
    missile_x = 0
    missile_y = 0

    score = 0
    missiles = 10
    game_over = False





    while True: # main game loop

        # Keypress events
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_LEFT]:
               base_x = base_x - 5
               if base_x < 10:
                   base_x = 10
            elif key_pressed[pygame.K_RIGHT]:
               base_x = base_x + 5
               if base_x > 350:
                   base_x = 350
            elif key_pressed[pygame.K_SPACE] and missile_firing is False and game_over is False:
                missile_firing = True
                missile_x = base_x + MISSILEPLATFORM
                missile_y = base_y - missile_height
                missiles = missiles - 1
            elif key_pressed[pygame.K_RETURN] and game_over is True:
                game_over = False
                score = 0
                missiles = 10

            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        game_screen.blit(background_image, [0, 0])




        # Display missile
        if (missile_firing is True):
            game_screen.blit(missile_fired_image, [missile_x, missile_y])
            missile_y = missile_y - MISSILESPEED
            if (missile_y < 0):
                missile_firing = False
                if (missiles == 0):
                    game_over = True

        else:
            game_screen.blit(missile_image, [base_x + MISSILEPLATFORM, SCREENHEIGHT - base_height - missile_height - 1])


        game_screen.blit(base_image, [base_x, base_y])



        # Move UFO
        #if ufo_1_direction
        if ufo_1_hit is False:
            ufo_1_loc = move_ufo(ufo_1_loc, ufo_1_dir)
        """ufo_1_x = ufo_1_x - 5
        if (ufo_1_x < 0):
            ufo_1_x = SCREENWIDTH - ufo_width
            ufo_y = random.randint(RANOMUFOMIN, RANDOMUFOMAX)
            ufo_explode_count= 0

        # Check if missile hit UFO


        if (missile_x > ufo_1_x) and (missile_x + missile_width < ufo_1_x + ufo_width) and (missile_y > ufo_y) and (missile_y + missile_height < ufo_y + ufo_height):
            missile_firing = False
            if(ufo_explode_count == 0):
                ufo_explode_count = 10
                score = score + 10
                if (missiles == 0):
                    game_over = True"""

        ufo_1_hit = check_hit_ufo(missile_x, missile_y, missile_width, missile_height, ufo_1_loc, ufo_width, ufo_height)
        if ufo_1_hit and missile_firing is True:
            missile_firing = False
            if (ufo_explode_count == 0):
                ufo_explode_count = 20
                score = score + 10
                if (missiles == 0):
                    game_over = True

        # Display UFO
        if (ufo_explode_count == 0):
            game_screen.blit(ufo_image, ufo_1_loc)
        else:
            game_screen.blit(ufo_explode_image, ufo_1_loc)
            ufo_explode_count = ufo_explode_count - 1


        # Game over
        if (game_over is True):
            display_game_over()

        score_text = "Score: " + str(score)
        display_scoreboard_data(score_text, "Left")

        missile_text = "Missiles: " + str(missiles)
        display_scoreboard_data(missile_text, "Right")

        pygame.display.update()
        clock.tick(30)


def move_ufo(location, direction):
    ufo_x = location[0]
    ufo_y = location[1]
    if direction == "L":
        ufo_x = ufo_x - UFOSPEED

    new_location = [ufo_x, ufo_y]
    return new_location

def check_hit_ufo(missile_x, missile_y, missile_width, missile_height, ufo_loc, ufo_width, ufo_height):
    ufo_x = ufo_loc[0]
    ufo_y = ufo_loc[1]
    ufo_hit = False

    if (missile_x > ufo_x) and (missile_x + missile_width < ufo_x + ufo_width) and (missile_y > ufo_y) and (
            missile_y + missile_height < ufo_y + ufo_height):
        ufo_hit = True

    return ufo_hit



def display_scoreboard_data(scoreboard_text, alignment):
    display_text = font.render(scoreboard_text, True, (LIGHT_YELLOW))
    text_rect = display_text.get_rect()

    if alignment == "Left":
        text_loc = [SCOREBOARDMARGIN, SCOREBOARDMARGIN]

    elif alignment == "Right":
        text_loc = [SCREENWIDTH - text_rect.width - SCOREBOARDMARGIN, SCOREBOARDMARGIN]

    game_screen.blit(display_text, text_loc)



def display_game_over():
    text_line_1 = font.render("GAME OVER", True, (WHITE))
    text_rect_1 = text_line_1.get_rect()
    text_line_1_loc = [(SCREENWIDTH - text_rect_1.width) / 2, (SCREENHEIGHT / 2) - 16]

    text_line_2 = font.render("Hit RETURN for new game", True, (WHITE))
    text_rect_2 = text_line_2.get_rect()
    text_line_2_loc = [(SCREENWIDTH - text_rect_2.width) / 2, (SCREENHEIGHT / 2) + 16]

    game_screen.blit(text_line_1, text_line_1_loc)
    game_screen.blit(text_line_2, text_line_2_loc)





if __name__ == "__main__":
    main()