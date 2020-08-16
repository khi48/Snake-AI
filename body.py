import pygame

# Body class for each link in the snake
class Body:
    def __init__(self, x, y, parent, snake_width):
        self.x = x
        self.y = y
        self.p_x = self.x
        self.p_y = self.y
        self.parent = parent
        self.snake_width = snake_width
        self.colour = (255, 255, 255)

    # updates position to follow the body ahead of it
    def update(self):
        self.p_x = self.x
        self.p_y = self.y
        self.x = self.parent.p_x
        self.y = self.parent.p_y

    # draw body onto screen
    def draw(self, win):
        rect = pygame.Rect(self.x-self.snake_width/2, self.y-self.snake_width/2, self.snake_width, self.snake_width)
        pygame.draw.rect(win, self.colour, rect)