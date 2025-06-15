import pygame
pygame.init()
from pygame import mixer
mixer.init()
import random
import time
from pygame import font

pygame.init()
W, H = 700, 500
FPS = 60
BLACK = 0, 0, 0
font = font.SysFont('Arial', 100)
i = 0
k = 0
num_fire = 0

window = pygame.display.set_mode((W, H))
pygame.display.set_caption('SPACE')
background_image = pygame.transform.scale(pygame.image.load('galaxy.jpg'), (W, H))

clock = pygame.time.Clock()
pygame.mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, weight, height, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), (weight, height))
        self.speed = speed
        self.rect = self.image.get_rect() #hitbox
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < W:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 5, 10, 4)
        bullets.add(bullet)
        mixer.music.load('fire.ogg')
        mixer.music.play()
        
class Enemy(GameSprite):
    def update(self):
        global k
        self.rect.y += self.speed
        if self.rect.y >= H:
            self.rect.y = -150
            self.rect.x = random.randint(0, W)
            k += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
        
score_text = font.render(f'Score: {i}', True, (255, 255, 255))
lost_text = font.render(f'Lost: {k}', True, (255, 255, 255))

player = Player('rocket.png', 325, 450, 50, 50, 6)

enemys = pygame.sprite.Group()
enemys.add(
    Enemy('ufo.png', random.randint(0, W), random.randint(-300, -150), 50, 50, random.randint(1, 2)), 
    Enemy('ufo.png', random.randint(0, W), random.randint(-300, -150), 50, 50, random.randint(1, 2)), 
    Enemy('ufo.png', random.randint(0, W), random.randint(-300, -150), 50, 50, random.randint(1, 2)), 
    Enemy('ufo.png', random.randint(0, W), random.randint(-300, -150), 50, 50, random.randint(1, 2)),
    Enemy('ufo.png', random.randint(0, W), random.randint(-300, -150), 50, 50, random.randint(1, 2))
    )
comets = pygame.sprite.Group()
comets.add(
    Enemy('asteroid.png', random.randint(0, W), random.randint(-300, -150), 50, 50, 1), 
    Enemy('asteroid.png', random.randint(0, W), random.randint(-300, -150), 50, 50, 1),
    )
bullets = pygame.sprite.Group()

rel_time = False
finish = False
game = True
while game:
    score_text = font.render(f'Score: {i}', True, (255, 255, 255))
    lost_text = font.render(f'Lost: {k}', True, (255, 255, 255))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                if num_fire < 5 and not rel_time:
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and not rel_time:
                    rel_time = True
                    start_time = time.time()                  
             
    collides = pygame.sprite.groupcollide(enemys, bullets, True, True)
    collides_2 = pygame.sprite.groupcollide(comets, bullets, False, True)
    for _ in collides:
        enemy = Enemy('ufo.png', random.randint(0, W), random.randint(-300, -150), 50, 50, random.randint(1, 3))
        enemys.add(enemy)
        i += 1
         
    if i >= 10: 
        win = font.render('Winner', True, (255, 215, 0))
        window.blit(win, (200, 200))
        finish = True
    elif k >= 3:
        lose = font.render('Loser', True, (255, 215, 0))
        window.blit(lose, (200, 200))
        finish = True
    
    if not finish:
        window.blit(background_image, (0, 0))
        window.blit(score_text, (20, 10))
        window.blit(lost_text, (20, 60))
        enemys.draw(window)
        comets.draw(window)
        bullets.draw(window)
        player.update()
        player.reset()
        enemys.update()
        comets.update()
        bullets.update()
    
    if rel_time:
        new_time = time.time()
        if new_time - start_time >= 3: 
            num_fire = 0 
            rel_time = False
        else:
            reloading = font.render('Wait, reload...', True, (255, 215, 0))
            window.blit(reloading, (200, 400))
            finish = False
        
    pygame.display.update()
    clock.tick(FPS)