import pygame

import config
from player import Player
from tile import Tile

from debug import debug


class Level:
    def __init__(self) -> None:
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.display = pygame.display.get_surface()

        self.player = None
        self.create_map()

    def create_map(self):
        for irow, row in enumerate(config.WORLD_MAP):
            for icol, col in enumerate(row):
                x = irow * config.tilesize
                y = icol * config.tilesize
                if col == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                elif col == "p":
                    self.player = Player(
                        (x, y), self.obstacles_sprites, [self.visible_sprites]
                    )

    def run(self):
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
        self.display = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, player):
        display_size = self.display.get_size()
        self.offset.x = player.rect.centerx - display_size[0] // 2
        self.offset.y = player.rect.centery - display_size[1] // 2

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset)
