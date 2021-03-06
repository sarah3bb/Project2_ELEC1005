# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT
import random

from game import Game

#RGB Codes for the colors 
black = pygame.Color(0, 0, 0) 
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)

#making an instance of the Game class
game = Game()


# bg_front = pygame.image.load("images/bg_front.png")
bg_front = pygame.image.load("images/galaxy2.jpg")
bg_front = pygame.transform.scale(bg_front,(game.settings.width * 15, game.settings.height * 15)) #resizing the background image to the size of the screen 

# bg_game = pygame.image.load("images/bg_game.png")
bg_game = pygame.image.load("images/galaxy2.png") #importing background image for inside the game
# bg_game = pygame.image.load("images/snake_red.png")
bg_game = pygame.transform.scale(bg_game,(game.settings.width * 15, game.settings.height * 15))  #making the background fit the dimensions of the game


rect_len = game.settings.rect_len #fetching length attribute from game class
snake = game.snake #assigning snake attribute from game class to variable snake
pygame.init()
fpsClock = pygame.time.Clock() #used for timing the game
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15)) #setting screen dimensions
pygame.display.set_caption('Gluttonous') #appears at the top of the window

crash_sound = pygame.mixer.Sound('./sound/crash.wav') #loading crash sounds

# eating_sound = pygame.mixer.Sound('./sound/eating.mp3')  

def theme_music(): #adding background music 
    pygame.mixer.music.load('./sound/jungle_music.wav')
    pygame.mixer.music.play(-1)

def text_objects(text, font, color=black): #creating a function to customize and render text on screen
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_display(text, x, y, color=black): #used to display messages in the game
    large_text = pygame.font.Font('fonts/mrsmonster.ttf', 70) #importing an external font that suits the game effects
    text_surf, text_rect = text_objects(text, large_text, color) #gets text and the area as a rectangle
    text_rect.center = (x, y) #coordinates of the text on the screen
    screen.blit(text_surf, text_rect) #display the text on the screen
    pygame.display.update() #update pygame


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None, mode=None): #used to craete buttons in the game
    
    mouse = pygame.mouse.get_pos() #gets the position of the mouse
    click = pygame.mouse.get_pressed() #returns if the mouse has been clicked
    if x + w > mouse[0] > x and y + h > mouse[1] > y: #if the mouse was positioned on the button
        # print(f'x in button (IF) {x}')
        # print(f'y in button (IF) {y}')
        # print(f'w in button (IF) {w}')
        # print(f'h in button (IF) {h}')
        # print(f'active color: {active_color}')
        pygame.draw.rect(screen, active_color, (x, y, w, h)) #drawing the button on screen
        if click[0] == 1 and action != None: 
            if parameter != None and mode != None:
                action(parameter, mode) #the action function is called if green buttons are clicked
            else:
                action()
    else:
        # print(f'inactive color: {inactive_color}')
        pygame.draw.rect(screen, inactive_color, (x, y, w, h)) #drawing the red quit button on the screen

    #setting the font and background of the text
    smallText = pygame.font.SysFont(None, 20)
    # print(f'small text: {smallText}')
    TextSurf, TextRect = text_objects(msg, smallText)
    # print(f'text surf: {TextSurf}, text rectangle: {TextRect}')
    TextRect.center = (x + (w / 2), y + (h / 2)) #coordinates of the text for the button
    screen.blit(TextSurf, TextRect) #display the text for the button


def quitgame(): #used to close the window when quit is pressed
    pygame.quit()
    quit()


def crash(): #plays the crashing when the snake hits the boundry and displays the message crashed along with the score which was added by us
    pygame.mixer.Sound.play(crash_sound)
    message_display('CRASHED', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    # message_display('Score: '+ str(game.snake.score), game.settings.width / 3 * 15, game.settings.height / 4 * 15, white)
    message_display('Score: '+ str(game.snake.score), 200, 250, white)

    time.sleep(1)

# class Eating_interface:

#     def __init__(self):
#         pass

#     def eat(self):
#         pygame.mixer.Sound.play(eating_sound) #playing eating music


def initial_interface(): #initial screen of the game before the user strats playing or quits the game
    intro = True
    while intro:

        for event in pygame.event.get(): #if the user quit, close the game
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(bg_front, [0,0]) #this is used to display the background image on the front screen
        message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15, white) #displays the name of the game

        # button('Go!', 80, 240, 80, 40, green, bright_green, game_loop, 'human') #creating button go to play game
        button('Easy', 40, 240, 80, 40, green, bright_green, game_loop, 'human', 1) #creating button for easy mode
        # button('Easy', 40, 240, 80, 40, green, game_loop, 'human', 1)
        # if easy:
        #     print(easy)
        button('Normal', 130, 240, 80, 40, green, bright_green, game_loop, 'human', 2) #creating button for normal mode
        button('Hard', 220, 240, 80, 40, green, bright_green, game_loop, 'human', 3) #creating button for hard mode
        button('Quit', 310, 240, 80, 40, red, bright_red, quitgame) #creating button quit to end game

        pygame.display.update() #udpates the changes as long as the game is running
        pygame.time.Clock().tick(15) #makes the game run at 15 frames per second (Sets the pace of the game)


# def game_loop(player, fps=10):
def game_loop(player, mode, fps=10): #where the game runs
    fps = 5
    if mode == 1: #if the mode is easy, make it slower for user
        print("easy")
        fps = 3
    elif mode == 2: #if the mode is normal, make it normal speed for user
        # print("hard or medium")
        fps = 7
    elif mode == 3: #if the mode is hard, make it very fast for user
        # print("hard or medium")
        fps = 15
    game.restart_game() #restarts the game with the objects initialized
    theme_music() #playing background music

    while not game.game_end(): #while the snake hasn't hit the boundary
        
        pygame.event.pump() #progresses the game

        move = human_move() #user command
        # fps = 20

        game.do_move(move) #make the snake move

        game.get_planet().move(screen) #makes the planets move 

        screen.blit(bg_game, [0,0]) #this is used to display the background image on the game screen

        ind= random.randint(1,8)
        yp = random.randint(40, 400)
        game.create_planet(ind, yp) #creates a new planet in the game

        #display all the objects on the screen
        game.planet.blit(screen)
        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        
        game.blit_score(yellow, screen)

        pygame.display.flip() #updates the contents of the display

        fpsClock.tick(fps) #runs at 5 frames per second

        
        # game.get_enemy1().move(screen)
        # game.get_enemy2().move(screen)
        # game.get_enemy3().move(screen)
        # game.planet.blit(screen)
        # game.enemy1.blit(screen)
        # game.enemy2.blit(screen)
        # game.enemy3.blit(screen)
        
    crash() #snake hits the boundary and the player loses
  

def human_move():
    direction = snake.facing

    for event in pygame.event.get(): #quit game if player quits
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN: #getting input from the player, the snake can move up, down, rigth and left
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction) #the direction the snake has to go depending on user input
    return move #return the next move of the snake


if __name__ == "__main__": #runs the game
    initial_interface()
