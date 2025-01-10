from random import randint
import pygame

pygame.init()
pygame.display.init()

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h

clock = pygame.time.Clock()
FPS = 120

### Ball Stuff ###

UPLEFT = 0
DOWNLEFT = 1
UPRIGHT = 2
DOWNRIGHT = 3

### Colors ###

WHITE = (255,255,255)
BLACK = (0,0,0)

### Creating the screen ###

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE, 32)
surface_rect = screen.get_rect()

class Border(pygame.sprite.Sprite):

    def __init__(self, border):
        pygame.sprite.Sprite.__init__(self)
        self.border = border

        if self.border == 'bottom' or self.border == 'top':
            self.image = pygame.Surface([W, 1])
        else:
            self.image = pygame.Surface([1, H])

        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        if self.border in ['left', 'right']:
            self.rect.centerx = getattr(screen.get_rect(), self.border)
            if self.border == 'right': self.rect.centerx -= 1
        if self.border in ['top' ,'bottom']:
            self.rect.centery = getattr(screen.get_rect(), self.border)
            if self.border == 'bottom': self.rect.centery -= 1

class Object(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('dvd.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = surface_rect.centerx
        self.rect.centery = surface_rect.centery
        self.direction = randint(0,3)
        self.speed = 1

    def move(self):
        if self.direction == UPLEFT:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        elif self.direction == UPRIGHT:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        elif self.direction == DOWNLEFT:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        elif self.direction == DOWNRIGHT:
            self.rect.x += self.speed
            self.rect.y += self.speed

logo = Object()
border_left = Border('left')
border_right = Border('right')
border_top = Border('top')
border_bottom = Border('bottom')

all_sprites = pygame.sprite.RenderPlain(border_left, border_right, border_top, border_bottom, logo)

def border_hit():
    if pygame.sprite.collide_rect(logo, border_left):
        if logo.direction == UPLEFT:
            logo.direction = UPRIGHT
        elif logo.direction == DOWNLEFT:
            logo.direction = DOWNRIGHT
    elif pygame.sprite.collide_rect(logo, border_right):
        if logo.direction == UPRIGHT:
            logo.direction = UPLEFT
        elif logo.direction == DOWNRIGHT:
            logo.direction = DOWNLEFT
    elif pygame.sprite.collide_rect(logo, border_top):
        if logo.direction == UPLEFT:
            logo.direction = DOWNLEFT
        elif logo.direction == UPRIGHT:
            logo.direction = DOWNRIGHT
    elif pygame.sprite.collide_rect(logo, border_bottom):
        if logo.direction == DOWNLEFT:
            logo.direction = UPLEFT
        elif logo.direction == DOWNRIGHT:
            logo.direction = UPRIGHT

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False
            pygame.quit()

    if run:
        all_sprites.update()
        screen.fill(BLACK)
        all_sprites.draw(screen)

        logo.move()
        border_hit()

        pygame.display.update()
