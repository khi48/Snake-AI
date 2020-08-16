''' 
    Game to output result of neural network training

    If this file is run as the main, user can play a regular game of snake
'''

import pygame 
import random

from head import Head
from body import Body
from apple import Apple

import config_game

# initialising pygame
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 50)

# loading configuration variables
WIN_WIDTH = config_game.WIN_WIDTH
SNAKE_WIDTH = config_game.SNAKE_WIDTH
SNAKE_SPEED = config_game.SNAKE_SPEED
MANUAL_SNAKE_SPEED = config_game.MANUAL_SNAKE_SPEED


# moving head and body position 
def update_positions(head, bodies):
    head.update()
    for b in bodies:
        b.update()

# determining position variables to pass to neural network 
def determine_position(h, bodies, a):

    # determing apple position relative to the direction that the snake is heading 
    right_to_apple = -1 # (-1 for left of the head, 0 for in line, 1 for right)
    forward_to_apple = -1 # (-1 for behind of the head, 0 for in line, 1 for forward)

    # determing obstacle position relative to head (1 if there is no obstacle in next square, -1 if there is an obstacle in next square)
    # the position is relative to the direction that the snake is heading. 
    distance_front = 1 
    distance_left = 1
    distance_right = 1

    # depending on the direction that the snake is heading, the variables are calculated differently

    # if snake is heading upwards
    if (h.dir == 0):
        # print('going up')
        if (a.x > h.x):
            right_to_apple = 1
        elif (a.x == h.x):
            right_to_apple = 0

        if (a.y < h.y):
            forward_to_apple = 1
        elif (a.y == h.y):
            forward_to_apple = 0

        if (h.check_future_collisions(h.x, h.y-SNAKE_WIDTH, bodies)): # front 
            distance_front = -1
        if (h.check_future_collisions(h.x-SNAKE_WIDTH, h.y, bodies)): # left
            distance_left = -1
        if (h.check_future_collisions(h.x+SNAKE_WIDTH, h.y, bodies)): # right
            distance_right = -1


    # if snake is heading down
    elif (h.dir == 1):
        # print('going down')
        if (a.x < h.x):
            right_to_apple = 1
        elif (a.x == h.x):
            right_to_apple = 0

        if (a.y > h.y):
            forward_to_apple = 1
        elif (a.y == h.y):
            forward_to_apple = 0

        if (h.check_future_collisions(h.x, h.y+SNAKE_WIDTH, bodies)): # front 
            distance_front = -1
        if (h.check_future_collisions(h.x+SNAKE_WIDTH, h.y, bodies)): # left
            distance_left = -1
        if (h.check_future_collisions(h.x-SNAKE_WIDTH, h.y, bodies)): # right
            distance_right = -1
                    

    # if snake is heading left
    elif (h.dir == 2):
        # print('going left')
        if (a.y < h.y):
            right_to_apple = 1
        elif (a.y == h.y):
            right_to_apple = 0

        if (a.x < h.x):
            forward_to_apple = 1
        elif (a.x == h.x):
            forward_to_apple = 0

        if (h.check_future_collisions(h.x-SNAKE_WIDTH, h.y, bodies)): # front 
            distance_front = -1
        if (h.check_future_collisions(h.x, h.y-SNAKE_WIDTH, bodies)): # left
            distance_left = -1
        if (h.check_future_collisions(h.x, h.y+SNAKE_WIDTH, bodies)): # right
            distance_right = -1


    # if snake is heading right
    elif (h.dir == 3):
        # print('going right')
        if (a.y > h.y):
            right_to_apple = 1
        elif (a.y == h.y):
            right_to_apple = 0

        if (a.x > h.x):
            forward_to_apple = 1
        elif (a.x == h.x):
            forward_to_apple = 0

        if (h.check_future_collisions(h.x+SNAKE_WIDTH, h.y, bodies)): # front 
            distance_front = -1
        if (h.check_future_collisions(h.x, h.y+SNAKE_WIDTH, bodies)): # left
            distance_left = -1
        if (h.check_future_collisions(h.x, h.y-SNAKE_WIDTH, bodies)): # right
            distance_right = -1

    return distance_front, distance_left, distance_right, right_to_apple, forward_to_apple

