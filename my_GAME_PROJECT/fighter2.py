import pygame 
#الاصللللل
#player here represents diffrent controls 
class Fighter2():
    def __init__(self, player , x,y , flip ,data , sprite_sheet , animation_steps , sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet , animation_steps)  #عمل call the load method in constructor when open it animation_list its variable not list .... ... ..#اللبوسه الملبوسه.....#####---#####
        self.action = 0   #0:idle #1:run #2:jump #3:attack1 #4:attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks() #counter measure time from wich fighter created --- slach between frames     
        self.rect = pygame.Rect((x,y,80,180))
        self.vel_y = 0  # زي ال SPEED بس لل y كمان بتتغير عشان في نط انما التانيه ثابته علي محور السينات 
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type= 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit= False
        self.health = 100
        self.alive = True



#####################################end of the constructor ######################################################

       ####فيها حتت ماث لازم تبقي عارفها مسبقا^^
       #method for all fighters
    def load_images(self,sprite_sheet ,animation_steps):
        #extract images from spritesheet
        #بيخش ياخد كل الصور بالعرض يخزنهم وينزل بالطول 
        animation_list = []
        # مفهومه حتت الواي
        for y, animation in enumerate(animation_steps) :
          temp_img_list =[]
          for x in range(animation):
            temp_img = sprite_sheet.subsurface( x * self.size , y * self.size ,self.size , self.size)
            temp_img_list.append( pygame.transform.scale(temp_img, (self.size * self.image_scale , self.size * self.image_scale)))
          animation_list.append(temp_img_list)
        return animation_list  

##################end of load images method ###########################################################




           # اهم ميثود عندكككaqaq
     ###### هنا المطبخ الللي هلي اساسه قايمه ميثود ال draw @@___@@
    def move(self ,screen_width ,screen_height , surface , target , round_over):
        #في محتجهم هنا بس مش علي كله ليه  خلتها فلس عشان كل مره هكول الفنكشن فاهم ملهاش علاقه  باللي في الكنستراكتور
        SPEED=3
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running= False
        self.attack_type = 0


        #get keypresses
        key = pygame.key.get_pressed()

        #can only perform other actions if not currently attacking and still alive
        if self.attacking == False and self.alive == True and round_over == False :
         
          #check player 1 controls 
         if self.player == 1 : 
           #movement
           if key[pygame.K_a]:
             dx -= SPEED
             self.running = True

           if key[pygame.K_d]:
             dx = SPEED
             self.running = True
            #jump
           if key[pygame.K_w] and self.jump == False:
             self.vel_y= -30    #عمل واحده مختلفه للجمبزززز
             self.jump = True
            #attack
           if key[pygame.K_r] or key[pygame.K_t]:
              self.attack(target) # دي فنكشن تحت يا بابلوا
              #determine attack type used 
              if  key[pygame.K_r]:
                self.attack_type = 1
              if  key[pygame.K_t]:
                self.attack_type = 2


        #check player 2 controls 
         if self.player == 2 : 
           #movement
           if key[pygame.K_LEFT]:
             dx -= SPEED
             self.running = True

           if key[pygame.K_RIGHT]:
             dx = SPEED
             self.running = True
            #jump
           if key[pygame.K_UP] and self.jump == False:
             self.vel_y= -30
             self.jump = True
            #attack
           if key[pygame.K_KP1] or key[pygame.K_KP2]:
              self.attack( target)
              #determine attack type used 
              if  key[pygame.K_KP_1]:
                self.attack_type = 1
              if  key[pygame.K_KP2]:
                self.attack_type = 2

############################################################
        #apply gravity بديهي بعد القفز وليس قبل    
        # احا مش ماث عمرو عناره ده سيستم اللعبه
        self.vel_y += GRAVITY   # عشان تفهمها محتاج ترجع للمين للوب الوايل ترو ده بير فريممم
        dy += self.vel_y 
       

        #ensure player stays on screen
        if self.rect.left + dx < 0:
           #اللي انت زودته ارجعه تاني 
            dx = - self.rect.left #- - = +#
        if self.rect.right + dx > screen_width:
           #اللي انت زودته ارجعه تاني  fuck to identation
            dx =  screen_width - self.rect.right   # الكبير ناقص الزياده .,.,.,.,.,
        if self.rect.bottom + dy > screen_height - 110 :
                self.vel_y =0 
                #اشتغلت هنا عشان ربطها بالارض 
                self.jump = False
                dy = screen_height - 110 - self.rect.bottom

        #ensure players face each other 
        #لو هو قدامي # يبن اللعيبه
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True    
         
        #apply attack cooldown 
        if self.attack_cooldown > 0:     # its releated to attack method we called upper return to it when finished ...
           self.attack_cooldown-= 1 


        #update player postion #انا بحرك الركتنجلز والصور وكله بيتحرك معاهم ززززز
        self.rect.x += dx    
        self.rect.y += dy  


        ##########move method end here##########################################

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################

    # handle animation updates  function
    def update(self):
       #check what action the player is performing--
       if self.health <= 0:
          self.health=0
          self.alive = False
          self.update_action(6)#6:death

       elif self.hit == True:
          self.update_action(5)#5:hit

       elif self.attacking == True:
          if self.attack_type ==1:
             self.update_action(3)#3:attack1
          elif self.attack_type ==2:
             self.update_action(4)#4:attack2  

       elif self.jump == True:
          self.update_action(2)#2:jump

       elif self.running == True:
          self.update_action(1)#1:run

       else :
          self.update_action(0)#0:idle

       animation_cooldown = 50
       #update image
       self.image = self.animation_list[self.action][self.frame_index] # frame index like x and action like y corr
       #check if enough time has passed since the last update 
       if pygame.time.get_ticks() - self.update_time > animation_cooldown:
          self.frame_index +=1
          self.update_time = pygame.time.get_ticks()

       #check if the animation have finished 
       if self.frame_index >= len(self.animation_list[self.action]):
          #if the player is dead then end the animation
          if self.alive == False:
             self.frame_index = len(self.animation_list[self.action])-1 # اخر عنصر يعني هخهخهخهخ
          else:
            self.frame_index =0 
          #check if an attack was excuted 
            if self.action == 3 or self.action == 4 :
              self.attacking = False
              self.attack_cooldown = 20
          #check if damage was taken 
            if self.action ==5:
              self.hit = False
             #if the player was in the middle of an attack , then the attack is stopped 
              self.attacking = False
              self.attack_cooldown = 20   
    

############update method end###########################################





#attack method++

    def attack(self  , target):
        if self.attack_cooldown == 0 :
          #excute attack 
          self.attacking = True
          self.attack_sound.play()
          #يبن اللعيبه  goalllll fe elgoalll
          attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width  * self.flip) , self.rect.y , 2 * self.rect.width , self.rect.height)
          if attacking_rect.colliderect(target.rect):
              target.health -= 10
              target.hit = True
          

############attack method end###########################################


   #update_action method
    def update_action(self, new_action):
       #check if the new action is diffrent to the previous one :
       if new_action != self.action:
          self.action = new_action
          #update the animation settings 
          self.frame_index= 0
          self.update_time = pygame.time.get_ticks()

        ############update_action method end###########################################



  #draw method
    def draw(self, surface):
        #flip image false is for not upward and down ward .....
        img = pygame.transform.flip(self.image , self.flip , False)   
        surface.blit(img ,(self.rect.x - (self.offset[0] * self.image_scale) ,    self.rect.y - (self.offset[1] * self.image_scale)))

        ##########draw method end here########################################## بالمربع يبن الالعيبه 