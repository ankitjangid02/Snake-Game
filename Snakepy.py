#Libraries
import pygame
import random


#initialization
pygame.init()
pygame.mixer.init()


#Game Initializers
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
green=(126, 217, 87)

screen_width=900
screen_height=600

with open("./highscore", "w") as f: 
    f.write("0")

clock=pygame.time.Clock()
font=pygame.font.SysFont(None, 55)

gameWindow=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake Game")
pygame.display.update()
bgimg = pygame.image.load("./game-bg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

bgimgs = pygame.image.load("./Snake-head.jpg")
bgimgs = pygame.transform.scale(bgimgs, (30, 30)).convert_alpha()


#Functions
def plot(gameWindow,colour,snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,green,[x,y, snake_size, snake_size])

def text_screen(text, colour, x, y):
    screen_text=font.render(text, True, colour)
    gameWindow.blit(screen_text, [x,y])

def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.fill((233,220,229))
        bgimg4 = pygame.image.load("./Welcome-bg.jpg")
        bgimg4 = pygame.transform.scale(bgimg4, (screen_width, screen_height)).convert_alpha()
        gameWindow.blit(bgimg4,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    gameloop()
        pygame.display.update()
        clock.tick(90)

def gameloop():
    
    exit_game=False
    game_over=False
    snake_x=100
    snake_y=150
    snake_size=30
    fps=90
    velocity_x=0
    velocity_y=0
    food_x = random.randint(20, int(screen_width / 2))
    food_y = random.randint(20, int(screen_height / 2))

    score=0
    init_velocity=3
    snk_list=[]
    snk_length=1
    
    pygame.mixer.music.load('./snake-hissing-sound.mp3')
    pygame.mixer.music.play()

    
    with open("./highscore", "r") as f: 
        highscore=f.read()

    while not exit_game:
        
        if game_over==True:
            with open("./highscore", "w") as f: 
                f.write(str(highscore))
            gameWindow.fill(white)
            bgimg3 = pygame.image.load("./Game-Over-bg.jpg")
            bgimg3 = pygame.transform.scale(bgimg3, (screen_width, screen_height)).convert_alpha()
            gameWindow.blit(bgimg3,(0,0))
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                    game_over=False
                if event.type==pygame.KEYDOWN:
                    if(event.key==pygame.K_RETURN):
                        gameloop()
        
        else:
            for event in pygame.event.get():
                if(event.type==pygame.QUIT):
                    exit_game=True
                if(event.type==pygame.KEYDOWN):
                    if(event.key==pygame.K_RIGHT):
                        velocity_x=init_velocity
                        velocity_y=0
                    elif(event.key==pygame.K_DOWN):
                        velocity_y=init_velocity
                        velocity_x=0
                    elif(event.key==pygame.K_LEFT):
                        velocity_x=-init_velocity
                        velocity_y=0
                    elif(event.key==pygame.K_UP):
                        velocity_y=-init_velocity
                        velocity_x=0
                    elif(event.key==pygame.K_q):
                        score+=10

            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y
            if abs(snake_x - food_x)<30 and abs(snake_y - food_y)<30:
                score=score+10
                snk_length=snk_length+5
                food_x=random.randint(20,int(screen_width/2))
                food_y=random.randint(20,int(screen_height/2))
                if score>int(highscore):
                    highscore=score
                pygame.mixer.music.load('./beep-sound.mp3')
                pygame.mixer.music.play()
            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            text_screen("Score:"+str(score)+"   High Score:"+str(highscore),white,5,5)

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if (len(snk_list)>snk_length):
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.load('./explosion-sound.mp3')
                pygame.mixer.music.play()
                game_over=True
                
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load('./explosion-sound.mp3')
                pygame.mixer.music.play()
                game_over=True
                print("Game Over")


            pygame.draw.rect(gameWindow,red, [food_x, food_y, snake_size, snake_size])
            plot(gameWindow,green,snk_list, snake_size)
            if snk_list:
                gameWindow.blit(bgimgs,(snk_list[-1][0],snk_list[-1][1]))
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()
