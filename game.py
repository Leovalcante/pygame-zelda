import sys

import pygame

import config
from level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption("PyZelda")
        self.clock = pygame.time.Clock()

        self.level = Level()

    @staticmethod
    def __quit():
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__quit()
                    if event.key == pygame.K_q:
                        self.__quit()

            self.screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(config.fps)


if __name__ == "__main__":
    Game().run()
