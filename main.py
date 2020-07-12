import os
import time

import pygame
import random


pygame.init()
pygame.mixer.init()



# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 128)
# Creating window
screen_width = 900
screen_height = 600
disp = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption("Zehrili Nagin")
clock=pygame.time.Clock()
fps=30
font=pygame.font.SysFont(name=None,size=30,italic=1)
pygame.display.update()

bgimg = pygame.image.load("sprites\snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

sbgimg = pygame.image.load("sprites\\back.jpg")
sbgimg = pygame.transform.scale(sbgimg, (screen_width, screen_height)).convert_alpha()

ubgimg = pygame.image.load("sprites\menu_cap.gif")
ubgimg = pygame.transform.scale(ubgimg, (screen_width, screen_height)).convert_alpha()

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    disp.blit(screen_text, [x,y])

def drawSnake(disp,red,snakelist,snake_size):
    fsnake=snakelist[-1]
    pygame.draw.circle(disp, red, [fsnake[0]+15, fsnake[1]+15],15)
    pygame.draw.rect(disp, black, [fsnake[0]+20, fsnake[1]+12, 4 , 4])
    for snake in snakelist[:-1]:
        pygame.draw.rect(disp, red, [snake[0], snake[1], snake_size, snake_size])



def welcome():
    exit_game = False
    while not exit_game:
        disp.fill(white)
        pygame.Surface.blit(disp,bgimg,[0,0,screen_width,screen_height])
        text_screen("Welcome to Snakes", white, 202, 250)
        text_screen("Press Space Bar To Play", white, 170, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('sprites\main.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)




def gameloop():
    exit_game=False
    game_over=False
    snake_size=30

    snake_x=50
    snake_y=100
    foodsize=10

    change=5
    snake_changex=0
    snake_changey=0
    snakelength=1
    snakelist=[]

    foodx=random.randint(13,screen_width-80)
    foody=random.randint(93,screen_height-80)
    score=90


    # Check if hiscore file exists
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = int(f.read())


    while not exit_game:

        if game_over:
            text_screen("Game Over! Press Enter To Continue", red, 250, 300)

            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key==pygame.K_SPACE:
                        pygame.mixer.music.load('sprites\main.mp3')
                        pygame.mixer.music.play()
                        gameloop()

        else:
            for event in pygame.event.get():


                if(event.type==pygame.QUIT):
                    exit_game=True
                if(event.type==pygame.KEYDOWN):
                    if event.key==pygame.K_RIGHT:
                        snake_changex=change
                        snake_changey=0
                    if event.key == pygame.K_LEFT:
                        snake_changex = -change
                        snake_changey = 0
                    if event.key == pygame.K_DOWN:
                        snake_changex = 0
                        snake_changey= change
                    if event.key == pygame.K_UP:
                        snake_changex = 0
                        snake_changey= -change
            snake_x=snake_x+snake_changex
            snake_y=snake_y+snake_changey


            pygame.Surface.blit(disp, ubgimg, [0, 0, screen_width, 80])
            pygame.Surface.blit(disp, sbgimg, [0, 80, screen_width, screen_height])

            hit=[snake_x,snake_y]
            snakelist.append(hit)

            if(len(snakelist)>snakelength):

                del snakelist[0]

            #FOOD
            if (abs( snake_x-foodx)<15 and abs(foody-snake_y)<15):
                foodx = random.randint(13, screen_width - 80)
                foody = random.randint(93, screen_height - 80)
                score+=5
                snakelength+=1
                if hiscore<score:
                    hiscore=score

            pygame.draw.circle(disp,blue,[foodx+10,foody+10],foodsize)
            text_screen("Score: " + str(score) + "  Hiscore: " + str(hiscore), red,650 , 20)
            #GameOver
            if snake_x>(screen_width-40) or snake_y>(screen_height-40) or snake_x<10 or snake_y<90 :
                pygame.mixer.music.load('sprites\die.wav')
                pygame.mixer.music.play()
                game_over=True
            if hit in snakelist[:-1]:
                pygame.mixer.music.load('sprites\die.wav')
                pygame.mixer.music.play()
                game_over=True
            #Snake and Border
            drawSnake(disp,red,snakelist,snake_size)
            pygame.draw.rect(disp, black, [0, 0, screen_width, 80], 10)
            pygame.draw.rect(disp, black, [0, 80, screen_width, screen_height - 80], 10)

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


if __name__ == '__main__':
    welcome()