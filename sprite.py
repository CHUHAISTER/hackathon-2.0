# -*- coding: utf-8 -*-

"""
x, y - start position (top left corner)
image - image
"""
import random
import pygame
import pyganim
from pygame.surface import Surface
import math

animation_delay = 100

#stand > go_1 > go_2 > go_1 > stand  > go_3 > go_4 > go_3 > stand

anim_move_up = [
    "Art/Hackathon/back_stand.png",
    "Art/Hackathon/back_go_1.png",
    "Art/Hackathon/back_go_2.png",
    "Art/Hackathon/back_go_1.png",
    "Art/Hackathon/back_stand.png",
    "Art/Hackathon/back_go_3.png",
    "Art/Hackathon/back_go_4.png",
    "Art/Hackathon/back_go_3.png",
    "Art/Hackathon/back_stand.png",
]
anim_move_down = [
    "Art/Hackathon/front_stand.png",
    "Art/Hackathon/front_go_1.png",
    "Art/Hackathon/front_go_2.png",
    "Art/Hackathon/front_go_1.png",
    "Art/Hackathon/front_stand.png",
    "Art/Hackathon/front_go_3.png",
    "Art/Hackathon/front_go_4.png",
    "Art/Hackathon/front_go_3.png",
    "Art/Hackathon/front_stand.png",
]
anim_move_right = [
    "Art/Hackathon/r_stand.png",
    "Art/Hackathon/r_go_1.png",
    "Art/Hackathon/r_go_2.png",
    "Art/Hackathon/r_go_1.png",
    "Art/Hackathon/r_stand.png",
    "Art/Hackathon/r_go_3.png",
    "Art/Hackathon/r_go_4.png",
    "Art/Hackathon/r_go_3.png",
    "Art/Hackathon/r_stand.png",
]
anim_move_left = [
    "Art/Hackathon/l_stand.png",
    "Art/Hackathon/l_go_1.png",
    "Art/Hackathon/l_go_2.png",
    "Art/Hackathon/l_go_1.png",
    "Art/Hackathon/l_stand.png",
    "Art/Hackathon/l_go_3.png",
    "Art/Hackathon/l_go_4.png",
    "Art/Hackathon/l_go_3.png",
    "Art/Hackathon/l_stand.png",
]
up=0
down=0
right=0
left=0

def make_animation(anim_list, delay):
    boltAnim = []
    for anim in anim_list:
        boltAnim.append((anim, delay))
    Anim = pyganim.PygAnimation(boltAnim)
    return Anim

class Sprite:
    def __init__(self, x, y, image):
        self.surface = pygame.image.load("Art/%s.png" % image)
        self.rect = self.surface.get_rect(topleft=(x, y))

    def draw(self):
        pass


class MovableSprite(Sprite):
    def __init__(self, x, y, max_speed, image):
        super().__init__(x, y, image)

        self.ax = 1
        self.ay = 1
        self.max_speed = max_speed
        self.dx = 0
        self.dy = 0
    def collision(self, tile_list):
        for tile in tile_list:
            if self.rect[0] + self.rect[2] + self.dx < tile[0]+1 or self.rect[0] + self.dx > tile[0]+99:
                continue
            if self.rect[1] + self.rect[3] + self.dy < tile[1]+1 or self.rect[1] + self.dy > tile[1]+99:
                continue
            self.dx = 0
            self.dy =0
    def collision_stone(self, stone_list):
        for i in range(len(stone_list)):
            if self.rect[0] + self.rect[2] + self.dx < stone_list[i].rect[0]+1 or self.rect[0] + self.dx > stone_list[i].rect[0]+17:

                continue
            if self.rect[1] + self.rect[3] + self.dy < stone_list[i].rect[1]+1 or self.rect[1] + self.dy > stone_list[i].rect[1]+17:

                continue
            stone_list[i]="0"
        return stone_list



