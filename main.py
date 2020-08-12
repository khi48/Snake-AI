import pygame
import random
import neat
import os

import visualize
import pickle

# os.environ["PATH"] += os.pathsep + '/usr/local/lib/python3.7/site-packages/graphviz/__pycache__'

pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800

SNAKE_WIDTH = 20
SNAKE_SPEED = 15
FONT = pygame.font.SysFont("comicsans", 50)

generation = 0

class Head:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.p_x = x
        self.p_y = y
        self.dir = 3 # 0 - up, 1 - down, 2 - left, 3 - right
        self.colour = (255, 0, 0)

    def moveUp(self):
        if not(self.dir == 1):
            self.dir = 0

    def moveDown(self):
        if not(self.dir == 0):
            self.dir = 1

    def moveLeft(self):
        if not(self.dir == 3):
            self.dir = 2

    def moveRight(self):
        if not(self.dir == 2):
            self.dir = 3
    
    def check_collisions(self, bodies):
        if (self.x <= 0):
            return True 
        elif (self.x >= WIN_WIDTH):
            return True 
        elif (self.y <= 0):
            return True 
        elif (self.y >= WIN_HEIGHT):
            return True 

        for b in bodies:
            if ((self.x == b.x) and (self.y == b.y)):
                return True

        return False

    def check_apple(self, a):
        if ((self.x == a.x) and (self.y == a.y)):
            return True
        return False

    def update(self):
        self.p_x = self.x
        self.p_y = self.y
        if (self.dir == 0):
            self.y -= SNAKE_WIDTH # inverted because of coord system
        elif (self.dir == 1):
            self.y += SNAKE_WIDTH
        elif (self.dir == 2):
            self.x -= SNAKE_WIDTH
        elif (self.dir == 3):
            self.x += SNAKE_WIDTH
        else:
            print('something wrong with the direction!')
        
    def draw(self, win):
        rect = pygame.Rect(self.x-SNAKE_WIDTH/2, self.y-SNAKE_WIDTH/2, SNAKE_WIDTH, SNAKE_WIDTH)
        pygame.draw.rect(win, self.colour, rect)
        
class Body:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.p_x = self.x
        self.p_y = self.y
        self.parent = parent
        self.colour = (255, 255, 255)

    def update(self):
        self.p_x = self.x
        self.p_y = self.y
        self.x = self.parent.p_x
        self.y = self.parent.p_y
    
    def draw(self, win):
        rect = pygame.Rect(self.x-SNAKE_WIDTH/2, self.y-SNAKE_WIDTH/2, SNAKE_WIDTH, SNAKE_WIDTH)
        pygame.draw.rect(win, self.colour, rect)

class Apple:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.colour = (0, 255, 0)
        # self.reset()

    # cannot regenerate onto body of snake!!
    def reset(self, h, bodies):
        found = False 

        while(not(found)):
            self.x = random.randrange(SNAKE_WIDTH+SNAKE_WIDTH/2, WIN_WIDTH-(SNAKE_WIDTH+SNAKE_WIDTH/2), SNAKE_WIDTH) 
            self.y = random.randrange(SNAKE_WIDTH, WIN_HEIGHT-SNAKE_WIDTH, SNAKE_WIDTH) 
            found = True

            if ((self.x == h.x) and (self.y == h.y)):
                found = False
            for b in bodies:
                if ((self.x == b.x) and (self.y == b.y)):
                    found = False


    def draw(self, win):
        rect = pygame.Rect(self.x-SNAKE_WIDTH/2, self.y-SNAKE_WIDTH/2, SNAKE_WIDTH, SNAKE_WIDTH)
        pygame.draw.rect(win, self.colour, rect)





def update_positions(head, bodies):
    head.update()
    for b in bodies:
        b.update()

