import pygame
from pygame import font
import button
import math
import spritesheet
import random

pygame.init()
pygame.font.init()

#Starting Screen
S_SCREENHEIGHT = 500
S_SCREENWIDTH = 700
GAME_NAME = "The Slime Trail"
screen = pygame.display.set_mode((S_SCREENWIDTH, S_SCREENHEIGHT))
pygame.display.set_caption(GAME_NAME)

#Speed up events
SPEED_SCROLL = pygame.USEREVENT + 1
SPEED_OBSTACLES = pygame.USEREVENT + 2
pygame.time.set_timer(SPEED_OBSTACLES, 10000)
pygame.time.set_timer(SPEED_SCROLL, 10000)

#Beginning vars
game_State = 'cover_page'
clock = pygame.time.Clock()
FPS = 80
BLACK = (0,0,0)
scroll = 0
obstacles = [550, 980, 1500]
obstacle_speed = 5
active = True
score = 0
pause = False
SPEEDUP_COUNTDOWN = 0

#jumping vars
y_gravity = 1 #two conditions jump_height/gravity = no remainders, and y_gravity > jumpheight/100
jump_height = 20
y_velocity = jump_height
jumping = False
y_position = 325
x_position = 170
velocity = 10

#Fonts
boldedpixel_font = pygame.font.Font('boldedpixelfont.ttf', 50)
score_text = boldedpixel_font.render("SCORE: " + str(score), True, BLACK)

death_font = pygame.font.Font('boldedpixelfont.ttf', 40)
death_score_text = death_font.render("You survived " + str(score) + " obstacles!", True, (198, 80, 90))
SPEEDUP_text = death_font.render("SPEED UP!", True, (198, 80, 90))

escape_font = pygame.font.Font('boldedpixelfont.ttf', 15)
escape_text = escape_font.render("Press 'ESC' to pause", True, BLACK)

escape_rect = escape_text.get_rect()
pygame.draw.rect(escape_text, BLACK, escape_rect, 1)

score_rect = score_text.get_rect()
pygame.draw.rect(score_text, BLACK, score_rect, 1)

SPEEDUP_text = death_font.render("SPEED UP!", True, (138,1,62))
text_rect = SPEEDUP_text.get_rect()
text_rect.center = (100,30)


#Load Images & Rescale
start_button = pygame.image.load('startbutton.png').convert_alpha()
quit_button = pygame.image.load('quitbutton.png').convert_alpha()
menu_button = pygame.image.load('thenewmenubutton.png').convert_alpha()
exit_button = pygame.image.load('exitbutton.png').convert_alpha()
resume_button = pygame.image.load('resumebutton.png').convert_alpha()
restart_button = pygame.image.load('restartbutton.png').convert_alpha()

background = pygame.image.load('coverart.png').convert_alpha()

death_screen = pygame.image.load('deathscreen.png').convert_alpha()

background_ingame = pygame.image.load('backgroundimage.png').convert()
BG_adjustedimage = pygame.transform.scale(background_ingame, (700,500))

menu_background = pygame.image.load('gamepaused.png').convert_alpha()
covermenu_background = pygame.image.load('gamemenu.png').convert_alpha()

obstacle_picture = pygame.image.load('obstacle 50x50.png').convert_alpha()
OP_adjustedimage = pygame.transform.scale(obstacle_picture, (125,125))
obs_rect = OP_adjustedimage.get_rect()

