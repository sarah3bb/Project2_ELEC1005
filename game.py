# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame, random
import numpy as np
# from main import Eating_interface

pygame.init()

class Settings:
    def __init__(self):
        #setting dimensions of the screen
        self.width = 28 
        self.height = 28
        self.rect_len = 15

class Snake:
    def __init__(self):
        #setting the image for the head of the snake in different positions in the game        
        self.image_up = pygame.image.load('images/head_up.bmp')
        self.image_down = pygame.image.load('images/head_down.bmp')
        self.image_left = pygame.image.load('images/head_left.bmp')
        self.image_right = pygame.image.load('images/head_right.bmp')

        # self.rect =  pygame.Surface.get_rect(self.image_right, self.x, self.y)

        #setting the iamge for the tail of the snake in different positions in the game
        self.tail_up = pygame.image.load('images/tail_up.bmp')
        self.tail_down = pygame.image.load('images/tail_down.bmp')
        self.tail_left = pygame.image.load('images/tail_left.bmp')
        self.tail_right = pygame.image.load('images/tail_right.bmp')
            
        #setting the image for the body of the snake
        self.image_body = pygame.image.load('images/body.bmp')

        #the snake starts with facing right in the game
        self.facing = "right"
        self.initialize()

    def initialize(self):
        #initializing the game for a new player, setting the position for the snake and the initial score of the user
        self.position = [6, 6]
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0
        self.rect =  pygame.Surface.get_rect(self.image_right, topleft =(self.get_x(), self.get_y()))

    def get_x(self): #returns x coordinate of the head of teh snake
        return self.segments[0][0]
        
    def get_y(self): #returns y coordinate of the head of teh snake
        return self.segments[0][1]

    def blit_body(self, x, y, screen): #making the body appear on the screen
        screen.blit(self.image_body, (x, y))
        
    def blit_head(self, x, y, screen): #changing the image for the head of the snake when it truns and displaying it on the screen

        if self.facing == "up":
            screen.blit(self.image_up, (x, y))

        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  

        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  

        else:
            screen.blit(self.image_right, (x, y))  
            
    def blit_tail(self, x, y, screen): #changing the image for the tail of the snake when it truns and displaying it on the screen
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)]
        
        if tail_direction == [0, -1]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail_down, (x, y))  
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail_left, (x, y))  
        else:
            screen.blit(self.tail_right, (x, y))  
    

    #
    def blit(self, rect_len, screen): #making the snake appear on the screen, makes calls to the blit_head and blit_tail functions
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)                
        for position in self.segments[1:-1]:
            # print(f'POSITIONs: {position}')
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)
        # print(f' segments in blit: {self.segments}')                
            
    
    def update(self): #keep moving the snake in the direction that it is facing
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        self.segments.insert(0, list(self.position))
        
class Strawberry(): #class for the food of the snake
    def __init__(self, settings):

        #varibles for the settings of the game and the image of the food
        self.settings = settings
        
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')        
        self.initialize()
        
    def random_pos(self, snake): #makes the strawberry appear at random positions in the game
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')                
        
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)
        
        if self.position in snake.segments:
            self.random_pos(snake)

    def blit(self, screen): #displaying the food on the screen
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    def initialize(self): #setting initial position 
        self.position = [15, 10]


class Planet():
    # vel = 5
    def __init__(self, settings, n, ypos):

        #setting varibales for the class
        self.settings = settings
        self.x = 20
        # self.y = 50
        self.y = ypos
        self.start = 6
        self.width = 40
        self.height = 35
        self.end = 400
        self.path = [self.start, self.end]
        self.vel = 10
        self.walk = 0
        # self.image = pygame.image.load('images/watermelonPlanet.png')
        self.image = pygame.image.load('images/planet' + str(n) + '.png')


        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect =  pygame.Surface.get_rect(self.image, topleft = (self.get_x(), self.get_y()))        
        self.initialize()

    def get_x(self): #returns x coordinate
        return self.x
        
    def get_y(self): #returns y coordinate
        return self.y

    def get_height(self): #returns height
        return self.height

    def get_width(self): #returns width
        return self.width     

    # def draw(self):
    #     self.move()


    # def move(self):
    #     print("in move")
    #     print(f'x pos: {self.x}, y pos: {self.y}')
    #     print(f'velocity: {self.vel}')
    #     if self.vel > 0:
    #         print("in move positive")
    #         if self.x + self.vel < self.path[1]:
    #             self.x += self.vel
    #         else:
    #             print("NO ERROR")
    #             self.vel = -1 * self.vel
                
    #             self.walk = 0

    #     else:
    #         print("in move neg")
    #         diff = self.x + self.vel
    #         print(diff)
    #         if diff < self.path[0]:
    #             print("\n\n\nMOVING BACK\n\n\n")
    #             self.x += self.vel
    #         else:
    #             self.vel = -1 * self.vel
    #             self.walk = 0

    def move(self, screen): #makes the planets move
        self.x += self.vel
        # if self.x >= self.end or self.x < self.start:
        #     self.vel = -1 * self.vel

    def blit(self, screen): #display the image of the planet on the screen 
        # screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
        screen.blit(self.image, (self.x, self.y))
   
    def initialize(self): #initialize the coordinates
        self.position = [self.x, self.y]
        # self.draw()
      
        
