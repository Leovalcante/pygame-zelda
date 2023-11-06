import os
import random

import pygame

import config
from player import Player
from support import import_csv_layout, import_folder
from tile import Tile

from debug import debug


class Level:
    def __init__(self) -> None:
        self.display = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        layouts = {
            "boundary": import_csv_layout(
                os.path.join("assets", "map", "map_FloorBlocks.csv")
            ),
            "grass": import_csv_layout(os.path.join("assets", "map", "map_Grass.csv")),
            "object": import_csv_layout(
                os.path.join("assets", "map", "map_Objects.csv")
            ),
        }
        graphics = {
            "grass": import_folder(os.path.join("assets", "graphics", "grass")),
            "objects": import_folder(os.path.join("assets", "graphics", "objects")),
        }
        for style, layout in layouts.items():
            for irow, row in enumerate(layout):
                for icol, col in enumerate(row):
                    if col != "-1":
                        x = icol * config.tilesize
                        y = irow * config.tilesize
                        if style == "boundary":
                            Tile(
                                (x, y),
                                [self.obstacles_sprites],
                                "invisible",
                            )
                        if style == "grass":
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacles_sprites],
                                "grass",
                                random.choice(graphics["grass"]),
                            )
                        if style == "object":
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacles_sprites],
                                "object",
                                graphics["objects"][int(col)],
                            )
        self.player = Player(
            pygame.Vector2(20, 31) * config.tilesize,
            [self.visible_sprites],
            self.obstacles_sprites,
        )

    def run(self):
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
        self.display = pygame.display.get_surface()
        self.offset = pygame.Vector2()

        self.floor_surface = pygame.image.load(
            os.path.join("assets", "graphics", "tilemap", "ground.png")
        ).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def draw(self, player):
        display_size = self.display.get_size()
        self.offset.x = player.rect.centerx - display_size[0] // 2
        self.offset.y = player.rect.centery - display_size[1] // 2
        self.display.blit(self.floor_surface, self.floor_rect.topleft - self.offset)
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset)
