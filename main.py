"""
   -------------------------- Tayab Soomro -----------------------
    --------------------- Overall Script Owner --------------------

   CREDITS:
     - Andriy Andriyevskyy ~ Graphics
     - Google ~ Sounds
     - Maruf & Enriquez ~ General Help

"""

import pygame
import math
import random
import main_menu as mm
import pygame, sys

# -- COLOR CONSTANTS

COLOR_WHITE = (225, 225, 225)

COLOR_RED = (225, 0, 0)
COLOR_GREEN = (0, 225, 0)
COLOR_BLUE = (0, 0, 225)
COLOR_BLACK = (0, 0, 0)
COLOR_ORANGE = (217, 172, 26)
COLOR_BEIGE = (133, 201, 230)


# -- MISC CONSTANTS
showing_creds = False


# -- SCREEN DIMENSIONS

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


# ---- Classes ---- #

class Ice(pygame.sprite.Sprite):
    """ The Ice class that creates the Ice blocks """

    # -- Attributes

    def __init__(self,x,y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Includes/Images/ice_block.png')

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

class Projectile(pygame.sprite.Sprite):
    """ The projectile that falls when the ball collides with the golden blocks"""

    def __init__(self,x,y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Includes/Images/Projectiles/health.png")

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 2.5


class Player(pygame.sprite.Sprite):
    """ The Player class that refers to a horizontal bar that the ball strikes on """

    # -- Attributes PLAYER_INFROMATION
    width = 80
    height = 15
    score = 0
    lives = 3
    speed = 20
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Includes/Images/platform_3.png')
        self.rect = self.image.get_rect()

    def move_right(self):
        self.rect.x += self.speed
        if(self.rect.right > SCREEN_WIDTH):
                self.rect.right = SCREEN_WIDTH
    def move_left(self):
        self.rect.x -= self.speed
        if(self.rect.left < 0):
            self.rect.left = 0


class Ball(pygame.sprite.Sprite):
    """ The Ball class that handles everything that occurs to the ball """

    # -- Attributes BALL_INFORMATION
    width = 20
    height = 20
    ball_vel = [7,-7]

    max_x = SCREEN_WIDTH - width

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Includes/Images/ball_20.png')
        self.rect = self.image.get_rect()


    # -- Update method for the ball
    def update(self):
        # -- If game isn't over.
        if((Game.STATE_GAME_OVER == False)):
            self.rect.left += self.ball_vel[0]
            self.rect.top += self.ball_vel[1]

            # Is the ball off the screen from left
            if(self.rect.left <= 0):
                self.rect.left = 0
                self.ball_vel[0] = -self.ball_vel[0]
            # Is the ball off the screen from right
            elif(self.rect.left >= self.max_x):
                self.rect.left = self.max_x
                self.ball_vel[0] = -self.ball_vel[0]
            # Is the ball off the screen from top
            if(self.rect.top <= 0):
                self.rect.top = 0
                self.ball_vel[1] = -self.ball_vel[1]

class Game():
    """ This handles everything happening inside of the game """

    # --  Attributes  -- STATUS
    STATE_GAME_OVER = False
    STATE_GAME_WON = False
    STATE_PLAYING = False
    STATE_BEGIN_PLAYING = False
    STATE_BALL_IN_PADDLE = False

    # -- Attributes -- MISC
    level = 1
    lives = 3
    hit_sound = None
    ice_break_sound = None
    score_font = None
    game_over_font = None

    # -- Attributes -- GROUPS
    gold_blocks = None
    ice_blocks = None
    balls = None
    all_sprites = None
    projectiles = None


    # -- Attributes -- CHARACTERS
    player = None
    ball =  None
    ice = None
    projectile = None
    ice_blocks_left = 0





    def __init__(self,level):

        self.level = level
        self.lives = 3

        # -- Reseting Variables
        self.STATE_GAME_OVER = False
        self.STATE_GAME_WON = False
        self.STATE_PLAYING = False
        self.STATE_BEGIN_PLAYING = False
        self.STATE_BALL_IN_PADDLE = True

        self.all_sprites = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.ice_blocks = pygame.sprite.Group()
        self.gold_blocks= pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()


        self.all_sprites.remove(self.player)
        self.all_sprites.remove(self.ball)
        self.balls.remove(self.ball)
        self.ice_blocks.remove(self.ice)
        self.gold_blocks.remove(self.ice)
        self.projectiles.remove(self.projectile)



        self.player = None
        self.ball = None
        self.ice = None

        self.ice_blocks_left = 0

        # -- Setting Mouse to be inactive while playing game
        pygame.mouse.set_visible(0)


        # -- Create our Player
        self.player = Player()
        self.player.rect.x = SCREEN_WIDTH / 2
        self.player.rect.y = SCREEN_HEIGHT - 20
        self.all_sprites.add(self.player)

        # -- Create our Ball
        self.ball = Ball()
        self.ball.rect.left = self.player.rect.left + self.player.width / 2
        self.ball.rect.top  = self.player.rect.top - self.ball.height
        self.all_sprites.add(self.ball)
        self.balls.add(self.ball)

        # -- Initiating Fonts
        self.score_font = pygame.font.Font('Includes/Fonts/IGLOO.ttf', 30)
        self.game_over_font = pygame.font.Font('Includes/Fonts/IGLOO.ttf', 35)

        # -- Initiating Sounds
        self.hit_sound = pygame.mixer.Sound('Includes/Sounds/hit.ogg')
        self.ice_break_sound = pygame.mixer.Sound('Includes/Sounds/ice_hit.wav')


        y_ofs = 100
        column_b = 20
        for row in range(self.level + 4):
            x_ofs = 20
            for column in range(column_b):
                goldBlock = random.randint(0,column_b)
                if(column == goldBlock):
                    self.ice = Ice(x_ofs,y_ofs)
                    self.ice.image = pygame.image.load("Includes/Images/gold_block.png")
                    self.all_sprites.add(self.ice)
                    self.gold_blocks.add(self.ice)
                else:
                    self.ice = Ice(x_ofs,y_ofs)
                    self.ice_blocks.add(self.ice)
                    self.all_sprites.add(self.ice)
                x_ofs += self.ice.rect.width + 8

            y_ofs += self.ice.rect.height + 5
        self.ice_blocks_left = (self.level + 4) * (column_b)




    def process_events(self,screen):
        """ Handles the event processing in the game """
        for event in pygame.event.get():
            if((event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key ==  pygame.K_ESCAPE)):
                pause_menu = mm.main_menu(screen, ['Resume','Credits', 'Quit Game'], 150, 40, 0.7, COLOR_BLUE)

                if(pause_menu == 1):
                    showing_creds = True                    
                    show_creds(screen)
                if(pause_menu == 2):
                    pygame.quit()

            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_RIGHT):
                    if((self.STATE_GAME_OVER == False) or (self.STATE_GAME_WON == False)):
                        self.player.move_right()
                if(event.key == pygame.K_LEFT):
                    if((self.STATE_GAME_OVER == False) or (self.STATE_GAME_WON == False)):
                        self.player.move_left()
                if(event.key == pygame.K_SPACE):
                    if((self.STATE_GAME_OVER) and (self.STATE_BALL_IN_PADDLE)):
                        self.__init__(1)
                if(event.key == pygame.K_SPACE):
                    if(self.STATE_BALL_IN_PADDLE):
                        self.STATE_BALL_IN_PADDLE = False
                        self.STATE_BEGIN_PLAYING = True
                        self.ball.ball_vel = self.ball.ball_vel
                if((event.key == pygame.K_KP_ENTER) or (event.key == pygame.K_RETURN)):
                    if(self.STATE_GAME_WON):
                        self.__init__(self.level + 1)


        return False
    def run_logic(self,screen):
        """ Entire game logic is controlled here """

        if((self.STATE_GAME_OVER == False) and (self.STATE_GAME_WON == False)):

            self.all_sprites.update()

            ice_blocks_hit_list = pygame.sprite.spritecollide(self.ball, self.ice_blocks, True)

            for block in ice_blocks_hit_list:
                self.ice_break_sound.play()
                self.ball.ball_vel[1] = -self.ball.ball_vel[1]
                self.ice_blocks_left -= 1
                if(self.ice_blocks_left <= 0):
                    self.STATE_GAME_WON = True

            gold_block_hit_list = pygame.sprite.spritecollide(self.ball, self.gold_blocks, True)

            for gblock in gold_block_hit_list:
                self.ball.ball_vel[1] = -self.ball.ball_vel[1]
                self.projectile = Projectile(gblock.rect.x,gblock.rect.y)
                self.projectiles.add(self.projectile)
            self.projectiles.update()

            proj_hit_list = pygame.sprite.spritecollide(self.player, self.projectiles, True)

            for proj in proj_hit_list:
                if(self.lives < 3):
                    self.lives += 1

            if(pygame.sprite.spritecollide(self.player,self.balls, False)):
                #self.hit_sound.play()
                self.ball.top = self.player.rect.y - self.ball.height
                self.ball.ball_vel[1] = -self.ball.ball_vel[1]
            elif(self.ball.rect.bottom > SCREEN_HEIGHT - self.player.height):
                self.lives -= 1

                self.STATE_BALL_IN_PADDLE = True
                if(self.lives <= 0):
                    self.STATE_GAME_OVER = True
        if(self.STATE_BALL_IN_PADDLE):
            self.ball.rect.left = self.player.rect.left + self.player.width / 2
            self.ball.rect.top  = self.player.rect.top - self.ball.height
        if(self.STATE_BEGIN_PLAYING):
            self.ball.ball_vel = self.ball.ball_vel
                   

    def display_frame(self,screen):
        if(showing_creds == False):
            self.player.image = pygame.image.load("Includes/Images/platform_" + str(self.lives) + ".png")

            self.all_sprites.draw(screen)
            self.projectiles.draw(screen)
                   
            
            if(self.STATE_GAME_OVER):
                go_text_1 = self.game_over_font.render("Game Over!", True, COLOR_RED)
                screen.blit(go_text_1, [(SCREEN_WIDTH / 2) - 50, SCREEN_HEIGHT / 2])
    
    
                go_text_2 = self.game_over_font.render("Press SPACE to restart", True, COLOR_RED)
                screen.blit(go_text_2, [(SCREEN_WIDTH / 2) - 110, (SCREEN_HEIGHT / 2) + 80])
            elif(self.STATE_GAME_WON):
                gw_text_1 = self.game_over_font.render("You won!", True, COLOR_GREEN)
                screen.blit(gw_text_1, [(SCREEN_WIDTH / 2) - 50, (SCREEN_HEIGHT / 2)])
    
                gw_text_2 = self.game_over_font.render("Press Enter to Continue", True, COLOR_GREEN)
                screen.blit(gw_text_2, [(SCREEN_WIDTH / 2) - 110, (SCREEN_HEIGHT / 2) + 80])
    
            if not (self.STATE_GAME_OVER or self.STATE_GAME_WON):
                go_text_2 = self.game_over_font.render("", True, COLOR_WHITE)
                screen.blit(go_text_2, [(SCREEN_WIDTH / 2) - 200, (SCREEN_HEIGHT / 2) + 80])
    
                score_text = self.score_font.render("Blocks Left: " + str(self.ice_blocks_left), True, COLOR_WHITE)
                screen.blit(score_text,[450,45])
    
                level_text = self.score_font.render("Level: " + str(self.level), True, COLOR_WHITE)
                screen.blit(level_text, [40, 45])
    
                lives_text = self.score_font.render("Lives: " + str(self.lives), True, COLOR_WHITE)
                screen.blit(lives_text, [(SCREEN_WIDTH / 2) - 100, 45])
            pygame.display.flip()
        else:
            
            

def show_creds(screen):
    cred_font_reg = pygame.font.Font('Includes/Fonts/cred_reg.ttf',30)
    cred_font_bold = pygame.font.Font('Includes/Fonts/cred_bold.ttf',30)
    screen.fill(COLOR_WHITE)
    cred_text_1_1 = cred_font_bold.render("Owner", True, COLOR_BLACK)
    screen.blit( cred_text_1_1, [(SCREEN_WIDTH / 2) - 325, SCREEN_HEIGHT / 2 - 200])
    
    cred_text_1_2 = cred_font_reg.render("Tayab Soomro", True, COLOR_BLACK)
    screen.blit( cred_text_1_2, [(SCREEN_WIDTH / 2) - 225, SCREEN_HEIGHT / 2 - 200]) 
    
    cred_text_2_1 = cred_font_bold.render("Helpers", True, COLOR_BLACK)
    screen.blit( cred_text_2_1, [(SCREEN_WIDTH / 2) - 325, SCREEN_HEIGHT / 2 - 150])
            
    cred_text_2_2 = cred_font_reg.render("Maruf Mugdho and", True, COLOR_BLACK)
    screen.blit( cred_text_2_2, [(SCREEN_WIDTH / 2) - 225, SCREEN_HEIGHT / 2 - 150]) 
                    
    cred_text_2_3 = cred_font_reg.render("Miguel", True, COLOR_BLACK)
    screen.blit( cred_text_2_3, [(SCREEN_WIDTH / 2 + 15), SCREEN_HEIGHT / 2 - 150])
    
    cred_text_3_1 = cred_font_bold.render("Graphics", True, COLOR_BLACK)
    screen.blit( cred_text_3_1, [(SCREEN_WIDTH / 2) - 325, SCREEN_HEIGHT / 2 - 100]) 
                            
    cred_text_3_2 = cred_font_reg.render("Andriy", True, COLOR_BLACK)
    screen.blit( cred_text_3_2, [(SCREEN_WIDTH / 2) - 215, SCREEN_HEIGHT / 2 - 100])
    pygame.display.flip()

def main():
    pygame.init()
    global clock
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    
    # -- CREDITS   

    main_menu = mm.main_menu(screen, ['Start Game', 'Credits', 'Quit Game'], 150, 40, 0.7, COLOR_BLUE)
    pygame.display.set_caption("My Ice Breaker")

    done = False

    clock = pygame.time.Clock()


    pygame.key.set_repeat(10,10)

    game = None

    if(main_menu == 0):
        game = Game(1)
    if(main_menu == 1):
        show_creds(screen)
        showing_creds = True
    elif(main_menu == 2):
        pygame.quit()

    background = pygame.image.load('Includes/Images/background.png')
    while not done:



        if(game != None): done = game.process_events(screen)

        if(game != None): game.run_logic(screen)

        screen.blit(background,[0,0])
        if(game != None): game.display_frame(screen)

        clock.tick(60)


        if game == None:
            for event in pygame.event.get():
                if((event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key ==  pygame.K_ESCAPE)):
                    showing_creds = False
                    main()

    pygame.quit()
if __name__ == "__main__":
    main()