class Game: #class for the game
    """
    """
    def __init__(self):

        #setting variables for the game class
        self.settings = Settings()
        self.snake = Snake()
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}    
        self.planet = Planet(self.settings, 1, 200)
        # self.Planet2 = Planet(self.settings, 2, 100)
        # self.Planet3 = Planet(self.settings, 3, 300)
        self.eating_sound = pygame.mixer.Sound('./sound/eating.mp3')

    def get_planet(self): #returns the planet on the screen in the game
        return self.planet

    def create_planet(self, image_index, ypos): #creates a new planet on the screen if one has already crossed the screen
        # print(f'\nIMAGE GIVEN: {image_index}, Y position: {ypos}\n\n\n')
        if self.planet.get_x() > 400:      
            self.planet = Planet(self.settings, image_index, ypos)
        
    def restart_game(self): #initialize all objects in the game
        self.snake.initialize()
        self.strawberry.initialize()
        self.planet.initialize()

    def current_state(self): #retruns the coordinates of the body of the snake        
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        k = 0
        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1

            # print(f'state for iter : {k}, for position: {position} giving state: {state}')
            k += 1
        
        state[:, :, 1] = -0.5        

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            # print(f'D in expand: {d}')
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state
    
    def direction_to_int(self, direction):
        #turning the directions: right, left, up and down to integers
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
    
    def do_move(self, move):
        move_dict = self.move_dict
        
        #setting the attribute for the new direction
        change_direction = move_dict[move]
        
        #if the new direction is right and the snake is not facing left, turn right because the snake cannot turn its head 180 degrees
        if change_direction == 'right' and not self.snake.facing == 'left':
        # if change_direction == 'right' and not self.snake.facing == 'right':
            self.snake.facing = change_direction

        #if the new direction is left and the snake is not facing right, turn left
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction

        #if the new direction is up and the snake is not facing down, turn upwards
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction

        #if the new direction is down and the snake is not facing up, turn downwards
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        #update the snake positions
        self.snake.update()
        
        food_sound = pygame.mixer.Sound('./sound/food.wav') #loading food eatten sounds
        
        #if the strawberry is in the same position as the snake, the snake gains the strawberry and the score is incremented 
        if self.snake.position == self.strawberry.position:
            self.strawberry.random_pos(self.snake)
            reward = 1
            pygame.mixer.Sound.play(food_sound)
            self.snake.score += 1
            pygame.mixer.Sound.play(self.eating_sound) #playing eating music
            # self.eating.eat()


        else:
            self.snake.segments.pop()
            reward = 0


        # if self.snake.position == self.Planet.position:

                
        #if the game ends, -1 is returned to indicate that it ended
        if self.game_end():
            return -1
                    
        return reward
    
    def game_end(self):
        end = False
        #game ends if the snake touches the boundaries of the screen
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        #game ends if the snake touches its body with its head
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        return end
        # if self.snake.position == self.Planet.position:
        #     end = True

        # if self.e1e2collide(self.snake, self.Planet):
        #     end = True

        # collide = self.snake.colliderect(self.Planet)
        # if len(pygame.Rect.collidelistall(self.Planet.rect, self.snake.rect)) == 1:
        #     end = True

        # if pygame.Rect.colliderect(self.Planet.rect, self.snake.rect) == True:
        #     end = True

        # return end

    def e1e2collide(self, e1, e2):
        return (e1.get_x() < (e2.get_x() + e2.get_width())) and ((e1.get_x() + e1.get_width()) > e2.get_x()) and (e1.get_y() < (e2.get_y() + e2.get_height())) and ((e1.get_x() + e1.get_height()) > e2.get_y())
    
    def blit_score(self, color, screen): #display score on the screen
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        screen.blit(text, (6, 6)) #changed the positioning of this so it is easier to see

