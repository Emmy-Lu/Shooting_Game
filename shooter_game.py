from pygame import *
from random import randint
from time import time as timer

# Initialize font
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

# Initialize background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Image paths
img_back = "galaxy.jpg"   # Game background
img_bullet = "bullet.png" # Bullet
img_hero = "rocket.png"   # Hero
img_enemy = "ufo.png"     # Enemy
img_ast = "asteroid.png"

# Game variables
score = 0     # Ships destroyed
goal = 10     # Ships to shoot down to win
lost = 0      # Ships missed
max_lost = 3  # Lose if you miss this many
life = 3

num_fire = 0
rel_time = False


# Parent class for other sprites
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Main player class
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# Enemy sprite class
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

# Bullet sprite class
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Create game window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Create player and enemies
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteriods = sprite.Group()
for i in range(1, 3):
    asteriod = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteriods.add(asteriod)

bullets = sprite.Group()

# Main game loop
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:   
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        asteriods.draw(window)
        bullets.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...", 1, (150, 0, 0))
                window.blit(reload, (250, 460))
            else:
                num_fire = 0
                rel_time = False

        bullet_amount = font2.render(str(num_fire), 1, (150, 0,0))
        window.blit(bullet_amount, (30, 460))
        

        # Check collision between bullet and enemies
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        collides_with_asteroid = sprite.groupcollide(asteriods, bullets, True, True)
        for c in collides_with_asteroid:
            score += 1
            asteriod = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteriods.add(asteriod)

        # Check for player losing conditions
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteriods , False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteriods, True)

        # Check for player winning condition
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        # Display score and missed ships
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        life_color = (0, 150, 0) if life == 3 else (150, 150, 0) if life == 2 else (150, 0, 0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        bullets.empty()
        monsters.empty()
        asteriods.empty()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, 5):
            asteriod = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
            asteriods.add(asteriod)

    time.delay(50)
