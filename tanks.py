import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
TILE = 28

class Tank:
    def __init__(self, color, px, py, direct, keysList, shotDelay, moveSpeed, hp):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = moveSpeed
        self.hp = hp

        self.shotTimer = 0
        self.shotDelayA = 5
        self.shotDelay = shotDelay
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT, self.keyRIGHT, self.keyUP, self.keyDOWN, self.keySHOT = keysList

    def update(self):
        oldX, oldY = self.rect.topleft
        if keys[self.keyUP]:
            if self.rect.y > 0:
                self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyRIGHT]:
            if self.rect.x < WIDTH - TILE:
                self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyDOWN]:
            if self.rect.y < HEIGHT - TILE:
                self.rect.y += self.moveSpeed
            self.direct = 2
        elif keys[self.keyLEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.moveSpeed
            self.direct = 3

        for obj in objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pygame.draw.line(window, 'white', self.rect.center, (x, y), 4)

    def damage(self, value):
        self.hp -= value
        print(self.color, 'HP:', self.hp)
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'is dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

        bullets.append(self)

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 15

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(window, 'green', self.rect)
        pygame.draw.rect(window, 'gray20', self.rect, 2)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


bullets = []
objects = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), 20, 5, 10)
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RCTRL), 5, 2, 20)
for _ in range(10):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj):
                fined = True
        if not fined:
            break

    Block(x, y, 50)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    for bullet in bullets:
        bullet.update()
    for obj in objects:
        obj.update()

    window.fill('black')
    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
