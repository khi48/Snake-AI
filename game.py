import pygame 
import random
# import neat

from head import Head
from body import Body
from apple import Apple

import config_game

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 50)

SNAKE_SPEED = 15

WIN_WIDTH = config_game.WIN_WIDTH
SNAKE_WIDTH = config_game.SNAKE_WIDTH

def update_positions(head, bodies):
    head.update()
    for b in bodies:
        b.update()

def determine_position(h, bodies, a):
    right_to_apple = -1
    forward_to_apple = -1
    distance_front = 1
    distance_left = 1
    distance_right = 1


    if (h.dir == 0):
        # print('going up')

        if (a.x > h.x):
            right_to_apple = 1
        if (a.y < h.y):
            forward_to_apple = 1

        if (h.check_future_collisions(h.x, h.y-SNAKE_WIDTH, bodies)): # front 
            distance_front = -1
        if (h.check_future_collisions(h.x-SNAKE_WIDTH, h.y, bodies)): # left
            distance_left = -1
        if (h.check_future_collisions(h.x+SNAKE_WIDTH, h.y, bodies)): # right
            distance_right = -1
                        


    elif (h.dir == 1):
        # print('going down')

        if (a.x < h.x):
            right_to_apple = 1
        if (a.y > h.y):
            forward_to_apple = 1

        if (h.check_future_collisions(h.x, h.y+SNAKE_WIDTH, bodies)): # front 
            distance_front = -1
        if (h.check_future_collisions(h.x+SNAKE_WIDTH, h.y, bodies)): # left
            distance_left = -1
        if (h.check_future_collisions(h.x-SNAKE_WIDTH, h.y, bodies)): # right
            distance_right = -1
                    

    elif (h.dir == 2):
        # print('going left')
        if (a.y < h.y):
            right_to_apple = 1
        if (a.x < h.x):
            forward_to_apple = 1

        if (h.check_future_collisions(h.x-SNAKE_WIDTH, h.y, bodies)): # front 
            distance_front = -1
        if (h.check_future_collisions(h.x, h.y-SNAKE_WIDTH, bodies)): # left
            distance_left = -1
        if (h.check_future_collisions(h.x, h.y+SNAKE_WIDTH, bodies)): # right
            distance_right = -1

    elif (h.dir == 3):
        # print('going right')

        if (a.y > h.y):
            right_to_apple = 1
        if (a.x > h.x):
            forward_to_apple = 1

        if (h.check_future_collisions(h.x+SNAKE_WIDTH, h.y, bodies)): # front 
            distance_front = -1
        if (h.check_future_collisions(h.x, h.y+SNAKE_WIDTH, bodies)): # left
            distance_left = -1
        if (h.check_future_collisions(h.x, h.y-SNAKE_WIDTH, bodies)): # right
            distance_right = -1

    return distance_front, distance_left, distance_right, right_to_apple, forward_to_apple


def draw_screen(win, head, bodies, apple, distance_list, score, time, gen):
    win.fill((0, 0, 0))
    head.draw(win)

    for b in bodies:
        b.draw(win)

    apple.draw(win)

    if (len(distance_list)):
        text = FONT.render("F: {}".format(distance_list[0]), 1, (255, 255, 255))
        win.blit(text, (head.x, head.y))
        text = FONT.render("L: {}".format(distance_list[1]), 1, (255, 255, 255))
        win.blit(text, (head.x, head.y+(text.get_height()+5)))
        text = FONT.render("R: {}".format(distance_list[2]), 1, (255, 255, 255))
        win.blit(text, (head.x, head.y+(text.get_height()+5)*2))

    text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10))

    text = FONT.render("Time: " + str(time), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10 + 10 + text.get_height()))

    if not(gen == None):
        text = FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
        win.blit(text, (10, 10))

    pygame.display.update()

def single_game(manual, distances=False, net=None, generation=None):
    win = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))
    win.fill((0, 0, 0))

    clock = pygame.time.Clock()
    
    x = random.randrange(SNAKE_WIDTH+SNAKE_WIDTH/2, WIN_WIDTH-(SNAKE_WIDTH+SNAKE_WIDTH/2), SNAKE_WIDTH) 
    y = random.randrange(SNAKE_WIDTH, WIN_WIDTH-(SNAKE_WIDTH), SNAKE_WIDTH) 
    h = Head(WIN_WIDTH, SNAKE_WIDTH,x, y)

    b1 = Body(h.x, h.y+SNAKE_WIDTH, h, SNAKE_WIDTH)
    b2 = Body(b1.x, b1.y+SNAKE_WIDTH, b1, SNAKE_WIDTH)
    bodies = [b1, b2]
    a = Apple(WIN_WIDTH, SNAKE_WIDTH, h, bodies)

    run = True
    score = 0
    time = 200
    while(run):
        clock.tick(SNAKE_SPEED)
        
        time -= 1   

        if (time<=0):
            run = False
            break

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False 
                break


            # Manual Control
            if manual:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        h.KeyMoveUp()
                    elif event.key == pygame.K_DOWN:
                        h.KeyMoveDown()
                    elif event.key == pygame.K_LEFT:
                        h.KeyMoveLeft()
                    elif event.key == pygame.K_RIGHT:
                        h.KeyMoveRight()

        # Automated Control
        # Inputs:
        # head x, head y, boundaries, apple x, apple y # Failed to train after 100 generatations of 100 population -> has no sense of direction
        # distance front, distance down, distance left, distance right, left distance to apple, upwards distance to apple
        if not(manual):

            # Control Code
            inputs = determine_position(h, bodies, a)
            
            output = net.activate((inputs)) #distance_up, distance_down, distance_left, distance_right

            i = output.index(max(output))
            if i == 0:
                h.moveForward()
            elif i == 1:
                h.moveLeft()
            elif i == 2:
                h.moveRight()


        update_positions(h, bodies)

        if (h.check_collisions(bodies)):
            run = False
            break

        if (h.check_apple(a)):
            score += 1
            time = 200
            end = bodies[-1]
            bodies.append(Body(end.p_x, end.p_y, end, SNAKE_WIDTH))
            a.reset(h, bodies)
            # if (score >= 200):
            #     run = False
            #     break


        distance_list = []
        if (distances):
            distance_list = [inputs[0], inputs[1], inputs[2]]

        draw_screen(win, h, bodies, a, distance_list, score, time, generation)


if __name__ == "__main__":
    single_game(True)