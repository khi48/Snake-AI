import random
import pygame

# Apple class for snake to eat
class Apple:
    def __init__(self, win_width, snake_width, h, bodies):
        self.x = 0
        self.y = 0
        self.snake_width = snake_width
        self.win_width = win_width
        self.colour = (0, 255, 0)
        self.reset(h, bodies)

    # Resets apple to a new random position when snake eats it
    def reset(self, h, bodies):
        found = False 

        # has to check that the apples new position is not on the snake head or body
        while(not(found)):
            self.x = random.randrange(self.snake_width+self.snake_width/2, self.win_width-(self.snake_width+self.snake_width/2), self.snake_width) 
            self.y = random.randrange(self.snake_width, self.win_width-self.snake_width, self.snake_width) 
            found = True

            if ((self.x == h.x) and (self.y == h.y)):
                found = False
            for b in bodies:
                if ((self.x == b.x) and (self.y == b.y)):
                    found = False


    # drawing the snake apple onto the screen
    def draw(self, win):
        rect = pygame.Rect(self.x-self.snake_width/2, self.y-self.snake_width/2, self.snake_width, self.snake_width)
        pygame.draw.rect(win, self.colour, rect)
