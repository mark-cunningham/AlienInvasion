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
MISSILESPEED = 10
GAMEMISSILES = 20

UFO1SPEED = 5
UFO2SPEED = 3
UFOYMIN = 20
UFOYMAX = SCREENHEIGHT / 2
UFOEXPLODETIME = 20
UFOOFFSCREENTIME = 60
UFOSCORE = 50

RANDUFOCHANCEVERTICAL = 20
RANDUFOCHANCEHORIZONTAL = 100
UFODIRECTIONS = ["L", "R", "U", "D"]

RANDRAY = 200
RANDRAYTIMEMAX = 120
RANDRAYTIMEMIN = 30

BASESPEED = 8

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

    ufo_1_image = pygame.image.load("ufo 1.png").convert()
    ufo_2_image = pygame.image.load("ufo 2.png").convert()
    ufo_1_exploded_image = pygame.image.load("ufo 1 exploded.png").convert()
    ufo_2_exploded_image = pygame.image.load("ufo 2 exploded.png").convert()
    ufo_ray_image_1 = pygame.image.load("ufo ray 1.png").convert()
    ufo_ray_image_2 = pygame.image.load("ufo ray 2.png").convert()

    # Initialise variables

    base_rectangle = base_image.get_rect()
    base_height = base_rectangle.height
    base_width = base_rectangle.width
    base_y = SCREENHEIGHT - base_height - 3
    base_x = SCREENWIDTH / 2

    ufo_rectangle = ufo_1_image.get_rect()
    ufo_width = ufo_rectangle.width
    ufo_height = ufo_rectangle.height

    ray_rectangle = ufo_ray_image_1.get_rect()
    ray_width = ray_rectangle.width

    ufo_1_y = random.randint(UFOYMIN, UFOYMAX)
    ufo_1_loc = [SCREENWIDTH - ufo_width, ufo_1_y]
    ufo_1_dir = "L"
    ufo_1_hit = False

    ufo_2_y = random.randint(UFOYMIN, UFOYMAX)
    ufo_2_loc = [0, ufo_2_y]
    ufo_2_dir = "R"
    ufo_2_hit = False



    missile_firing = False

    ufo_1_explode_count = 0
    ufo_2_explode_count = 0

    ufo_1_offscreen_count = 0
    ufo_2_offscreen_count = 0

    ufo_1_ray_count = 0
    ufo_2_ray_count = 0



    missile_rectangle = missile_image.get_rect()
    missile_width = missile_rectangle.width
    missile_height = missile_rectangle.height
    missile_x = 0
    missile_y = 0

    score = 0
    hi_score = 0
    missiles = GAMEMISSILES
    game_over = False





    while True: # main game loop

        # Keypress events
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_LEFT]:
                base_x = base_x - BASESPEED
                if base_x < 0:
                    base_x = 0
            elif key_pressed[pygame.K_RIGHT]:
                base_x = base_x + BASESPEED
                if base_x > SCREENWIDTH - base_width:
                    base_x = SCREENWIDTH - base_width
            elif key_pressed[pygame.K_SPACE] and missile_firing is False and game_over is False:
                missile_firing = True
                missile_x = base_x + MISSILEPLATFORM
                missile_y = base_y - missile_height
                missiles = missiles - 1
            elif key_pressed[pygame.K_RETURN] and game_over is True:
                game_over = False
                score = 0
                missiles = GAMEMISSILES

            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        game_screen.blit(background_image, [0, 0])




        # Display base
        game_screen.blit(base_image, [base_x, base_y])

        # Display missile
        if missile_firing is True:
            game_screen.blit(missile_fired_image, [missile_x, missile_y])
            missile_y = missile_y - MISSILESPEED
            if missile_y < 0:
                missile_firing = False
                if missiles == 0:
                    game_over = True

        else:
            game_screen.blit(missile_image, [base_x + MISSILEPLATFORM, SCREENHEIGHT - base_height - missile_height - 1])



        missile_rect = pygame.Rect(missile_x, missile_y, missile_width, missile_height)


        # Move UFOs and test for hit
        if ufo_1_hit is False:
            ufo_1_loc, ufo_1_dir = move_ufo(ufo_1_loc, ufo_1_dir, ufo_width, UFO1SPEED)
            ufo_1_rect = pygame.Rect(ufo_1_loc[0], ufo_1_loc[1], ufo_width, ufo_height)
            if missile_rect.colliderect(ufo_1_rect):
                if ufo_1_ray_count == 0:
                    ufo_1_hit = True
                else:
                    missile_firing = False

        if ufo_2_hit is False:
            ufo_2_loc, ufo_2_dir = move_ufo(ufo_2_loc, ufo_2_dir, ufo_width, UFO2SPEED)
            ufo_2_rect = pygame.Rect(ufo_2_loc[0], ufo_2_loc[1], ufo_width, ufo_height)
            if missile_rect.colliderect(ufo_2_rect):
                if ufo_2_ray_count == 0:
                    ufo_2_hit = True
                else:
                    missile_firing = False




        # UFO has been hit so set up explosion
        if ufo_1_hit is True and ufo_1_explode_count == 0 and ufo_1_offscreen_count == 0:
            missile_firing = False
            if ufo_1_explode_count == 0:
                ufo_1_explode_count = UFOEXPLODETIME
                score = score + UFOSCORE * 2
                if missiles == 0:
                    game_over = True

        if ufo_2_hit is True and ufo_2_explode_count == 0 and ufo_2_offscreen_count == 0:
            missile_firing = False
            if ufo_2_explode_count == 0:
                ufo_2_explode_count = UFOEXPLODETIME
                score = score + UFOSCORE
                if missiles == 0:
                    game_over = True


        # Display UFO 1

        if ufo_1_explode_count > 0:
            game_screen.blit(ufo_1_exploded_image, ufo_1_loc)
            ufo_1_explode_count = ufo_1_explode_count - 1
            if ufo_1_explode_count == 0:
                ufo_1_offscreen_count = UFOOFFSCREENTIME
        elif ufo_1_offscreen_count > 0:
            ufo_1_offscreen_count = ufo_1_offscreen_count - 1
            if ufo_1_offscreen_count == 0:
                ufo_1_y = random.randint(UFOYMIN, UFOYMAX)
                ufo_1_loc = [SCREENWIDTH - ufo_width, ufo_1_y]
                ufo_1_dir = "L"
                ufo_1_hit = False
        else:
            game_screen.blit(ufo_1_image, ufo_1_loc)

        # Display UFO 2
        if ufo_2_explode_count > 0:
            game_screen.blit(ufo_2_exploded_image, ufo_2_loc)
            ufo_2_explode_count = ufo_2_explode_count - 1
            if ufo_2_explode_count == 0:
                ufo_2_offscreen_count = UFOOFFSCREENTIME
        elif ufo_2_offscreen_count > 0:
            ufo_2_offscreen_count = ufo_2_offscreen_count - 1
            if ufo_2_offscreen_count == 0:
                ufo_2_y = random.randint(UFOYMIN, UFOYMAX)
                ufo_2_loc = [0, ufo_2_y]
                ufo_2_dir = "R"
                ufo_2_hit = False
        else:
            game_screen.blit(ufo_2_image, ufo_2_loc)

        # Random UFO defence rays
        if ufo_1_ray_count > 0:
            ray_x = ufo_1_loc[0] + (ufo_width - ray_width) / 2
            ray_y = ufo_1_loc[1] + ufo_height
            if (ufo_1_ray_count % 9 == 0 or ufo_1_ray_count % 10 == 0):
                game_screen.blit(ufo_ray_image_2, [ray_x, ray_y])
            else:
                game_screen.blit(ufo_ray_image_1, [ray_x, ray_y])

        if ufo_2_ray_count > 0:
            ray_x = ufo_2_loc[0] + (ufo_width - ray_width) / 2
            ray_y = ufo_2_loc[1] + ufo_height
            if (ufo_2_ray_count % 9 == 0 or ufo_2_ray_count % 10 == 0):
                game_screen.blit(ufo_ray_image_2, [ray_x, ray_y])
            else:
                game_screen.blit(ufo_ray_image_1, [ray_x, ray_y])

        if ufo_1_ray_count == 0 and ufo_1_hit is False:
            random_ray_1 = random.randint(0, RANDRAY)
            if random_ray_1 == 1:
                ufo_1_ray_count = random.randint(RANDRAYTIMEMIN, RANDRAYTIMEMAX)
        elif ufo_1_ray_count > 0:
            ufo_1_ray_count = ufo_1_ray_count - 1

        if ufo_2_ray_count == 0 and ufo_2_hit is False:
            random_ray_2 = random.randint(0, RANDRAY)
            if random_ray_2 == 1:
                ufo_2_ray_count = random.randint(RANDRAYTIMEMIN, RANDRAYTIMEMAX)
        elif ufo_2_ray_count > 0:
            ufo_2_ray_count = ufo_2_ray_count - 1


        # Game over
        if game_over is True:
            if score > hi_score:
                hi_score = score

            display_game_over()


        # Display score board

        score_text = "Score: " + str(score)
        display_scoreboard_data(score_text, "Left")

        missile_text = "Missiles: " + str(missiles)
        display_scoreboard_data(missile_text, "Centre")

        hi_score_text = "Hi: " + str(hi_score)
        display_scoreboard_data(hi_score_text, "Right")

        pygame.display.update()
        clock.tick(30)



