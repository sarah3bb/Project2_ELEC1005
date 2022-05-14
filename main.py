# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

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


bg_front = pygame.image.load("images/bg_front.png")
bg_front = pygame.transform.scale(bg_front,(game.settings.width * 15, game.settings.height * 15)) #resizing the background image to the size of the screen 

bg_game = pygame.image.load("images/bg_game.png") #importing background image for inside the game
bg_game = pygame.transform.scale(bg_game,(game.settings.width * 15, game.settings.height * 15))  #making the background fit the dimensions of the game



rect_len = game.settings.rect_len #fetching length attribute from game class
snake = game.snake #assigning snake attribute from game class to variable snake
pygame.init()
fpsClock = pygame.time.Clock() #used for timing the game
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15)) #setting screen dimensions
pygame.display.set_caption('Gluttonous') #appears at the top of the window

crash_sound = pygame.mixer.Sound('./sound/crash.wav') #variable for sound


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black): #used to display messages in the game
    large_text = pygame.font.Font('fonts/mrsmonster.ttf', 70) #importing an external font that suits the game effects
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    #used to 
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        print(f'x in button (IF) {x}')
        print(f'y in button (IF) {y}')
        print(f'w in button (IF) {w}')
        print(f'h in button (IF) {h}')
        print(f'active color: {active_color}')
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        print(f'inactive color: {inactive_color}')
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont(None, 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame(): #used to close the window when quit is pressed
    pygame.quit()
    quit()


def crash(): #plays the crashing when the snake hits the boundry 
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(1)


def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(bg_front, [0,0]) #this is used to display the background image on the front screen
        message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15) #displays the name of the game

        button('Go!', 80, 240, 80, 40, green, bright_green, game_loop, 'human') #creating button go to play game
        button('Quit', 270, 240, 80, 40, red, bright_red, quitgame) #creating button quit to end game

        pygame.display.update() #udpates the changes as long as the game is running
        pygame.time.Clock().tick(15) #makes the game run at 15 frames per second (Sets the pace of the game)


def game_loop(player, fps=10):
    game.restart_game()

    while not game.game_end(): #while the snake hasn't hit the boundary

        pygame.event.pump()

        move = human_move() #user command
        fps = 5

        game.do_move(move) #make the snake move

        screen.blit(bg_game, [0,0]) #this is used to display the background image on the game screen

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(black, screen)

        pygame.display.flip()

        fpsClock.tick(fps) #runs at 5 frames per second

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
