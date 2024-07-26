import sys

import pygame

from Classes.Enemy import Enemy

"""
music credit

"Infinite Perspective" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

"Mesmerizing Galaxy " Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/
"""

# Initialize PyGame's internal variables
pygame.init()

pygame.key.set_repeat(60, 10)

pygame.display.set_caption('  Blue, Green, Saviour')

# Set up variables for the screen size in pixels
size = (1540, 865)

# Initialize a window with the screen size you set
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
fps = 60

player_image = pygame.image.load("images/avatar.png")
enemy_image = pygame.image.load("images/enemy.png")
princess_image = pygame.image.load("images/princess.png")
bg_image = pygame.image.load("images/bg.png")
icon = pygame.image.load("images/icon.png")

pygame.display.set_icon(icon)

pygame.mixer_music.load("music/Infinite Perspective.mp3")

music_playing = False

# Colors
txt_color = (0, 0, 0)

game_font_small = pygame.font.SysFont("fonts/Montserrat/Montserrat-Regular.ttf", 25)
game_font_reg = pygame.font.SysFont("fonts/Montserrat/Montserrat-Regular.ttf", 50)
game_font_big = pygame.font.SysFont("fonts/Montserrat/Montserrat-Regular.ttf", 100)


# player
player_x = 100
player_y = 580
player_w = 50
player_h = 80
player_s = 1
jumping = False

grav = 0.9
jump_h = 20
jump_v = jump_h

player = pygame.Rect(player_x, player_y, player_w, player_h)

enemy_x = 600
enemy_y = 580
enemy_w = 50
enemy_h = 80
enemy_s = -2

# enemy = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)

enemy = Enemy(enemy_x, enemy_y, enemy_w, enemy_h, enemy_s, "h",  50, 1450)

princess_x = 600
princess_y = 580
princess_w = 50
princess_h = 80

princess = pygame.Rect(princess_x, princess_y, princess_w, princess_h)

stage = 1
scene = 1


def draw_sprites():
    if scene == 1:
        screen.blit(bg_image, (0, 0))
        draw_text("Blue, Green, Saviour", game_font_big, txt_color, 450, 252.5)
        draw_text("BY IAN NORTHCUTT", game_font_big, txt_color, 450, 352.5)
        draw_text("PRESS SPACE TO START", game_font_big, txt_color, 400, 452.5)
        screen.blit(player_image, player)
    elif scene == 2:
        screen.blit(bg_image, (0, 0))
        draw_text(f"Stage: {str(stage)} / 5", game_font_reg, txt_color, 20, 20)
        screen.blit(player_image, player)
        if 1 <= stage <= 4:
            draw_enemy()
        elif stage == 5:
            draw_princess()
    elif scene == 3:
        screen.blit(bg_image, (0, 0))
        draw_enemy()
        draw_text("You touched the enemy (you lost)", game_font_big, txt_color, 200, 252.5)
        draw_text("press space to play again", game_font_big, txt_color, 320, 352.5)
        draw_text("or press esc, q, or end to exit.", game_font_big, txt_color, 250, 452.5)
    elif scene == 4:
        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (500, 580))
        draw_princess()
        draw_text("You saved the princess (you won)", game_font_big, txt_color, 200, 252.5)
        draw_text("press space to play again", game_font_big, txt_color, 320, 352.5)
        draw_text("or press esc, q, or end to exit.", game_font_big, txt_color, 250, 452.5)


def draw_enemy():
    global scene
    if stage == 4:
        screen.blit(enemy_image, enemy.rect)
    elif stage == 3:
        screen.blit(enemy_image, enemy.rect)
    elif stage == 2:
        screen.blit(enemy_image, enemy.rect)
    elif stage == 1:
        screen.blit(enemy_image, enemy.rect)
    else:
        screen.blit(enemy_image, enemy)

    e_move = enemy.speed

    if enemy.direction == "h":
        enemy.rect.x += e_move
        if enemy.rect.x <= enemy.start or enemy.rect.x >= enemy.end:
            enemy.speed = -e_move
        # Vertical Direction
    elif enemy.direction == "v":
        enemy.rect.y += e_move
        if enemy.rect.y <= enemy.start or enemy.rect.y >= enemy.end:
            enemy.speed = -e_move

    if player.colliderect(enemy.rect):
        # print("You lost! :(")
        # sys.exit()
        start_music("music/Infinite Perspective.mp3")
        scene = 3


def draw_text(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def draw_princess():
    global scene
    screen.blit(princess_image, princess)

    if player.colliderect(princess):
        # print("You won! :)")
        # sys.exit()
        start_music("music/Infinite Perspective.mp3")
        scene = 4


def start_music(name):
    global music_playing
    if not music_playing:
        pygame.mixer_music.load(name)
        pygame.mixer_music.play()
        music_playing = True
    else:
        stop_music()
        start_music(name)


def stop_music():
    global music_playing
    pygame.mixer_music.stop()
    music_playing = False


print()

start_music("music/Infinite Perspective.mp3")

# ==========================
# ===== MAIN GAME LOOP =====
# ==========================
while True:
    clock.tick(fps)
    # This for loop gets any keyboard, mouse, or other events that happen from user input
    for event in pygame.event.get():
        # The pygame.QUIT event happens when you close the game window
        if event.type == pygame.QUIT:
            print("You left the game. :|")
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if scene == 1:
                if key[pygame.K_SPACE] or key[pygame.K_s]:
                    scene = 2
                    start_music("music/Mesmerizing Galaxy Loop.mp3")
                elif key[pygame.K_q] or key[pygame.K_ESCAPE] or key[pygame.K_END]:
                    print("You left the game. :|")
                    sys.exit()
            elif scene == 2:
                if key[pygame.K_RIGHT] or key[pygame.K_d]:
                    if jumping:
                        player.move_ip(player_s + 3, 0)
                    else:
                        player.move_ip(player_s, 0)
                    if player.x >= size[0] - 90 and stage == 5:
                        player.x = size[0] - 90
                    elif player.x >= size[0] + 100:
                        stage += 1
                        player.x = -50
                elif key[pygame.K_LEFT] or key[pygame.K_a]:
                    if jumping:
                        player.move_ip(-player_s - 3, 0)
                    else:
                        player.move_ip(-player_s, 0)
                    if player.x <= 50 and stage == 1:
                        player.x = 50
                    if player.x <= -50:
                        stage -= 1
                        player.x = size[0]
                elif key[pygame.K_UP] or key[pygame.K_w]:
                    jumping = True
                    player.move_ip(0, -player_s)
                    if player.y <= 700:
                        player.y = 700
                elif key[pygame.K_q] or key[pygame.K_ESCAPE] or key[pygame.K_END]:
                    print("You left the game. :|")
                    sys.exit()
            elif scene == 3 or scene == 4:
                if key[pygame.K_SPACE] or key[pygame.K_s]:
                    stage = 1
                    scene = 2
                    player = pygame.Rect(player_x, player_y, player_w, player_h)
                    enemy = Enemy(enemy_x, enemy_y, enemy_w, enemy_h, enemy_s, "h", 50, 1450)
                    start_music("music/Mesmerizing Galaxy Loop.mp3")
                elif key[pygame.K_q] or key[pygame.K_ESCAPE] or key[pygame.K_END]:
                    print("You left the game. :|")
                    sys.exit()

    if jumping:
        player.y -= jump_v
        jump_v -= grav
        if jump_v < -jump_h:
            jumping = False
            jump_v = jump_h
    if player.y >= 580:
        player.y = 580

    draw_sprites()

    # At the end of each game loop, call pygame.display.flip() to update the screen with all of your sprites
    pygame.display.flip()