# drawing snake, apple and text to the screen
def draw_screen(win, head, bodies, apple, distance_list, score, time, gen):
    win.fill((0, 0, 0))
    head.draw(win)

    for b in bodies:
        b.draw(win)

    apple.draw(win)

    # if (len(distance_list)):
    #     text = FONT.render("F: {}".format(distance_list[0]), 1, (255, 255, 255))
    #     win.blit(text, (head.x, head.y))
    #     text = FONT.render("L: {}".format(distance_list[1]), 1, (255, 255, 255))
    #     win.blit(text, (head.x, head.y+(text.get_height()+5)))
    #     text = FONT.render("R: {}".format(distance_list[2]), 1, (255, 255, 255))
    #     win.blit(text, (head.x, head.y+(text.get_height()+5)*2))

    text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10))

    text = FONT.render("Time: " + str(time), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10 + 10 + text.get_height()))

    # draw the generation number if being trained automatically
    if not(gen == None):
        text = FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
        win.blit(text, (10, 10))

    pygame.display.update()


# generate the snake game 
def single_game(manual, distances=False, net=None, generation=None):
    win = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))
    win.fill((0, 0, 0))

    clock = pygame.time.Clock()

    # generating head of snake
    x = random.randrange(SNAKE_WIDTH+SNAKE_WIDTH/2, WIN_WIDTH-(SNAKE_WIDTH+SNAKE_WIDTH/2), SNAKE_WIDTH) 
    y = random.randrange(SNAKE_WIDTH, WIN_WIDTH-(SNAKE_WIDTH), SNAKE_WIDTH) 
    h = Head(WIN_WIDTH, SNAKE_WIDTH,x, y)

    # generating body of snake
    b1 = Body(h.x, h.y+SNAKE_WIDTH, h, SNAKE_WIDTH)
    b2 = Body(b1.x, b1.y+SNAKE_WIDTH, b1, SNAKE_WIDTH)
    bodies = [b1, b2]

    # generating apple for snake to eat
    a = Apple(WIN_WIDTH, SNAKE_WIDTH, h, bodies)

    run = True
    score = 0
    time = 200
    while(run):

        # setting clock speed. Slower if the game is being manually run
        if manual:
            clock.tick(MANUAL_SNAKE_SPEED)
        else:
            clock.tick(SNAKE_SPEED)
        
        # Counting down time and cause the game to quit if an apple hasnt been eaten within the time frame
        time -= 1   

        if (time<=0):
            run = False
            print('Time Out!')
            break
        
        # Automated Control
        # inputs to neural network:
        # distance forward, distance left, distance right, apple right, apple top
        inputs = determine_position(h, bodies, a)

        # Previous attempts
        # head x, head y, boundaries, apple x, apple y # Failed to train after 100 generatations of 100 population -> has no sense of direction
        # distance front, distance down, distance left, distance right, left distance to apple, upwards distance to apple # Failed to train after 100 generatations of 100 population -> has no sense of direction

        # if the user is not playing the game manually, run the game with automated controls
        if not(manual):
            # run inputs into neural network
            output = net.activate((inputs)) 

            # determing direction indicated by NN
            i = output.index(max(output))
            if i == 0:
                h.moveForward()
            elif i == 1:
                h.moveLeft()
            elif i == 2:
                h.moveRight()


        
        for event in pygame.event.get():
            # checking if exit button is pushed on game
            if (event.type == pygame.QUIT):
                run = False 
                break


            # manual control - checking for key pushes
            if manual:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        h.KeyMoveUp()
                        break # breaking prevents multiple keys being processed at the same time
                    elif event.key == pygame.K_DOWN:
                        h.KeyMoveDown()
                        break
                    elif event.key == pygame.K_LEFT:
                        h.KeyMoveLeft()
                        break
                    elif event.key == pygame.K_RIGHT:
                        h.KeyMoveRight()
                        break

        # update the position of the head and bodies
        update_positions(h, bodies)

        # checking for collisions
        if (h.check_collisions(bodies)):
            run = False
            print('Collision!')
            break

        # check if head ate apple
        if (h.check_apple(a)):
            score += 1
            time = 200
            end = bodies[-1]
            bodies.append(Body(end.p_x, end.p_y, end, SNAKE_WIDTH))
            a.reset(h, bodies)
            # if (score >= 200):
            #     run = False
            #     break


        # outputing distances for debugging
        distance_list = []
        if (distances):
            distance_list = [inputs[0], inputs[1], inputs[2]]

        # drawing game state onto screen
        draw_screen(win, h, bodies, a, distance_list, score, time, generation)

# running this file as main will allow user to play a regular game of snake
if __name__ == "__main__":
    single_game(manual=True, distances=True)