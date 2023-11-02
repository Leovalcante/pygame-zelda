import pygame

import config


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None) -> None:
        super().__init__(*groups)
        self.image = surface
        if self.image is None:
            self.image = pygame.Surface([config.tilesize] * 2)

        self.sprite_type = sprite_type
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
