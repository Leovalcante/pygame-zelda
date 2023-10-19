import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(
            "./assets/graphics/test/player.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.movement = pygame.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

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

    def update(self):
        self.input()
        self.move(self.speed)
