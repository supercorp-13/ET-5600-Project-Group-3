import pygame
from pygame.locals import *

pygame.init()

#Set Max frames
clock = pygame.time.Clock()
fps = 60

#Set the window size
screen_width = 500
screen_height = 500

#Set screen size & show title
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jump Journey')

#Set the font type
font_score = pygame.font.SysFont('Comic Sans', 30)

#game variables
tile_size = 25
game_over = 0
main_menu = True
score = 0
max_cats = 10
collected_cats = 0


#load color
white = (255, 255, 255)

#load images (from folder images)
background_img = pygame.image.load('images/background1.png')
restart_img = pygame.image.load('images/restart.png')
start_img = pygame.image.load('images/start.png')
exit_img = pygame.image.load('images/exit.png')

#text, font, pos, and font color
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#define button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):

        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        #get mouse clicks
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
    
                

        screen.blit(self.image, self.rect)

        return action

#define player class
class Player():
    def __init__(self, x, y):
        self.reset(x, y)
        self.collected_cats = 0

    def update(self, game_over):
      
        if self.collected_cats >= max_cats:
            game_over = 1

        dx = 0
        dy = 0
        walk_cooldown = 5


        if game_over == 0: 

           
            #key presses
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
                self.vel_y = -12
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 2.5
            if key[pygame.K_RIGHT]:
                dx += 2.5

            #gravity
            self.vel_y += 1
            if self.vel_y > 5:
                self.vel_y = 5
            dy += self.vel_y

            #gravity collision
            self.in_air = True
            for tile in world.tile_list:
                

                #regular tile collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile [1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False


            #enemy/ghost collision
            if pygame.sprite.spritecollide(self, ghost_group, False):
                game_over = -1

           #player coordinates update
            self.rect.x += dx
            self.rect.y += dy

        #death animation
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 75:
                self.rect.y -= 2

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0

        screen.blit(self.image, self.rect)
        return game_over
    
    #when game resets
    def reset(self, x, y,):
        img = pygame.image.load('images/skelly.png')
        self.image = pygame.transform.scale(img, (25, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dead_image = pygame.image.load('images/skellydead.png').convert_alpha()
        self.dead_image = pygame.transform.scale(self.dead_image, (self.width, self.height))
        self.vel_y = 0
        self.jumped = False
        self.in_air = True
        self.collected_cats = 0

#define the cat class
class Cats(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/cat.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.initial_x = x
        self.initial_y = y

#define world class
class World():
    def __init__(self, data):
        self.tile_list = []

        #tile images
        dirt_img = pygame.image.load('images/dirt.png')
        grass_img = pygame.image.load('images/grass.png')
        
        #tile types
        row_count = 0 
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    ghost = Enemy(col_count * tile_size, row_count * tile_size)
                    ghost_group.add(ghost)
                if tile == 7:
                    cats = Cats(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    cat_group.add(cats)
                col_count += 1
            row_count += 1

    #draw character in world
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1]) 

#define enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ghost.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1

#world map/tiles
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 2, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 0, 6, 6, 3, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]             

#player position
player = Player(50, screen_height - 80) 

#groups
ghost_group = pygame.sprite.Group() 
cat_group = pygame.sprite.Group()           

world = World(world_data)

#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 200, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 40, screen_height // 2, exit_img)

run = True
while run:


    clock.tick(fps)

    screen.blit(background_img, (0, 0))

    #if exit button pressed
    if main_menu == True:
       if exit_button.draw():
        run = False
        
       #if start button pressed
       if start_button.draw():
           main_menu =  False
    
    else:

        world.draw()


        if game_over == 0:
            ghost_group.update()
            
            
            #cat/coin collision
            if pygame.sprite.spritecollide(player, cat_group, True):
                score += 1 #score increase
                #cats collected increase
                player.collected_cats += 1
                #score text
            draw_text('X '+ str(score), font_score, white, tile_size - 10, 10)
        
        game_over = player.update(game_over)

        #if won
        if game_over == 1:
            draw_text('YOU WIN', font_score, white, (screen_width // 2) -70, screen_height // 2)
        
        #if game over
        if game_over == -1:
            if restart_button.draw():
             player.reset(50, screen_height - 80)
             game_over = 0
             score = 0
        
        #draw cats & ghost onto screen
        ghost_group.draw(screen)
        cat_group.draw(screen)
    
    #if window is quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()

pygame.quit()