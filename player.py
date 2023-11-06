import os

import pygame

from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            "./assets/graphics/test/player.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.import_player_assets()

        self.movement = pygame.Vector2()
        self.speed = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = os.path.join("assets", "graphics", "player")
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_attack": [],
            "down_attack": [],
            "left_attack": [],
            "right_attack": [],
        }
        for animation in self.animations:
            animation_path = os.path.join(character_path, animation)
            self.animations[animation] = import_folder(animation_path)
        print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_UP]:
            self.movement.y = -1
        elif keys[pygame.K_DOWN]:
            self.movement.y = 1
        else:
            self.movement.y = 0

        if keys[pygame.K_LEFT]:
            self.movement.x = -1
        elif keys[pygame.K_RIGHT]:
            self.movement.x = 1
        else:
            self.movement.x = 0

        # attack input
        if keys[pygame.K_x] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("attack")
        # magic input
        if keys[pygame.K_z] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("magic")

    def move(self, speed):
        if self.movement and not self.movement.is_normalized():
            self.movement = self.movement.normalize()

        self.hitbox.x += self.movement.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.movement.y * speed
        self.collision("vertical")

        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.movement.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.movement.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.movement.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.movement.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def update(self):
        self.input()
        self.cooldowns()
        self.move(self.speed)