class Player(MovableSprite):
    def __init__(self, x, y, max_speed, image):
        super().__init__(x, y, max_speed, image)
        self.surface = Surface((50,80))
        self.surface = pygame.image.load("Art/%s.png" % image)
        self.health = 5
        self.max_health = 5
        self.damage=1

        #animation create
        self.anim_move_up= make_animation(anim_move_up, animation_delay)
        self.anim_move_up.play()
        self.anim_move_down = make_animation(anim_move_down, animation_delay)
        self.anim_move_down.play()
        self.anim_move_right = make_animation(anim_move_right, animation_delay)
        self.anim_move_right.play()
        self.anim_move_left = make_animation(anim_move_left, animation_delay)
        self.anim_move_left.play()


    def move(self, tile_list):
        global up
        global down
        global right
        global left
        # Get all pressed keys on keyboard
        keys = pygame.key.get_pressed()
        # Move Ox
        if keys[pygame.K_RIGHT] and abs(self.dx) != self.max_speed:
            self.dx += self.ax
            self.surface.fill((108, 73, 34))
            self.anim_move_right.blit(self.surface, (0,0))
            up = 0
            down = 0
            right = 1
            left = 0
        elif keys[pygame.K_LEFT] and abs(self.dx) != self.max_speed:
            self.dx -= self.ax
            self.surface.fill((108, 73, 34))
            self.anim_move_left.blit(self.surface, (0, 0))
            up = 0
            down = 0
            right = 0
            left = 1
        elif self.dx > 0:
            self.dx -= self.ax
        elif self.dx < 0:
            self.dx += self.ax
        # Move Oy
        if keys[pygame.K_DOWN] and abs(self.dy) != self.max_speed:
            self.dy += self.ay
            self.surface.fill((108, 73, 34))
            self.anim_move_down.blit(self.surface, (0, 0))
            up = 0
            down = 1
            right = 0
            left = 0
        elif keys[pygame.K_UP] and abs(self.dy) != self.max_speed:
            self.dy -= self.ay
            self.surface.fill((108, 73, 34))
            self.anim_move_up.blit(self.surface, (0, 0))
            up = 1
            down = 0
            right = 0
            left = 0
        elif self.dy > 0:
            self.dy -= self.ay
        elif self.dy < 0:
            self.dy += self.ay

        self.collision(tile_list)
        self.rect[0] = self.rect[0] + self.dx
        self.rect[1] = self.rect[1] + self.dy


    def get_damage(self, mob, mobs, screen_surface):
        for self.heart in range (self.max_health):
            if self.rect[0] + self.rect[2] + self.dx < mob.rect[0] + 1 or self.rect[0] + self.dx > \
                    mob.rect[0] + 30:
                continue
            if self.rect[1] + self.rect[3] + self.dy < mob.rect[1] + 1 or self.rect[1] + self.dy > \
                    mob.rect[1] + 30:
                continue


            if (screen_surface.get_rect().left + 350) > mobs[mobs.index(mob)].rect.x:
                mobs[mobs.index(mob)].rect.x += random.randint(350, 600)
            elif (screen_surface.get_rect().right - 350) < mobs[mobs.index(mob)].rect.x:
                mobs[mobs.index(mob)].rect.x -= random.randint(350, 600)
            else:
                mobs[mobs.index(mob)].rect.x += random.randint(-700, 700)
            if (screen_surface.get_rect().top + 350) > mobs[mobs.index(mob)].rect.y:
                mobs[mobs.index(mob)].rect.y += random.randint(350, 600)
            elif (screen_surface.get_rect().bottom - 350) < mobs[mobs.index(mob)].rect.y:
                mobs[mobs.index(mob)].rect.y -= random.randint(350, 600)
            else:
                mobs[mobs.index(mob)].rect.y += random.randint(-700, 700)
            self.health -= 1

    def collision_hp(self, donut):
            if self.rect[0] + self.rect[2] + self.dx < donut.rect[0]+1 or self.rect[0] + self.dx > donut.rect[0]+63:
                return 0
            if self.rect[1] + self.rect[3] + self.dy < donut.rect[1]+1 or self.rect[1] + self.dy > donut.rect[1]+63:
                return 0
            self.health +=1
            self.max_health +=1
    def collision_damage(self, donut):
            if self.rect[0] + self.rect[2] + self.dx < donut.rect[0]+1 or self.rect[0] + self.dx > donut.rect[0]+63:
                return 0
            if self.rect[1] + self.rect[3] + self.dy < donut.rect[1]+1 or self.rect[1] + self.dy > donut.rect[1]+63:
                return 0
            self.damage +=1

    def collision_speed(self, donut):
            if self.rect[0] + self.rect[2] + self.dx < donut.rect[0]+1 or self.rect[0] + self.dx > donut.rect[0]+63:
                return 0
            if self.rect[1] + self.rect[3] + self.dy < donut.rect[1]+1 or self.rect[1] + self.dy > donut.rect[1]+63:
                return 0
            self.max_speed +=5

    def collision_gas(self, gas_appears):
        for i in range(len(gas_appears)):
            if self.rect[0] + self.rect[2] + self.dx < gas_appears[i].rect[0]+1 or self.rect[0] + self.dx > gas_appears[i].rect[0]+99:

                continue
            if self.rect[1] + self.rect[3] + self.dy < gas_appears[i].rect[1]+1 or self.rect[1] + self.dy > gas_appears[i].rect[1]+99:

                continue
            return 7