def move_ufo(location, direction, ufo_width, speed):
    ufo_x = location[0]
    ufo_y = location[1]
    if direction == "L":
        ufo_x = ufo_x - speed
    elif direction == "R":
        ufo_x = ufo_x + speed
    elif direction == "U":
        ufo_y = ufo_y - speed
    elif direction == "D":
        ufo_y = ufo_y + speed

    if ufo_x < 0 and direction == "L":
        ufo_x = 0
        direction = "R"
    elif ufo_x > SCREENWIDTH - ufo_width and direction == "R":
        ufo_x = SCREENWIDTH - ufo_width
        direction = "L"
    elif ufo_y < UFOYMIN and direction == "U":
        ufo_y = UFOYMIN
        direction = "D"
    elif ufo_y > UFOYMAX and direction == "D":
        ufo_y = UFOYMAX
        direction = "U"
    else:
        if direction == "U" or direction == "D":
            ufo_direction_chance = random.randint(0, RANDUFOCHANCEVERTICAL)
        else:
            ufo_direction_chance = random.randint(0, RANDUFOCHANCEHORIZONTAL)

        if ufo_direction_chance == 1:
            direction = random.choice(UFODIRECTIONS)

    new_location = [ufo_x, ufo_y]

    return new_location, direction



def display_scoreboard_data(scoreboard_text, alignment):
    display_text = font.render(scoreboard_text, True, (LIGHT_YELLOW))
    text_rect = display_text.get_rect()

    if alignment == "Left":
        text_loc = [SCOREBOARDMARGIN, SCOREBOARDMARGIN]

    elif alignment == "Right":
        text_loc = [SCREENWIDTH - text_rect.width - SCOREBOARDMARGIN, SCOREBOARDMARGIN]

    elif alignment == "Centre":
        text_loc = [(SCREENWIDTH - text_rect.width) / 2, SCOREBOARDMARGIN]

    game_screen.blit(display_text, text_loc)



def display_game_over():
    text_line_1 = font.render("GAME OVER", True, WHITE)
    text_rect_1 = text_line_1.get_rect()
    text_line_1_loc = [(SCREENWIDTH - text_rect_1.width) / 2, (SCREENHEIGHT / 2) - 16]

    text_line_2 = font.render("Hit RETURN for new game", True, WHITE)
    text_rect_2 = text_line_2.get_rect()
    text_line_2_loc = [(SCREENWIDTH - text_rect_2.width) / 2, (SCREENHEIGHT / 2) + 16]

    game_screen.blit(text_line_1, text_line_1_loc)
    game_screen.blit(text_line_2, text_line_2_loc)

if __name__ == "__main__":
    main()