def eval_genome(g, config):

    net = neat.nn.FeedForwardNetwork.create(g, config)

    fitnesses = []
    runs = 1

    for r in range(runs):
        fitness = 0
        run = True
        score = 0
        time = 200
        
        x = random.randrange(SNAKE_WIDTH+SNAKE_WIDTH/2, WIN_WIDTH-(SNAKE_WIDTH+SNAKE_WIDTH/2), SNAKE_WIDTH) 
        y = random.randrange(SNAKE_WIDTH, WIN_WIDTH-(SNAKE_WIDTH), SNAKE_WIDTH) 
        h = Head(x, y)

        b1 = Body(200, 200, h)
        b2 = Body(200, 200, b1)
        bodies = [b1, b2]
        a = Apple()
        a.reset(h, bodies)

        
        while(run):
            time -= 1   
            fitness += 0.05

            if (time<0):
                run = False
                break

            # Automated Control
            # Inputs:
            # head x, head y, boundaries, apple x, apple y # Failed to train after 100 generatations of 100 population -> has no sense of direction
            # distance front, distance down, distance left, distance right, left distance to apple, upwards distance to apple
            # if not(manual):

            distance_up = h.y/WIN_HEIGHT
            distance_down = (WIN_HEIGHT-h.y)/WIN_HEIGHT
            distance_left = h.x/WIN_WIDTH
            distance_right = (WIN_WIDTH-h.x)/WIN_WIDTH

            left_to_apple = (h.x-a.x)/WIN_WIDTH # DIDNT THINK ABOUT THIS YET
            up_to_apple = (h.y-a.y)/WIN_HEIGHT

            for b in bodies:
                if (b.x == h.x):
                    if (b.y > h.y):
                        d = (b.y-h.y)/WIN_HEIGHT
                        if (d < distance_down):
                            distance_down = d
                    else:
                        d = (h.y-b.y)/WIN_HEIGHT
                        if (d < distance_up):
                            distance_up = d
                elif (b.y == h.y):
                    if (b.x > h.x):
                        d = (b.x-h.x)/WIN_WIDTH
                        if (d < distance_right):
                            distance_right = d
                    else:
                        d = (h.x-b.x)/WIN_WIDTH
                        if (d < distance_left):
                            distance_left = d
                # else: 
                #     print('na')

            # print([distance_up, distance_down, distance_left, distance_right, left_to_apple, up_to_apple])
            output = net.activate((distance_up, distance_down, distance_left, distance_right, left_to_apple, up_to_apple))
            
            i = output.index(max(output))
            if i == 0:
                h.moveUp()
            elif i == 1:
                h.moveDown()
            elif i == 2:
                h.moveLeft()
            elif i == 3:
                h.moveRight()
            else:
                print('something wrong with output')


            update_positions(h, bodies)

            if (h.check_collisions(bodies)):
                run = False
                break

            if (h.check_apple(a)):
                score += 1
                fitness += 10 + time*0.1
                time = 200
                end = bodies[-1]
                bodies.append(Body(end.p_x, end.p_y, end))
                a.reset(h, bodies)
                if (score >= 2000/5):
                    print("\nSCORED TO HIGH!\n")
                    run = False
                    break

        fitnesses.append(fitness)

    return sum(fitnesses)/len(fitnesses), net


def eval_genomes(genomes, config):

    global generation
    generation += 1

    best_net = [None, 0] # net, fitness


    for _, g in genomes:

        g.fitness, net = eval_genome(g, config)
        
        if (g.fitness > best_net[1]):
            best_net[0] = net 
            best_net[1] = g.fitness

    print(best_net[1])
    single_game(False, True, best_net[0])



def draw_screen(win, head, bodies, apple, distance_list, score, time, gen):
    win.fill((0, 0, 0))
    head.draw(win)

    for b in bodies:
        b.draw(win)

    apple.draw(win)

    text = FONT.render("U: {}".format(distance_list[0]), 1, (255, 255, 255))
    win.blit(text, (head.x, head.y))
    text = FONT.render("D: {}".format(distance_list[1]), 1, (255, 255, 255))
    win.blit(text, (head.x, head.y+text.get_height()+5))
    text = FONT.render("L: {}".format(distance_list[2]), 1, (255, 255, 255))
    win.blit(text, (head.x, head.y+(text.get_height()+5)*2))
    text = FONT.render("R: {}".format(distance_list[3]), 1, (255, 255, 255))
    win.blit(text, (head.x, head.y+(text.get_height()+5)*3))

    text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10))

    text = FONT.render("Time: " + str(time), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10 + 10 + text.get_height()))

    text = FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    pygame.display.update()