class Mob(MovableSprite):
    def __init__(self, x, y, max_speed, image):
        super().__init__(x, y, max_speed, image)
        self.rect = self.surface.get_rect(topleft=(x, y))

    def behaviour(self, player):
        dirvect = pygame.math.Vector2( player.rect.x - self.rect.x, player.rect.y - self.rect.y)

        self.er = player.rect.x - self.rect.x
        self.ex = player.rect.y - self.rect.y
        dist: float = math.hypot( self.er, self.ex )
        if player.rect.x != self.rect.x and player.rect.y != self.rect.y and dist < 700:

            dirvect.normalize()
            dirvect.scale_to_length(self.max_speed)
            self.rect.move_ip(dirvect)
            if self.max_speed <= len(dirvect):
                pass
    def collision_dead(self, tile_list):
        for tile in tile_list:
            if self.rect[0] + self.rect[2] + self.dx < tile[0].rect[0]+1 or self.rect[0] + self.dx > tile[0].rect[0]+63:
                continue
            if self.rect[1] + self.rect[3] + self.dy < tile[0].rect[1]+1 or self.rect[1] + self.dy > tile[0].rect[1]+63:
                continue


            return tile_list.index(tile)

class Tile(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Stone_on_floor(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Stone_weapon(MovableSprite):
    def __init__(self,x,y,max_speed, image):
        super().__init__(x,y,max_speed, image )
        self.start_x = x
        self.start_y = y
        self.up = up
        self.down = down
        self.right = right
        self.left = left
    def collision_mmm(self, tile_list):
        for tile in tile_list:
            if self.rect[0] + self.rect[2] + self.dx < tile[0]+1 or self.rect[0] + self.dx > tile[0]+63:
                continue
            if self.rect[1] + self.rect[3] + self.dy < tile[1]+1 or self.rect[1] + self.dy > tile[1]+63:
                continue
            return 1

class Donut(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
class Cool_stone(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
class Shoes(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Gas(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)



class Cat (MovableSprite ):

    def __init__(self, x, y, max_speed, image):
        super().__init__( x, y, max_speed, image )
        self.rect = self.surface.get_rect( topleft=(x, y) )

class Boss(MovableSprite):
    def __init__(self, x, y, max_speed, image):
        super().__init__(x, y, max_speed, image)
        self.rect = self.surface.get_rect(midright=(x, y))

class Archer(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        # Ray settings
        self.fov = math.pi / 3  # 60 degrees
        self.angle = 0  # Start look
        self.ray_number = 1  # I draw N rays
        self.d_angle = self.fov / self.ray_number  # angle between rays inside
        self.fov_length = 640  # How far I can see
        self.shuriken = None

    def behaviour(self):
        pass

class Shuriken(MovableSprite):
    def __init__(self, x, y, max_speed, image, player):
        super().__init__(x, y, max_speed, image)
        self.x = x
        self.y = y
        self.max_speed = max_speed
        self.player = player
        self.dx = -((self.x - player.rect[0]) / max_speed)
        self.dy = -((self.y - player.rect[1]) / max_speed)

    def collision_mmm(self, player):
        if self.rect[0] + self.rect[2] + self.dx < player.rect[0] or self.rect[0] + self.dx > player.rect[0]+player.rect[2]:
            if self.rect[1] + self.rect[3] + self.dy < player.rect[1] or self.rect[1] + self.dy > player.rect[1]+player.rect[3]:
                del self

    def move(self, level):
        self.rect[0] += self.dx
        self.rect[1] += self.dy
        self.collision_mmm(self.player)
        level.surface.blit(self.surface, self.rect)