sprite_sheet_image = pygame.image.load('slime_jump.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

sprite_sheet_image2 = pygame.image.load('slime_move.png').convert_alpha()
sprite_sheet_2 = spritesheet.SpriteSheet(sprite_sheet_image2)

#sprite frames jumping vars
animation_list = []
animation_steps = [7, 7]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
temp_list = []
temp_list1 = []

#animation frames
for running_frame in range(animation_steps[0]):
    temp_list.append(sprite_sheet_2.get_image(running_frame, 123, 75, 1.55, BLACK))
animation_list.append(temp_list)

for jumping_frame in range(animation_steps[1]):
    temp_list1.append(sprite_sheet.get_image(jumping_frame, 79, 75, 2.6, BLACK))
animation_list.append(temp_list1)

#Base slime rectangle
slime_rect = animation_list[0][1].get_rect(center=(x_position,y_position))

#instances
s_button = button.Button(350, 285, start_button, 4.5)
me_button = button.Button(100, 420, menu_button, 3)
qu_button = button.Button(575, 420, quit_button, 3)
re_button = button.Button(350, 285, resume_button, 3)
qu1_button = button.Button(75, 450, quit_button, 2)
ex1_button = button.Button(350, 400, exit_button, 3)
ex_button = button.Button(350, 250, exit_button, 3)
res_button = button.Button(350, 275, restart_button, 3)

#infinite screen movenment
bg_ingame_width = BG_adjustedimage.get_width()
tiles = math.ceil(S_SCREENWIDTH / bg_ingame_width) + 1


#Game Loop
run = True
while run == True:
    clock.tick(FPS)
    screen.blit((background), (0, 0))
    if game_State == "cover_page":
        score = 0  #hard reset
        x_position = 165 
        y_position = 312
        y_velocity = jump_height  
        obstacles = [550, 1100, 1450] 
        active = True  
        jumping = False
        pause = False
        obstacle_speed = 5
        scroll = 0
        SPEEDUP_COUNTDOWN = 0
        if s_button.draw(screen):
            game_State = "in_game"
        if me_button.draw(screen):
            game_State = "in_menu"
        if qu_button.draw(screen):
            run = False
    if game_State == "cover_page": pygame.display.update()

    elif game_State == "in_menu":
        screen.blit((covermenu_background), (0,0))
        if ex_button.draw(screen):
            game_State = "cover_page"
    if game_State == "in_menu": pygame.display.update()

    elif game_State == "death_page": #output score acheived in run
        screen.blit(death_screen, (0, 0))
        death_score_text = death_font.render("You survived " + str(score) + " obstacles!", True, (198, 80, 90))
        if res_button.draw(screen):
            game_State = "cover_page"
        if score == 1:
            death_score_text1 = death_font.render("You survived " + str(score) + " obstacle!", True, (198, 80, 90))
            screen.blit(death_score_text1, (135, 125))
        if score != 1:
            death_score_text = death_font.render("You survived " + str(score) + " obstacles!", True, (198, 80, 90))
            screen.blit(death_score_text, (125, 125))

    if game_State == "death_page": pygame.display.update()

    elif game_State == "paused":
        screen.blit((menu_background), (0, 0))
        if re_button.draw(screen):
            game_State = "in_game"
            pause = False
        if qu1_button.draw(screen):
            pause = False
            run = False
        if ex1_button.draw(screen):
            score = 0  #hard reset
            x_position = 165 
            y_position = 312  
            y_velocity = jump_height 
            obstacles = [550, 1100, 1450] 
            active = True  
            jumping = False
            game_State = "cover_page"
            obstacle_speed = 5
            scroll = 0
            SPEEDUP_COUNTDOWN = 0
    if game_State == "paused": pygame.display.update()

    elif game_State == "in_game":
        for i in range(0, tiles):
            screen.blit(BG_adjustedimage, (i*bg_ingame_width + scroll,0))
        scroll -= 5 #move background << 5fps/load another image >>
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(animation_list[action]):
                frame = 0
        if abs(scroll) > bg_ingame_width:
            scroll = 0

        #score text output
        score_text = boldedpixel_font.render("SCORE: " + str(score), True, BLACK)
        screen.blit(score_text, (250, 10))

        #esc to pause text output
        escape_text = escape_font.render("Press 'ESC' to pause", True, BLACK)
        screen.blit(escape_text, (250,50))

        #jumping, and movement frames
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            jumping = True

        if jumping == True:
            y_position -= y_velocity
            y_velocity -= y_gravity
            if y_velocity < -jump_height:
                jumping = False
                y_velocity = jump_height
            slime_rect = animation_list[0][1].get_rect(center=(x_position, y_position))
            screen.blit(animation_list[0][6], slime_rect)
            slime_rect.center = (x_position, y_position)
        else:
            screen.blit(animation_list[action][frame], (75,312)) #running

        #adjusting slime hitbox
        hitbox_rect = pygame.Rect(slime_rect.left+95, slime_rect.top+90, (slime_rect.width // 2)-85, (slime_rect.height // 2)-50)
        #pygame.draw.rect(screen, (255, 0, 0), hitbox_rect, 2)

        #drawing obstacles
        obstacle0 = screen.blit(OP_adjustedimage, (obstacles[0], 280))
        obstacle1 = screen.blit(OP_adjustedimage, (obstacles[1], 280))
        obstacle2 = screen.blit(OP_adjustedimage, (obstacles[2], 280))

        #adjustment of obstacle hitbox + collision detection
        for i in range(len(obstacles)):
            obstacle_rect = pygame.Rect(obstacles[i]+25, 295, OP_adjustedimage.get_width()-50, OP_adjustedimage.get_height()-20)
            screen.blit(OP_adjustedimage, (obstacles[i], 280))
            #pygame.draw.rect(screen, (255, 0, 0), obstacle_rect, 2)
            if hitbox_rect.colliderect(obstacle_rect):
                #fading from the in-game to death screen
                fade_surface = pygame.Surface(screen.get_size())
                fade_surface.fill((0, 0, 0))
                for alpha in range(0, 255, 5):
                    fade_surface.set_alpha(alpha)
                    screen.blit(fade_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(10)  #delay to control the speed of the fade effect
                fade_surface.set_alpha(255)

                active = False
                game_State = "death_page"

        #infinite and randomly generated obstacles
        min_distance = 200
        for i in range(len(obstacles)):
            if active:
                obstacles[i] -= obstacle_speed
                if obstacles[i] < -85:
                    score += 1
                    obstacles[i] = random.randint(900, 1500)
                    #minimum distance between obstacles
                    if obstacles[i] - obstacles[i - 1] < min_distance:
                        obstacles[i] = obstacles[i - 1] + min_distance

            if SPEEDUP_COUNTDOWN > 0:
                screen.blit(SPEEDUP_text, text_rect) #draw the text
                SPEEDUP_COUNTDOWN -= 1 / FPS #update the counter

    for event in pygame.event.get():
        #pause functionality
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = True
                if pause == True:
                    game_State = 'paused'
        #speed up event
        if event.type == SPEED_OBSTACLES: 
            obstacle_speed += 0.25
        if event.type == SPEED_SCROLL:
            scroll -= 1.75
            SPEEDUP_COUNTDOWN = 3
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()

