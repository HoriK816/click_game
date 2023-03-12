import pygame
import sys
import math
import random
from enum import Enum

# system
display   = None
clock     = None
counter   = 0 
last_time = 30

# game 
proc_list = Enum("proc_list",["OP","GAME","ED"])
proc      = proc_list["OP"].value

# mouse cursor
cursor_x = 0 
cursor_y = 0

# target = [x,y,age,radius] 
target = []

# score 
score = 0
miss  = 0


def initialize():
    global display, clock
    # pygame
    pygame.init()
    pygame.display.set_caption("templete")
    display = pygame.display.set_mode((1200,800)) 
   
    # mixer
    pygame.mixer.init(44100)

    # mouse 
    pygame.mouse.set_visible(True)

    # clock
    clock = pygame.time.Clock()


def create_target():
    global target

    target_x = random.randint(0,1000)
    target_y = random.randint(0,700)
    target_color = None
    age = 0
    r = 60

    target.append([target_x,target_y,age,r])


def update_target():
    global target
    global target_element

    delete_index = []

    for i in range(len(target)):
        target[i][2] += 1

        if(target[i][2] %3 == 0): 
            target[i][3] -= 1

        if(target[i][2] == 180):
            delete_index.append(i)
    
    for i in range(len(delete_index)):
        if len(delete_index) != 0:
            max_index = len(delete_index) - 1
        else:
            max_index = 0
            
        del target[delete_index[max_index - i]]

def hit_check(click_x, click_y):
    global target
    global score, miss 
    
    delete_index = None

    for i in range(len(target)):

        # calculate the distance between the target to the mouse cursor
        target_x = target[i][0]
        target_y = target[i][1] 
        target_radius = target[i][3]

        distance = ((target_x-click_x)**2 + (target_y-click_y)**2) ** (1/2)

        # if the radius of target is bigger than the distance,
        # the target was hit
        if target_radius >= distance:
            delete_index = i

    if delete_index is not None:
        # hit -> score up 
        del target[delete_index]
        score += 1

    else:
        # miss click
        miss += 1


def draw_reticle():
    global display
    global cursor_x, cursor_y

    cursor_x, cursor_y  = pygame.mouse.get_pos()

    reticle = pygame.Rect(cursor_x-3,cursor_y-3, 6, 6) 
    reticle_up    = pygame.Rect(cursor_x-3,cursor_y-29,6,20) 
    reticle_down  = pygame.Rect(cursor_x-3,cursor_y+9,6,20)
    reticle_left  = pygame.Rect(cursor_x-29,cursor_y-3,20,6)
    reticle_right = pygame.Rect(cursor_x+9,cursor_y-3,20,6)

    pygame.draw.rect(display,(255,0,0),reticle)    
    pygame.draw.rect(display,(255,255,255),reticle_up)
    pygame.draw.rect(display,(255,255,255),reticle_down)
    pygame.draw.rect(display,(255,255,255),reticle_left)
    pygame.draw.rect(display,(255,255,255),reticle_right)


def draw_target():
    global display
    global target

    for i in range(len(target)):

        x = target[i][0]
        y = target[i][1] 
        age = target[i][2]  
        r = target[i][3]


        if 0 <= age < 60:
            color = (0,255,0)
        elif 60 < age < 120:
            color = (255,255,0)
        else:
            color = (255,0,0)

        pygame.draw.circle(display,color,(x,y),r)

def game_reset():
    global target, score, miss
    global proc, counter, last_time 
    
    target    = []
    score     = 0
    miss      = 0
    counter   = 0
    last_time = 30
    proc      = proc_list["GAME"].value

    pygame.mouse.set_visible(False)

def main():
    global display 
    global target
    global score, miss
    global proc
    global counter, last_time
    
    initialize()

    normal_font = pygame.font.SysFont(None,24)
    large_font = pygame.font.SysFont(None,48)

    # main loop
    while True:

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                if proc == proc_list["OP"].value:
                    proc += 1 
                    pygame.mouse.set_visible(False)
                elif proc == proc_list["GAME"].value:
                    cx, cy = pygame.mouse.get_pos()
                    hit_check(cx,cy)
                elif proc  == proc_list["ED"].value:
                    game_reset()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        if proc == proc_list["OP"].value:


            game_title = large_font.render("Click Game"
                    ,True,(255,255,255))
            how_to_start  = normal_font.render("click the mouse button" \
                    "to start the game", True,(255,255,255))

            display.blit(game_title,(505,300))
            display.blit(how_to_start,(435,500))

        if proc == proc_list["GAME"].value:

            # decrease the last time
            if counter % 60 == 0:
                last_time -= 1
                
                # move to ED screen
                if last_time <= 0 :
                    proc += 1
                    counter += 1
                    pygame.mouse.set_visible(True)

            # create a new target
            if counter % 30 == 0:
                create_target()

            # score denotation
            game_time  = normal_font.render("last time : "+str(last_time)
                    ,True,(255,255,255))
            game_score = normal_font.render("score     : "+str(score),
                    True,(255,255,255))
           
            # draw
            draw_target()
            draw_reticle()
            display.blit(game_time,(800,700))
            display.blit(game_score,(800,750))
           
            # calc
            update_target()
            
            counter += 1

        if proc == proc_list["ED"].value:

            # score denotation
            score_show = large_font.render("score :  " + str(score)
                    ,True,(255,255,255))
            miss_count = large_font.render("miss  :  " + str(miss)
                    ,True,(255,255,255))
            how_to_restart  = normal_font.render("click the mouse button" \
                    "to restart the game", True,(255,255,255))
            # draw
            display.blit(score_show,(400,300))
            display.blit(miss_count,(400,400))
            display.blit(how_to_start,(435,500))

        pygame.display.update()
        display.fill((0,0,0))
        clock.tick(60)


main()



