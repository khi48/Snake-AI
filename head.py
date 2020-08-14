import pygame

class Head:
    def __init__(self, win_width, snake_width, x, y):
        self.snake_width = snake_width
        self.win_width = win_width
        self.x = x
        self.y = y
        self.p_x = x
        self.p_y = y
        self.dir = 3 # 0 - up, 1 - down, 2 - left, 3 - right
        self.colour = (255, 0, 0)

    def KeyMoveUp(self):
        if not(self.dir == 1):
            self.dir = 0

    def KeyMoveDown(self):
        if not(self.dir == 0):
            self.dir = 1

    def KeyMoveLeft(self):
        if not(self.dir == 3):
            self.dir = 2

    def KeyMoveRight(self):
        if not(self.dir == 2):
            self.dir = 3

    def moveForward(self):
        pass

    def moveLeft(self):
        if (self.dir == 0):
            self.dir = 2
        elif (self.dir == 1):
            self.dir = 3
        elif (self.dir == 2):
            self.dir = 1
        elif (self.dir == 3):
            self.dir = 0

    def moveRight(self):
        if (self.dir == 0):
            self.dir = 3
        elif (self.dir == 1):
            self.dir = 2
        elif (self.dir == 2):
            self.dir = 0
        elif (self.dir == 3):
            self.dir = 1
    
    def check_collisions(self, bodies):
        if (self.x <= 0):
            return True 
        elif (self.x >= self.win_width):
            return True 
        elif (self.y <= 0):
            return True 
        elif (self.y >= self.win_width):
            return True 

        for b in bodies:
            if ((self.x == b.x) and (self.y == b.y)):
                return True

        return False

    def check_future_collisions(self, next_x, next_y, bodies):
        if (next_x <= 0):
            return True 
        elif (next_x >= self.win_width):
            return True 
        elif (next_y <= 0):
            return True 
        elif (next_y >= self.win_width):
            return True 

        for b in bodies:
            if ((next_x == b.x) and (next_y == b.y)):
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
            self.y -= self.snake_width # inverted because of coord system
        elif (self.dir == 1):
            self.y += self.snake_width
        elif (self.dir == 2):
            self.x -= self.snake_width
        elif (self.dir == 3):
            self.x += self.snake_width
        else:
            print('something wrong with the direction!')
        
    def draw(self, win):
        rect = pygame.Rect(self.x-self.snake_width/2, self.y-self.snake_width/2, self.snake_width, self.snake_width)
        pygame.draw.rect(win, self.colour, rect)