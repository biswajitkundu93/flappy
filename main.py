import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 680

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("flappy Birds by Biswajit Kundu")

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255, 255, 255)
black = (0, 0, 0)


#define game veriables
ground_scroll = 0
scroll_speed = 4    
flying = False
game_over = False
pipe_gap = 120
pipe_frequencies = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequencies
score = 0
pass_pipe = False





#load image
background = pygame.image.load('img/bg.png')
background = pygame.transform.scale(background, (screen_width, screen_height-100))
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

def draw_text(text, font, text_col, x, y):  
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def reset_game(): 
    global score
    pipe_group.empty()
    flappy.rect.y = int(screen_height / 2)-20
    score = 0


class Birds(pygame.sprite.Sprite):
    def __init__(self, x, y):  
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):  
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img) 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.vel = 0
        self.clicked = False

    def update(self): 
        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8 :
                self.vel = 8
            if self.rect.bottom < screen_height-150: 
                self.rect.y += int(self.vel)
        if game_over == False: 
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
                self.vel = -5
                self.rect.y += int(self.vel)
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0 : 
                self.clicked = False

            #handel the animation
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown: 
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):  
                    self.index = 0
            self.image = self.images[self.index]

            #rotated the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-3)
        else:   
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):  
    def __init__(self, x, y, position):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()

        if position == 1:  
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y-int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y+int(pipe_gap / 2)]

    def update(self):  
        self.rect.x -= scroll_speed
        if self.rect.right < 0:  
            self.kill()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Birds(100, int(screen_height / 2)-20)
bird_group.add(flappy)



class Button():  
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        #get posison
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos): 
            if pygame.mouse.get_pressed()[0] == 1: 
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))  
        return action

# btn_pipe = Pipe(300, int(screen_width / 2)-150, -1)
# top_pipe = Pipe(300, int(screen_width / 2)-150, 1)
# pipe_group.add(btn_pipe)
# pipe_group.add(top_pipe)

button = Button(screen_width//2-50, screen_height//2-100, button_img)

run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(background, (0,0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)

    #draw the ground
    screen.blit(ground_img, (ground_scroll, screen_height-150))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
        draw_text(str(score), font, black, int(screen_width/2), 20)


    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        

    #check if bird has hit the ground
    if flappy.rect.bottom >= screen_height-150:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        #genarete pipe 
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequencies:
            pipe_height = random.randint(-100, 100)  
            btn_pipe = Pipe(screen_width, int(screen_width / 2)-150+pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_width / 2)-150+pipe_height, 1)
            pipe_group.add(btn_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        

        #draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        
        pipe_group.update()

    #reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        

    pygame.display.update()

pygame.quit()