def single_game(manual, distances=False, net=None):
    # if draw:
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    win.fill((0, 0, 0))

    clock = pygame.time.Clock()


    run = True
    score = 0
    time = 200
    
    x = random.randrange(SNAKE_WIDTH+SNAKE_WIDTH/2, WIN_WIDTH-(SNAKE_WIDTH+SNAKE_WIDTH/2), SNAKE_WIDTH) 
    y = random.randrange(SNAKE_WIDTH, WIN_WIDTH-(SNAKE_WIDTH), SNAKE_WIDTH) 
    h = Head(x, y)

    b1 = Body(200, 200, h)
    b2 = Body(200, 200, b1)
    bodies = [b1, b2]
    a = Apple()
    a.reset(h, bodies)

    global generation

    
    while(run):
        clock.tick(SNAKE_SPEED)
        
        time -= 1   

        if (time<0):
            run = False
            break

        # if draw:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False 
                break


            # Manual Control
            if manual:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        h.moveUp()
                    elif event.key == pygame.K_DOWN:
                        h.moveDown()
                    elif event.key == pygame.K_LEFT:
                        h.moveLeft()
                    elif event.key == pygame.K_RIGHT:
                        h.moveRight()

        # Automated Control
        # Inputs:
        # head x, head y, boundaries, apple x, apple y # Failed to train after 100 generatations of 100 population -> has no sense of direction
        # distance front, distance down, distance left, distance right, left distance to apple, upwards distance to apple
        if not(manual):

            distance_up = h.y/WIN_HEIGHT
            distance_down = (WIN_HEIGHT-h.y)/WIN_HEIGHT
            distance_left = h.x/WIN_WIDTH
            distance_right = (WIN_WIDTH-h.x)/WIN_WIDTH

            left_to_apple = (h.x-a.x)/WIN_WIDTH # DIDNT THINK ABOUT THIS YET
            up_to_apple = (h.y-a.y)/WIN_HEIGHT

            for b in bodies:
                if (b.x == h.x):
                    if (b.y > h.y):
                        d = (b.y-h.y)/WIN_HEIGHT
                        if (d < distance_down):
                            distance_down = d
                    else:
                        d = (h.y-b.y)/WIN_HEIGHT
                        if (d < distance_up):
                            distance_up = d
                elif (b.y == h.y):
                    if (b.x > h.x):
                        d = (b.x-h.x)/WIN_WIDTH
                        if (d < distance_right):
                            distance_right = d
                    else:
                        d = (h.x-b.x)/WIN_WIDTH
                        if (d < distance_left):
                            distance_left = d
                        
            output = net.activate((distance_up, distance_down, distance_left, distance_right, left_to_apple, up_to_apple))
            
            i = output.index(max(output))
            if i == 0:
                h.moveUp()
            elif i == 1:
                h.moveDown()
            elif i == 2:
                h.moveLeft()
            elif i == 3:
                h.moveRight()
            else:
                print('something wrong with output')


        update_positions(h, bodies)

        if (h.check_collisions(bodies)):
            run = False
            break

        if (h.check_apple(a)):
            score += 1
            time = 200
            end = bodies[-1]
            bodies.append(Body(end.p_x, end.p_y, end))
            a.reset(h, bodies)
            if (score >= 50):
                run = False
                break


        distance_list = []
        if (distances):
            distance_list = [distance_up, distance_down, distance_left, distance_right]


        draw_screen(win, h, bodies, a, distance_list, score, time, generation)




# Automated Control
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes,100)


    # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    node_names = {-1: 'd_up', -2: 'd_down', -3: 'd_left', -4: 'd_right', -5: 'd_apple_x', -6: 'd_apple_y', 0: 'control'}
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward.gv")
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled.gv", show_disabled=False)
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)


# if (h.dir == 0):
#     # print('going up')
#     distance_front = h.y
#     distance_left = h.x
#     distance_right = WIN_WIDTH-h.x

#     for b in bodies:
#         if ((b.x == h.x) and (b.y <= h.y)):
#             distance_front = h.y-b.y
#         if (b.y == h.y):
#             if (b.x <= h.x):
#                 distance_left = h.x-b.x
#             else:
#                 distance_right = b.x-h.x
                


# elif (h.dir == 1):
#     # print('going down')
#     distance_front = WIN_HEIGHT-h.y
#     distance_left = WIN_WIDTH-h.x
#     distance_right = h.x

#     for b in bodies:
#         if ((b.x == h.x) and (b.y >= h.y)):
#             distance_front = b.y-h.y
#         if (b.y == h.y):
#             if (b.x >= h.x):
#                 distance_left = b.x-h.x
#             else:
#                 distance_right = h.x-b.x
                

# elif (h.dir == 2):
#     # print('going left')
#     distance_front = h.x
#     distance_left = WIN_HEIGHT-h.y
#     distance_right = h.y

#     for b in bodies:
#         if ((b.y == h.y) and (b.x <= h.x)):
#             distance_front = h.x-b.x
#         if (b.x == h.x):
#             if (b.y >= h.y):
#                 distance_left = b.y-h.y
#             else:
#                 distance_right = h.y-b.y

# elif (h.dir == 3):
#     # print('going right')
#     distance_front = WIN_WIDTH-h.x
#     distance_left = h.y
#     distance_right = WIN_WIDTH-h.y

#     for b in bodies:
#         if ((b.y == h.y) and (b.x >= h.x)):
#             distance_front = b.x-h.x
#         if (b.x == h.x):
#             if (b.y <= h.y):
#                 distance_left = h.y-b.y
#             else:
#                 distance_right = b.y-h.y
                
            