## warriors and wizards easy names repreasents objects of diffrent classes !

import pygame
from fighter1 import Fighter1 #copy
from fighter2 import Fighter2 #orignal
from pygame import mixer

#start pygame and mixer 
mixer.init()
pygame.init()

#create game window 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
pygame.display.set_caption("mo the resa")


#set framerate for controlling frames
clock= pygame.time.Clock()
FPS = 120

#define colors 
RED =(255 ,0 ,0)
YELLOW =(255 ,255 , 0)
WHITE =(255,255,255)

#define game variables 
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0] #player scores. [p1,p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000


#define fighter variables 
WARRIOR_SIZE = 180
WARRIOR_OFFSET =[72 , -2]
WARRIOR_DATA = [WARRIOR_SIZE , WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3 
WIZARD_OFFSET = [112 , 194]
WIZARD_DATA = [WIZARD_SIZE , WIZARD_SCALE , WIZARD_OFFSET]


#load music and sounds
pygame.mixer.music.load("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\audio\\music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1 , 0.0, 5000)

sword_fx = pygame.mixer.Sound("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\audio\\sword.wav")
sword_fx.set_volume(0.5)

magic_fx = pygame.mixer.Sound("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\audio\\magic.wav")
magic_fx.set_volume(0.75)


#lood background image 
bg_image = pygame.image.load("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\images\\background\\bg.jpg").convert_alpha()

# load sprite sheets
warrior_sheet = pygame.image.load("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\images\\warrior\\Sprites\\M-R\\ideal-IRJ-sii.png").convert_alpha()
wizard_sheet = pygame.image.load("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\images\\wizard\\Sprites\\wizard.png").convert_alpha()

# load victory image 
victory_img = pygame.image.load("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\images\\icons\\victory.png").convert_alpha()




#define number of steps in each animation
# note: each steps will be in list and all lists in a big one list
WARRIOR_ANIMATION_STEPS = [10 , 40 , 40]
WIZARD_ANIMATION_STEPS = [8 , 8, 1, 8, 8, 3, 7]


# define font 
count_font = pygame.font.Font("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\fonts\\Turok.ttf" , 80)
# score font 
score_font = pygame.font.Font("C:\\Users\\Num 1\\Documents\\GAME_PROJECT\\assets\\fonts\\Turok.ttf" , 30)

# function for drawing text 
def draw_text(text , font , text_col , x , y ):
   img = font.render(text , True , text_col)
   screen.blit(img, (x,y))


# function for drawing background
def draw_bg():
   screen.blit(bg_image ,(0,0))



# function for drawing fighters health bars  #لا تنسي كل ده ايتريشنز داخل اللوب #
def draw_health_bar(health, x , y ):
   ratio = health / 100
   pygame.draw.rect(screen , WHITE  ,(x - 2 ,y - 2 , 404 , 34))
   pygame.draw.rect(screen , RED  ,(x ,y , 400  ,30))
   pygame.draw.rect(screen , YELLOW  ,(x ,y , 400 * ratio ,30))
   


#create two instances of fighters
fighter_1 = Fighter1(1 ,200, 310 ,False , WARRIOR_DATA ,warrior_sheet , WARRIOR_ANIMATION_STEPS, sword_fx )
fighter_2 = Fighter2(2 ,700, 310,  True ,WIZARD_DATA , wizard_sheet , WIZARD_ANIMATION_STEPS , magic_fx )



###############################################################
#GAME LOOP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!----- 
run = True 
while(run):

    clock.tick(FPS)

    #draw background
    draw_bg()

    #show health bars
    draw_health_bar(fighter_1.health , 20 , 20)
    draw_health_bar(fighter_2.health , 580 , 20)
    draw_text("MO RESA: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("p2:" + str(score[1]), score_font, RED, 580, 60)


     #update countdown 
    if intro_count <= 0:
        #move fighters 
      fighter_1.move( SCREEN_WIDTH ,SCREEN_HEIGHT , screen , fighter_2 , round_over)
      fighter_2.move( SCREEN_WIDTH ,SCREEN_HEIGHT , screen , fighter_1 , round_over)
    else:
       #display count timer
       draw_text(str(intro_count), count_font, RED , SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 3)
       #update count timer
       #كل ثانيه فرق بين وقت باي جيم ووقت اللعبه دات نفسه .....
       if (pygame.time.get_ticks()- last_count_update) >= 1000 :
          intro_count -=1
          last_count_update = pygame.time.get_ticks() 
           
    #هو ده الصح
    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)


    #check for player defeat
    if round_over == False:
       if fighter_1.alive == False:
          score[1] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()

       elif fighter_2.alive == False:
          score[0] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
    else:
       #المره الجايه هتبقي بترو بقي
       #display victory image
       screen.blit(victory_img, (400, 200))
       #تخيل ارقام بسيطه 
       if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
          round_over = False
          intro_count = 3
          # you can made it with differ way add a reset method to fighter class
          fighter_1 = Fighter1(1 ,200, 310 ,False , WARRIOR_DATA ,warrior_sheet , WARRIOR_ANIMATION_STEPS, sword_fx )
          fighter_2 = Fighter2(2 ,700, 310,  True ,WIZARD_DATA , wizard_sheet , WIZARD_ANIMATION_STEPS , magic_fx )


    #event handler 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
         run = False


#update the display (of the screen)
    pygame.display.update()


#exit pygame after the while loop finished  
pygame.quit()