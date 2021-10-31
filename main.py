    # -*- coding: utf-8 -*-

import pygame
from textboxify import TextBoxFrame
import textboxify
from sprite import Player
from buttons import Button
from level import Level
import random
from sprite import Stone_on_floor
from sprite import Stone_weapon
from sprite import Mob
from timer import Timer
from sprite import Donut
from sprite import Cool_stone
from sprite import Shoes
from sprite import Gas
from timergas import Timer_gas
from sprite import Cat
from sprite import Boss
"""
pygame.image.load() - returns Surface
Surface() - It's like plot on which I place pictures
Surface.get_rect() - returns Rect
Rect(left, top, width, height) - Saves coords of Surface
Surface.blit(surface, coords) = on_this.draw(this, coords) (coords=(x,y) or Rect) 

if event.type == pygame.MOUSEMOTION: event return (pos)
"""
# Create level instances






class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        # Set window
        self.window = pygame.display
        self.window.set_caption('Game')

        # Get user screen resolution
        self.window_width = self.window.Info().current_w
        self.window_height = self.window.Info().current_h

        # Set screen_surface
        self.screen_surface = self.window.set_mode(size=(self.window_width, self.window_height), flags=pygame.FULLSCREEN, depth=32)
        self.screen_surface.fill((150, 30, 0))

        # Camera_surface
        self.camera_surface = pygame.Surface((self.window_width, self.window_height))

        # Game State
        self.game_state = "Menu"
        # Pressed buttons on keyboard
        self.events = None

        # Create Mobs
        self.mobs = []
        self.full_heart = pygame.image.load('Art/full_heart.png').convert_alpha()
        self.empty_heart = pygame.image.load('Art/empty_heart.png').convert_alpha()

        #stone
        self.max_stone = 15
        self.player_stone = 0
        self.stone_floor = []
        self.gas_appears = []
        self.font= pygame.font.SysFont('Consolas', 30)
        self.stone_text = self.font.render("="+str(self.player_stone), False, (0,0,0))
        self.stone_dash=[]

        #win or lose screens
        self.win = pygame.image.load('Art/win.png').convert_alpha()
        self.win_rect = self.win.get_rect()
        self.lose = pygame.image.load('Art/lose.png').convert_alpha()
        self.lose_rect = self.lose.get_rect()

        self.donut = Donut(65, 235, "donut")
        self.cool_stone = Cool_stone(65, 2560, "cool_stone")
        self.shoes = Shoes(2760, 600, "speed")

        #music
        pygame.mixer.music.load('music.mp3')

        #dialogs

        self.dialog_group = pygame.sprite.LayeredDirty()
        dialog_text = "Невже це Ви, шукачко пригод ?! " \
                      " Кажани мені нашептали, що Ви шукаєте скарби Фараона," \
                      " але я не очікувала, що ви прибудете так швидко." \
                      " Ах так, я не представилася. Я була улюбленою кішкою Фараона," \
                      " чиї скарби Ви хочете зараз викрасти. Була улюбленицою до моменту, коли жрець не розповів" \
                      " моєму господареві якусь маячню, говорив, що я принесу йому невдачу і взагалі мене треба позбутися!" \
                      " А мій господар - дурень! Взяв й викинув на вулицю посеред ночі! Навіть їжі не дав у дорогу! " \
                      " Я не заслуговую на таке ставлення, тому хочу помститися Фараону - допомогти Вам викрасти усе, що у нього є" \
                      ". Шлях буде непростий, але я вірю у Ваші сили! Думаю лишень Ви зможете це зробити, постарайтеся" \
                      " й заради мене. До справи! Спочатку Вас очікує найскладніше завдання - пройти лабіринт. Звучить просто," \
                      " але насправді ще ні одна людина не вийшла звідти живою... Будьте обережними, aле пострайтеся" \
                      " пройти лабіринт швидко, згодом зрозумієте чому. " \
                      " Далі Ви стикнетеся з потойбічними істотами, які, до речі, завжди стріляють влучно. Останнє випробування" \
                      " навіть для мене є загадкою, але певна, що треба буде проявити усю свою ерудицію та кмітливість.          " \
                      "            " \
                      " Щасти Вам!                     "\
                      "*Натисніть Enter, щоб почати випробування*"

        info_1 = "Котик хоче з вами поговорити! Натисніть (S) для розмови"
        info_2 = "Для продовження натисніть (Enter)"
        self.info_text_1 = textboxify.TextBoxFrame(
            text=info_1,
            text_width=550,
            pos=(self.window_height / 2, self.window_width / 2.5),
            lines=2,
            bg_color=(255, 194, 88),
            font_color=(155, 62, 0),
            padding=(50, 50),
        )
        self.info_text_2 = textboxify.TextBoxFrame(
            text=info_2,
            text_width=457,
            pos=(self.window_height / 2, self.window_width / 2.5 - 60),
            bg_color=(255, 194, 88),
            font_color=(155, 62, 0),
            padding=(50, 50),
        )
        self.dialog_box = textboxify.TextBoxFrame(
            text=dialog_text,
            text_width=320,
            lines=5,
            pos=(self.window_height / 2, self.window_width / 2.5),
            padding=(150, 100),
            font_color=(100, 100, 100),
            font_size=26,
            bg_color=(255, 154, 64),
        )

        self.activate_lobby = True
        self.activate_lvl0 = False
        self.activate_lvl1 = False
        self.mob_spawn = False

        self.level1 = Level("lobby")

        self.count = 0
        self.score = 0

        self.dialog_group_1 = pygame.sprite.LayeredDirty()
        dialog_text_1 = "Привіт, дівчино! Я підготував тобі кілька загадок. Розгадай або помри " \
                        "Як давні єгиптяни називали священного бика?" \
                        "1. Апоп, 2. Апіс, 3. Нут, 4. Маас"

        self.count = 0
        self.score = 0
        info_3 = "Фараон приготував для тебе загадки!Натисніть (Ls) для розмови"
        info_4 = "Для продовження натисніть (Enter)"
        self.info_text_3 = textboxify.TextBoxFrame(
            text=info_3,
            text_width=550,
            pos=(self.window_height / 2, self.window_width / 2.5),
            lines=2,
            bg_color=(255, 194, 88),
            font_color=(155, 62, 0),
            padding=(50, 50),
        )
        self.info_text_4 = textboxify.TextBoxFrame(
            text=info_4,
            text_width=457,
            pos=(self.window_height / 2, self.window_width / 2.5 - 60),
            bg_color=(255, 194, 88),
            font_color=(155, 62, 0),
            padding=(50, 50),
        )
        self.dialog_box_1 = textboxify.TextBoxFrame(
            text=dialog_text_1,
            text_width=500,
            lines=5,
            pos=(self.window_height / 2, self.window_width / 2.5),
            padding=(50, 50),
            font_color=(92, 53, 102),
            font_size=26,
            bg_color=(255, 154, 64),
        )

        self.dialog_box_1.set_portrait()

    def toss_stone(self):
        for i in range(self.max_stone - self.player_stone - len(self.stone_floor)):
            x=random.randint(0, self.level1.level_size[0])
            y=random.randint(0, self.level1.level_size[1])
            stone=Stone_on_floor(x,y, "salt_15")
            self.stone_floor.append(stone)

    def stone_weapon(self):
        if self.player_stone == 0:
            pass
        else:
            self.player_stone -= 1
            live_stone = Stone_weapon(player.rect[0] + 32, player.rect[1] + 32, 15, "salt_15")
            if live_stone.up == 1:
                direction = "up"
            elif live_stone.down == 1:
                direction = "down"
            elif live_stone.right == 1:
                direction = "right"
            elif live_stone.left == 1:
                direction = "left"

            self.stone_dash.append([live_stone, direction])

    def gas_appear(self):
        for e in range(50):
            x=random.randint(0, 4500)
            y=random.randint(0, 4200)
            gas = Gas(x, y,  "gascl_small")
            self.gas_appears.append(gas)

    def mainloop(self):
        self.dialog_group.add( self.info_text_1 )
        self.dialog_group_1.add(self.info_text_3)
        self.gas_appear()
        while True:
            self.stone_text = self.font.render("=" + str(self.player_stone), False, (0, 0, 0))
            self.clock.tick(60)
            self.events = pygame.event.get()
            self.binds()
            if self.game_state == "Menu":
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.2)
                self.build_menu()
                self.mouse_on_button()
            elif self.game_state == "Playing":
                if player.health == 0:
                    self.screen_surface.fill((150, 30, 0))
                    self.you_lose()
                    self.build_menu_for_win_and_lose()
                    self.mouse_on_button()
                elif timergas.time_m == 0 and timergas.time_s == 0:
                    self.screen_surface.fill((150, 30, 0))
                    self.you_lose()
                    self.build_menu_for_win_and_lose()
                    self.mouse_on_button()
                else:
                    if self.activate_lobby:
                        self.draw_lobby()
                        if not self.dialog_group:
                            self.activate_lobby = False
                            self.activate_lvl0 = True
                            self.level1.surface.fill((108, 73, 34))
                            self.level1 = Level("level1")

                            player.rect[0],player.rect[1]=2810, 100
                            #self.level1.size_level()

                    elif self.activate_lvl0:
                        if player.collision_gas( self.gas_appears ) == 7:
                            timergas.prep_time()
                            timergas.reduce_time()
                        if player.max_health !=6:
                            player.collision_hp(self.donut)
                        if player.damage ==1:
                            player.collision_damage(self.cool_stone)
                        if player.max_speed ==20:
                            player.collision_speed(self.shoes)

                        player.move(self.level1.tile_list)

                        self.draw_level()
                        player.collision_gas(self.gas_appears)
                        for mob in self.mobs:
                            mob.behaviour(player)
                            player.get_damage(mob, self.mobs, self.level1.surface)
                        timer.reduce_time()
                        timer.prep_time()

                        self.gas = pygame.Rect(10, 50, (timergas.time_m * 60 + timergas.time_s) / 1.3, 10)
                        pygame.draw.rect(self.screen_surface, (100, 30, 200), self.gas)
                        if player.rect[1] >=4190 and player.rect[0]>=4098:
                            self.activate_lvl0 = False
                            self.activate_lvl1 = True
                            self.mob_spawn = True
                            
                            self.level1.surface.fill((108, 73, 34))
                            self.level1 = Level("level2")

                            player.rect[0], player.rect[1] = 500, 500
                            self.dialog_group_1.add(self.info_text_3)
                    elif self.activate_lvl1:
                        self.level1.surface.fill((108, 73, 34))
                        self.level1 = Level("level2")
                        if (self.mob_spawn == True):
                            self.create_melee()
                            self.mob_spawn = False
                        if self.score == 3:
                            self.screen_surface.fill((150, 30, 0))
                            self.you_win()
                            self.build_menu_for_win_and_lose()
                            self.mouse_on_button()
                        elif self.score < 3 and self.count == 3:
                            self.screen_surface.fill((150, 30, 0))
                            self.you_lose()
                            self.build_menu_for_win_and_lose()
                            self.mouse_on_button()
                        else:
                            self.draw_level2()
                            player.move(self.level1.fire_list)


                self.window.update()
                pygame.display.flip()

    def binds(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.stone_weapon()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pygame.time.Clock().tick( 60 )
                self.info_text_1.kill()
                if not self.dialog_group:
                    self.dialog_group.add(self.info_text_2)
                    self.dialog_group.add( self.dialog_box )

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                if self.dialog_box.words:
                    self.dialog_box.reset()

                else:
                    self.dialog_box.reset(hard = True)
                    self.dialog_box.set_text("А котик зайнятий!")
                    self.dialog_box.kill()
                    self.info_text_2.kill()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                pygame.time.Clock().tick( 60 )
                self.info_text_3.kill()
                if not self.dialog_group_1:
                    self.dialog_group_1.add(self.info_text_4)
                    self.dialog_group_1.add(self.dialog_box_1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Cleans the text box to be able to go on printing text
                # that didn't fit, as long as there are text to print out.
                if self.dialog_box_1.words:
                    self.dialog_box_1.reset()

                # Whole message has been printed and the box can now reset
                # to default values, set a new text to print out and close
                # down itself.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2 and self.count == 0:
                self.score += 1
                self.count += 1
                self.dialog_box_1.reset(hard=True)
                self.dialog_box_1.set_text("Він дожив до 96 років, мав 48 синів та 40 дочок. Про кого йдеться" \
                        "1. Хеопс, 2. Рамзес 2, 3. Пепі, 4. Аменхотеп")

                if not self.dialog_group_1:
                    self.dialog_group_1.add(self.dialog_box_1)
            elif self.count == 0 and event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_3 or event.key == pygame.K_4):
                self.count += 1
                self.dialog_box_1.reset(hard=True)
                self.dialog_box_1.set_text("Він дожив до 96 років, мав 48 синів та 40 дочок. Про кого йдеться" \
                                        "1. Хеопс, 2. Рамзес 2, 3. Пепі, 4. Аменхотеп")

                if not self.dialog_group_1:
                    self.dialog_group_1.add(self.dialog_box_1)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2 and self.count == 1:
                self.score += 1
                self.count += 1
                self.dialog_box_1.reset(hard=True)
                self.dialog_box_1.set_text("Як називалася корона фараона після об'єднання Нижнього та Верхнього Єгипту?" \
                                          "1. Хеопс, 2. Дешрет 2, 3. Хеджет, 4. Пшент")
                if not self.dialog_group_1:
                    self.dialog_group_1.add(self.dialog_box_1)

            elif self.count == 1 and event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_3 or event.key == pygame.K_4):
                self.count += 1
                self.dialog_box_1.reset(hard=True)
                self.dialog_box_1.set_text("Як називалася корона фараона після об'єднання Нижнього та Верхнього Єгипту?" \
                                           "1. Хеопс, 2. Дешрет 2, 3. Хеджет, 4. Пшент")
                if not self.dialog_group_1:
                    self.dialog_group_1.add(self.dialog_box_1)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4 and self.count == 2:
                self.score += 1
                self.count += 1
                self.dialog_box_1.reset(hard=True)
                self.dialog_box_1.set_text(f"Ти набрав {self.score}/3 балів")
                if not self.dialog_group_1:
                    self.dialog_group_1.add(self.dialog_box_1)
            elif self.count == 2 and event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3):
                self.count += 1
                self.dialog_box_1.reset(hard=True)
                self.dialog_box_1.set_text(f"Ти набрав {self.score}/3 балів")
                if not self.dialog_group_1:
                    self.dialog_group_1.add(self.dialog_box_1)

            if self.game_state == "Menu" and event.type == pygame.ACTIVEEVENT:
                self.build_menu()
                self.window.update()
            elif self.game_state == "Playing" and event.type == pygame.ACTIVEEVENT:
                self.draw_level()
                self.window.update()
        self.dialog_group.update()
        self.dialog_group_1.update()

    def mouse_on_button(self):
        for event in self.events:
            if event.type == 1025 and event.button == 1:
                if button_start.rect[0] < event.pos[0] < button_start.rect[0] + button_start.rect[2] and \
                button_start.rect[1] < event.pos[1] < button_start.rect[1] + button_start.rect[3]:
                    self.game_state = "Playing"
                    self.window.update()
            if event.type == 1025 and event.button == 1:
                if button_exit.rect[0] < event.pos[0] < button_exit.rect[0] + button_exit.rect[2] and \
                button_exit.rect[1] < event.pos[1] < button_exit.rect[1] + button_exit.rect[3]:
                    pygame.quit()
                    exit()

    def draw_level(self):


        self.level1.surface.fill((108, 73, 34))
        self.level1.surface.blit(player.surface, player.rect)
        for gas in self.gas_appears:
            self.level1.surface.blit( gas.surface, gas.rect )
        for heart in range(player.health):
            self.camera_surface.blit(self.full_heart, (heart * 50 + 10, 5))
        for heart in range(player.max_health):
            if heart < player.health:
                self.camera_surface.blit(self.full_heart, (heart * 50 + 10, 5))
            else:
                self.camera_surface.blit(self.empty_heart, (heart * 50 + 10, 5))

        x_rect_camera = player.rect[0] - (self.window_width / 2)
        y_rect_camera = player.rect[1] - (self.window_height / 2)
        if player.max_health != 6:
            self.level1.surface.blit(self.donut.surface, self.donut.rect)
        else:
            self.donut =0
        if player.damage == 1:
            self.level1.surface.blit(self.cool_stone.surface, self.cool_stone.rect)
        else:
            self.cool_stone = 0
        if player.max_speed == 20:
            self.level1.surface.blit(self.shoes.surface, self.shoes.rect)
        else:
            self.shoes = 0
        self.level1.build_level()
        self.screen_surface.blit(self.camera_surface, (0, 0))
        if x_rect_camera <= 0:
            x_rect_camera = 0
        elif x_rect_camera  + self.window_width >= self.level1.level_size[0]:
            x_rect_camera = self.level1.level_size[0] - self.window_width
        if y_rect_camera   <= 0:
            y_rect_camera = 0
        elif y_rect_camera  + self.window_height>= self.level1.level_size[1]:
            y_rect_camera = self.level1.level_size[1] - self.window_height
        self.camera_surface.blit(self.level1.surface, (0, 0), area=(x_rect_camera, y_rect_camera, self.window_width, self.window_height))


    def build_menu(self):
        self.screen_surface.blit(button_start.surface, button_start.rect)
        self.screen_surface.blit(button_exit.surface, button_exit.rect)
    def build_menu_for_win_and_lose(self):
        self.screen_surface.blit(button_exit.surface, button_exit.rect)

    def you_win(self):
        self.screen_surface.blit(self.win, ((self.window_width - self.win_rect[2])/2,(self.window_height - self.lose_rect[3])/2))
        self.screen_surface.blit(button_exit.surface, button_exit.rect)

    def you_lose(self):
        self.screen_surface.blit(self.lose, ((self.window_width - self.lose_rect[2])/2,(self.window_height - self.lose_rect[3])/2))
        self.screen_surface.blit(button_exit.surface, button_exit.rect)


    def draw_lobby(self):
        self.level1.surface.fill((108, 73, 34))
        timer.time_rect[0] = self.window_width - 200
        self.dialog_group.draw( self.camera_surface )
        self.level1.surface.blit(player.surface, player.rect)
        self.level1.surface.blit( cat.surface, cat.rect )
        self.level1.build_level()

        self.screen_surface.blit(self.camera_surface, (0, 0))
        x_rect_camera = player.rect[0] - (self.window_width / 2)
        y_rect_camera = player.rect[1] - (self.window_height / 2)
        if x_rect_camera <= 0:
            x_rect_camera = 0
        elif x_rect_camera + self.window_width >= self.level1.level_size[0]:
            x_rect_camera = self.level1.level_size[0] - self.window_width
        if y_rect_camera <= 0:
            y_rect_camera = 0
        elif y_rect_camera + self.window_height >= self.level1.level_size[1]:
            y_rect_camera = self.level1.level_size[1] - self.window_height
        self.camera_surface.blit(self.level1.surface, (0, 0),
                                 area=(x_rect_camera, y_rect_camera, self.window_width, self.window_height))

    def create_melee(self):
        for mob_number in range(10):
            x = random.randint(200, self.level1.level_size[0])
            y = random.randint(200, self.level1.level_size[1])
            max_speed = random.randint(2, 4)
            mob = Mob(x, y, max_speed, 'skeleton_front')
            self.mobs.append(mob)


    def draw_level2(self):
        self.level1.surface.fill((100, 63, 0))
        timer.time_rect[0] = self.window_width - 200
        if player.rect.x > 1800:
            self.dialog_group_1.draw(self.camera_surface)

        self.level1.surface.blit(player.surface, player.rect)
        self.level1.surface.blit(boss.surface, boss.rect)

        self.level1.build_level()

        for mob in self.mobs:
            mob.behaviour(player)
            self.level1.surface.blit(mob.surface, mob.rect)

        self.screen_surface.blit(self.camera_surface, (0, 0))
        x_rect_camera= player.rect[0]-(self.window_width/2)
        y_rect_camera= player.rect[1]-(self.window_height/2)
        if x_rect_camera <= 0:
            x_rect_camera = 0
        elif x_rect_camera  + self.window_width >= self.level1.level_size[0]:
            x_rect_camera = self.level1.level_size[0] - self.window_width
        if y_rect_camera   <= 0:
            y_rect_camera = 0
        elif y_rect_camera  + self.window_height>= self.level1.level_size[1]:
            y_rect_camera = self.level1.level_size[1] - self.window_height
        self.camera_surface.blit(self.level1.surface, (0, 0), area=(x_rect_camera, y_rect_camera, self.window_width, self.window_height))




# Create game instance
game = Game()

# Create player
player = Player(500, 500, 20, 'front_stand')
cat = Cat(800, 300, 0, 'cat')
boss = Boss(2200, 450, 4, 'boss')
timer = Timer()
timergas = Timer_gas()

# Create buttons
button_start = Button("midtop", game.window_width/2, 100, 'button_start')
button_exit = Button("midtop", game.window_width/2, 500, 'button_exit')




# Start
game.mainloop()

#player = Player(1794, 64, 10, 'character_standing_front')
