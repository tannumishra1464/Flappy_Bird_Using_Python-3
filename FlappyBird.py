# Required Packages.
import random
import sys
import pygame
from pygame.locals import*

# Game Functions.
# Bird Rotation.
def Rotate_Bird(bird):
	new_bird=pygame.transform.rotozoom(bird,Bird_Movement*3,1)
	return new_bird
	
# Bird Animation.	
def Bird_Animation():
	new_bird=BIRD_FRAMES[BIRD_INDEX]
	new_bird_rect=new_bird.get_rect(center=(40,BIRD_RECT.centery))
	return new_bird,new_bird_rect
	
# Creating The Pipe.
def Create_Pipe():
	random_pipe_pos=random.choice(PIPE_HEIGHT)
	top_pipe=PIPE_SURFACE.get_rect(midbottom=(250,random_pipe_pos-80))
	bottom_pipe=PIPE_SURFACE.get_rect(midtop=(250,random_pipe_pos))
	return bottom_pipe,top_pipe

# Pipe Movement.
def Move_Pipe(pipes):
	for pipe in pipes:
	    pipe.centerx-=3
	return pipes

# Drawing The Pipes.
def Draw_Pipes(pipes):
	for pipe in pipes:
	    if pipe.bottom>=486:
	        SCREEN.blit(PIPE_SURFACE,pipe)
	    else:
	        Flip_Pipe=pygame.transform.flip(PIPE_SURFACE,False,True)
	        SCREEN.blit(Flip_Pipe,pipe)

# Checking Collision.
def Check_Collision(pipes):
    for pipe in pipes:
        if BIRD_RECT.colliderect(pipe):
            Die_Sound.play()
            return False 
    if BIRD_RECT.centery>=372 or BIRD_RECT.centerx<=-50:
        return False 
    return True

# Score.
def Score_Display(game_state):
    if game_state=="main_game":
        Score_Surface=Score_Font.render(str(int(Score)),True,(255,255,255))
        Score_Rect=Score_Surface.get_rect(center=(150,100))
        SCREEN.blit(Score_Surface,Score_Rect)
        
    if game_state=="game_over":
        Score_Surface=Score_Font.render(str(int(Score)),True,(255,255,255))
        Score_Rect=Score_Surface.get_rect(center=(150,100))
        SCREEN.blit(Score_Surface,Score_Rect)
          	        	       		
# Game Variables.
Score=0
High_Score=0
Game_Active=True
Bird_Movement=0
Gravity=0.25
FPS=60

# Screen Dimensions.
SCREENWIDTH=285
SCREENHEIGHT=485
pygame.init()
FPSCLOCK=pygame.time.Clock()
Score_Font=pygame.font.Font("04B_19__.TTF",50)

# Fullscreen scaled output
SCREEN=pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.SCALED|pygame.FULLSCREEN)

# Creating The Ground.
BACKGROUND=pygame.image.load("Background.png").convert_alpha()

# Creating The Ground.
BASE=pygame.image.load("Base.png").convert_alpha()
BASE_x_pos=0

# Creating The Pipe.
PIPE_SURFACE=pygame.image.load("pipe.png").convert_alpha()
#PIPE_RECT=PIPE.get_rect(center=(150,380))
PIPE_LIST=[]
PIPE_HEIGHT=[166,180,230,270,300,320]
SPAWN_PIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE,1200)

# Creating The Bird.
BIRD_1=pygame.image.load("Upflap.png"). convert_alpha()
BIRD_2=pygame.image.load("Midflap.png"). convert_alpha()
BIRD_3=pygame.image.load("Downflap.png"). convert_alpha()
BIRD_FRAMES=[BIRD_1,BIRD_2,BIRD_3]
BIRD_INDEX=0
BIRD_SURFACE=BIRD_FRAMES[BIRD_INDEX]
BIRD_RECT=BIRD_SURFACE.get_rect(center=(40,200))
BIRD_FLYING=pygame.USEREVENT+1
pygame.time.set_timer(BIRD_FLYING,200)

# Creating Game Over Message.
Game_Over_Message=pygame.image.load("Gameover.png")

# Game Sounds.
Die_Sound=pygame.mixer.Sound("Diesound.wav")
Flap_Sound=pygame.mixer.Sound("FlapSound.wav")
Score_Sound=pygame.mixer.Sound("Pointsound.wav")
Score_Sound_Count=100
SCOREEVENT=pygame.USEREVENT+2
pygame.time.set_timer(SCOREEVENT,100 )

# The Main Game Loop.
while True:
    for event in pygame.event.get():
       if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
           pygame.quit()
           sys.exit()
       if event.type == KEYDOWN and (event.key == pygame.K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN and Game_Active:
           Bird_Movement=0
           Bird_Movement-=4
           Flap_Sound.play()
       if event.type == KEYDOWN and (event.key == pygame.K_5 or event.key == K_UP) or event.type == MOUSEBUTTONDOWN and Game_Active==False:
           Game_Active=True
           PIPE_LIST.clear()
           BIRD_RECT.center=(40,200)
           Bird_Movement=0
           Score=0
                      
       if event.type==BIRD_FLYING:
           if BIRD_INDEX<2:
               BIRD_INDEX+=1
           else:
               BIRD_INDEX=0
           BIRD_SURFACE,BIRD_RECT=Bird_Animation()
       if event.type==SPAWN_PIPE:
           PIPE_LIST.extend(Create_Pipe())
    
    # Main Background Screen.    
    SCREEN.blit(BACKGROUND,(0,-20))
    
    if Game_Active:
        # Bird Movement.
        Bird_Movement+=Gravity
        Rotated_Bird=Rotate_Bird(BIRD_SURFACE)
        BIRD_RECT.centery+=Bird_Movement
        if BIRD_RECT.centery>=372:
            Bird_Movement=0      
        SCREEN.blit(Rotated_Bird,BIRD_RECT)
        Game_Active=Check_Collision(PIPE_LIST)
        
        #Pipe Movement 
        PIPE_LIST=Move_Pipe(PIPE_LIST)
        Draw_Pipes(PIPE_LIST)
        
        #Score
        Score+=0.01        
        Score_Display("main_game")
        Score_Sound_Count-=1
        if Score_Sound_Count<=0:
           Score_Sound.play()
           Score_Sound_Count=100
    else:
        SCREEN.blit(Game_Over_Message,(45,200))
        SCREEN.blit(Rotated_Bird,BIRD_RECT)
        BASE_x_pos=0
        Score_Display("game_over")
                   
    # Base Movement.
    SCREEN.blit(BASE,(BASE_x_pos,385))
    BASE_x_pos-=2
    if BASE_x_pos<=-50:
        BASE_x_pos=0
	
	# Updating The Screen.
    pygame.display.update()
    FPSCLOCK.tick(FPS)
