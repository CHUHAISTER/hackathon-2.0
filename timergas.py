import pygame.font
import time

class Timer_gas:
    def __init__(self):
        self.bg_color = (108, 73, 34)
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 80)

        self.time_m = 5
        self.time_s = 0
        self.prep_time()

    def reduce_time(self):
        if self.time_s == 0:
            self.time_m -= 1
            self.time_s = 60
        self.time_s -= 1
        time.sleep(0)
        self.prep_time()

    def prep_time(self):
        time_m_str = str(self.time_m)
        time_s_str = str(self.time_s)

        if self.time_m < 10:
            time_m_str = f"0{time_m_str}"
        if self.time_s < 10:
            time_s_str = f"0{time_s_str}"

        self.time_image = self.font.render(f"{time_m_str}:{time_s_str}", True,
                                           self.text_color, self.bg_color)

        self.time_rect = self.time_image.get_rect()





