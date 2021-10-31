import pygame



class Fog():
    def __init__(self,level1):
        self.fog = pygame.Surface((level1.level_size[0], level1.level_size[1]), pygame.SRCALPHA)
        self.fog.fill((0, 0, 0, 255))
    def render_fog(self, x,y):

        self.fog.fill((0, 0, 0, 255))
        # self.fog.blit(self.player.seen, (0, 0))
        m = 255 / float(450)
        for i in range(450, 1, -1):
            pygame.draw.circle(self.fog, (0, 0, 0, i * m), (x, y), i)


def create_gas(self):
    smoke = []
    for i in range(30):
        smoke.append([300, 300])
        # put within your game loop
        for i in smoke:
            i[1] -= 5
            i[0] += random.randint(-10, 10)
            if i[1] < 0:
                smoke.remove(i)
            else:
                pygame.draw.rect(level1.surface, (23, 114, 69), (i[0], i[1], 4, 4))
            pygame.time.Clock().tick(60)