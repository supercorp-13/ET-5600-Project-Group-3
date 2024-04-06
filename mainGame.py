import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('platformer')
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        self.original_img = pygame.image.load('cloud_1.png')
        self.image = pygame.transform.scale(self.original_img, (50, 50))
        self.image.set_colorkey((0, 0, 0))

        self.img_pos = [100, 100]
        self.movement = [False, False]

        self.collision_area = pygame.Rect(50, 50, 300, 50)

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))

            self.img_pos[1] += self.movement[1] - self.movement[0]
            self.screen.blit(self.image, self.img_pos)

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.image.get_width(), self.image.get_height())

            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 225), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)

Game().run()
