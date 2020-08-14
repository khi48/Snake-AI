# import pygame
import random
import neat
import os
import statistics

import game
from head import Head
from body import Body
from apple import Apple


import visualize
import pickle

import config_game

WIN_WIDTH = config_game.WIN_WIDTH
SNAKE_WIDTH = config_game.SNAKE_WIDTH

generation = 0


def eval_genome(g, config):

    net = neat.nn.FeedForwardNetwork.create(g, config)

    cycles_per_net = 5
    fitnesses = [0]*cycles_per_net

    for cycle in range(cycles_per_net):
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
            time -= 1  
            fitnesses[cycle] += 0.01 

            if (time<=0):
                run = False
                break
            

            # Control Code
            inputs = game.determine_position(h, bodies, a)
            
            output = net.activate((inputs)) #distance_up, distance_down, distance_left, distance_right

            i = output.index(max(output))
            if i == 0:
                h.moveForward()
            elif i == 1:
                h.moveLeft()
            elif i == 2:
                h.moveRight()

            game.update_positions(h, bodies)

            if (h.check_collisions(bodies)):
                run = False
                break

            if (h.check_apple(a)):
                score += 1
                fitnesses[cycle] += 10 + time*0.1
                time = 200
                end = bodies[-1]
                bodies.append(Body(end.p_x, end.p_y, end, SNAKE_WIDTH))
                a.reset(h, bodies)

    return [statistics.median(fitnesses), net]

def eval_genomes(genomes, config):

    global generation
    generation += 1

    best_net = [None, 0] # net, fitness

    for _, g in genomes:
        g.fitness = 0
        g.fitness, net = eval_genome(g, config)
        
        if (g.fitness > best_net[1]):
            best_net[0] = net 
            best_net[1] = g.fitness

    # print(best_net[1])
    # if ((generation) == 0):
    game.single_game(False, True, best_net[0], generation)


# Automated Control
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    # p.add_reporter(neat.StatisticsReporter())
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes,100)

    # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    # print(winner)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    # node_names = {-1: 'd_front', -2: 'd_left', -3: 'd_right', -4: 'a_right', -5: 'a_up'}
    # visualize.draw_net(config, winner, True, node_names=node_names)

    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                    filename="winner-feedforward.gv")
    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                    filename="winner-feedforward-enabled.gv", show_disabled=False)
    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                    filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)





if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    print(config_path)
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
#     distance_front = WIN_WIDTH-h.y
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
#     distance_left = WIN_WIDTH-h.y
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
                
            

# Latest control method. Converting to binary system to avoid collisions
# if (h.dir == 0):
#         # print('going up')
#         distance_front = h.y/WIN_WIDTH
#         distance_left = h.x/WIN_WIDTH
#         distance_right = (WIN_WIDTH-h.x)/WIN_WIDTH

#         if (a.x > h.x):
#             right_to_apple = 1
#         if (a.y < h.y):
#             forward_to_apple = 1

#         for b in bodies:
#             if (b.x == h.x):
#                 if (b.y < h.y):
#                     d =  (h.y-b.y)/WIN_WIDTH
#                     if (d < distance_front):
#                         distance_front = d
#             if (b.y == h.y):
#                 if (b.x < h.x):
#                     d = (h.x-b.x)/WIN_WIDTH
#                     if (d < distance_left):
#                         distance_left = d
#                 else:
#                     d = (b.x-h.x)/WIN_WIDTH
#                     if (d < distance_right):
#                         distance_right = d
                    


#     elif (h.dir == 1):
#         # print('going down')
#         distance_front = (WIN_WIDTH-h.y)/WIN_WIDTH
#         distance_left = (WIN_WIDTH-h.x)/WIN_WIDTH
#         distance_right = (h.x)/WIN_WIDTH

#         if (a.x < h.x):
#             right_to_apple = 1
#         if (a.y > h.y):
#             forward_to_apple = 1

#         for b in bodies:
#             if (b.x == h.x):
#                 if (b.y > h.y):
#                     d = (b.y-h.y)/WIN_WIDTH
#                     if (d < distance_front):
#                         distance_front = d
#             if (b.y == h.y):
#                 if (b.x > h.x):
#                     d = (b.x-h.x)/WIN_WIDTH
#                     if (d < distance_left):
#                         distance_left = d
#                 else:
#                     d = (h.x-b.x)/WIN_WIDTH
#                     if (d < distance_right):
#                         distance_right = d
                    

#     elif (h.dir == 2):
#         # print('going left')
#         distance_front = (h.x)/WIN_WIDTH
#         distance_left = (WIN_WIDTH-h.y)/WIN_WIDTH
#         distance_right = (h.y)/WIN_WIDTH

#         if (a.y < h.y):
#             right_to_apple = 1
#         if (a.x < h.x):
#             forward_to_apple = 1


#         for b in bodies:
#             if (b.y == h.y):
#                 if (b.x < h.x):
#                     d = (h.x-b.x)/WIN_WIDTH
#                     if (d < distance_front):
#                         distance_front = d
#             if (b.x == h.x):
#                 if (b.y >= h.y):
#                     d = (b.y-h.y)/WIN_WIDTH
#                     if (d < distance_left):
#                         distance_left = d
#                 else:
#                     d = (h.y-b.y)/WIN_WIDTH
#                     if (d < distance_right):
#                         distance_right = d

#     elif (h.dir == 3):
#         # print('going right')
#         distance_front = (WIN_WIDTH-h.x)/WIN_WIDTH
#         distance_left = (h.y)/WIN_WIDTH
#         distance_right = (WIN_WIDTH-h.y)/WIN_WIDTH

#         if (a.y > h.y):
#             right_to_apple = 1
#         if (a.x > h.x):
#             forward_to_apple = 1

#         for b in bodies:
#             if (b.y == h.y):
#                 if (b.x > h.x):
#                     d = (b.x-h.x)/WIN_WIDTH 
#                     if (d < distance_front):    
#                         distance_front = d
#             if (b.x == h.x):
#                 if (b.y <= h.y):
#                     d = (h.y-b.y)/WIN_WIDTH
#                     if (d < distance_left): 
#                         distance_left = d
#                 else:
#                     d = (b.y-h.y)/WIN_WIDTH
#                     if (d < distance_right): 
#                         distance_right = d