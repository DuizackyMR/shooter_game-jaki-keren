from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont(None, 36)

img_back = 'galaxy.jpg'
img_player = 'rocket.png'
img_bullet = 'bullet.png' 
img_enemy = 'ufo.png'
img_enemy2 = 'asteroid.png'

window = display.set_mode((700,500))
display.set_caption('Shooter Game')
background = transform.scale(image.load(img_back), (700, 500))

lost = 0
score = 0
max_lost = 3
goal = 10

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):

        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20 ,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update (self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

rocket = Player(img_player, 5, 500 - 100, 80, 100, 10)
ufos = sprite.Group()
for i in range(1, 6):
    ufo = Enemy(img_enemy, randint(80, 700-80), -40, 80, 50, randint(1,5))
    ufos.add(ufo)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_enemy2,randint(30, 700 - 80), -40, 80, 50, randint(1,3))
    asteroids.add(asteroid)



rocket = Player(img_player, 5, 500 - 100, 80, 100, 10)

bullets = sprite.Group()

game = True 
finish = False
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()

    if not finish:
        window.blit(background, (0,0))

        text_lose = font2.render('Missed:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_score = font2.render('Score:' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        

        rocket.update()
        rocket.reset()

        ufos.update()
        ufos.draw(window)

        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score += 1 
            ufo = Enemy(img_enemy, randint(80, 700 -80), -40, 80, 50, randint (1,5))
            ufos.add(ufo)

        if sprite.spritecollide(rocket, ufos, False) or sprite.spritecollide(rocket, asteroids, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win,(200, 200))

        display.update()
    else:
        finish = False
        score = 0
        lost = 0

        for b in bullets:
            b.kill()

        for u in ufos:
            u.kill()

        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1,6):
            ufo = Enemy(img_enemy, randint(80, 700 - 80), -40, 80, 50, randint(1,5))
            ufos.add(ufo)   

        for i in range(1,3):
            asteroid = Enemy(img_enemy, randint(80, 700 - 80), -40, 80, 50, randint(1,5))
            asteroids.add(asteroids)   
    
    clock.tick(60)

