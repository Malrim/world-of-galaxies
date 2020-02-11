import pygame, random

# region CONSTANTS

BG_SCROLLING_SPEED = 3      # rychlost scrollování pozadí hry

PLAYER_HEALTH = 3           # životy hráče
PLAYER_SPEED = 5            # rychlost hráčovi lodě
PLAYER_SHOOT_DELAY = 250    # rychlost střelbi hráče
PLAYER_SCORE_ENEMY = 10     # počet score za zničení nepřátelské lodi
PLAYER_SCORE_METEOR = 5     # počet score za zničení meteoritu
PLAYER_LASER_SPEED = 8      # rychlost hráčova laseru
PLAYER_LASER_DAMAGE = -1    # jak velké bude poškození hráčova laseru

SHIPS_CRASH_DAMAGE = -1     # jak velké bude poškození hráčovi lodě při nárazu

ENEMY_HEALTH = 1            # životy nepřátelské lodě
ENEMY_SPEED = 3             # rychlost nepřátelské lodě
ENEMY_SHOOT_DELAY = 500     # rychlost střelby nepřátel
ENEMY_LASER_SPEED = 8       # rychlost laseru nepřátelské lodě
ENEMY_LASER_DAMAGE = -1     # jak velké bude poškození nepřátelského laseru

METEORITE_SPEED = 3         # rychlost meteoritu

ENEMIES_GEN = 1000          # rychlost generování nepřátelských lodí
METEORITES_GEN = 1500       # rychlost generování meteoritů

EXPLOSION_FRAME_RATE = 50   # rychlost animace exploze

# endregion

# třída pozadí
class Background:

    def __init__(self, scrolling_speed, start_x, start_y, img):
        self.scrolling_speed = scrolling_speed
        self.pos_x = start_x
        self.pos_y = start_y
        self.img = img

    # metoda scrolluje pozadím
    def scrolling(self, height_win):
        if self.pos_y < height_win:
            self.pos_y += self.scrolling_speed
        else:
            self.pos_y = 0

    # metoda vykreslí pozadí
    def draw(self, win):
        win.blit(self.img, (self.pos_x, self.pos_y))
        win.blit(self.img, (self.pos_x, -self.img.get_height() + self.pos_y))

# třída pro komponentu hry (základní třída)
class Component(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y, img, *groups):
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.explosion_sprites = None
        self.explosion_sound = None

    def get_rect(self):
        return self.rect

    def get_x(self):
        return self.rect.x

    def set_x(self, x):
        self.rect.x = x

    def add_x(self, value):
        self.rect.x += value

    def get_y(self):
        return self.rect.y

    def set_y(self, y):
        self.rect.y = y

    def add_y(self, value):
        self.rect.y += value

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_img(self):
        return self.image

    # metoda vytvoří efekt exploze
    def explode(self, components):
        self.explosion = Explosion(
            (self.get_x() + self.image.get_width() / 2, self.get_y() + self.image.get_height() / 2),
            self.explosion_sprites,
            EXPLOSION_FRAME_RATE
        )
        components.add(self.explosion)
        pygame.mixer.Sound.play(self.explosion_sound)

# třída vesmírné lodě
class Ship(Component):

    def __init__(self, health, speed, shoot_delay, start_x, start_y, img,
                 laser_img, explosion_sprites, laser_sound, explosion_sound
                 ):
        super().__init__(start_x, start_y, img)
        self.health = health
        self.speed = speed
        self.shoot_delay = shoot_delay
        self.last_shot = pygame.time.get_ticks()
        self.laser_img = laser_img
        self.explosion_sprites = explosion_sprites
        self.laser_sound = laser_sound
        self.explosion_sound = explosion_sound

    def get_health(self):
        return self.health

    def add_health(self, value):
        self.health += value

# třída laseru
class Laser(Component):

    # parametr "direction" - "1" pro pohyb dolů, "-1" pro pohyb nahoru
    def __init__(self, speed, damage, direction, start_x, start_y, img):
        super().__init__(start_x, start_y, img)
        self.speed = speed
        self.damage = damage
        self.direction = direction

    # pohyb laseru
    def update(self, height_win):
        self.add_y(self.speed * self.direction)

        # pokud je laser mimo obrazovku, tak se zničí
        if self.get_rect().bottom < 0 or self.get_rect().top > height_win:
            self.kill()

    def get_damage(self):
        return self.damage

# třída hráče
class Player(Ship):

    def __init__(self, health, speed, shoot_delay, start_x, start_y, img,
                 laser_img, explosion_sprites, laser_sound, explosion_sound
                 ):
        super().__init__(health, speed, shoot_delay, start_x, start_y, img,
                         laser_img, explosion_sprites, laser_sound, explosion_sound
                         )
        self.score = 0
        self.death = False

    def update(self, width_win, components, player_lasers, enemies, enemies_lasers, meteors):
        # ovládání hráče
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.add_x(self.speed)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.add_x(-self.speed)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.add_y(self.speed)
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.add_y(-self.speed)
        if keys[pygame.K_SPACE]:
            self.shoot(components, player_lasers)

        self.broadcast_rect(enemies)

        # kontrola kolizí s nepřátelskou lodí, s laserama nepřátel a meteoritama
        self.check_collide_with_enemy(enemies)
        self.check_collide_with_meteorite(meteors, components)
        self.check_collide_with_enemy_laser(enemies_lasers)
        self.check_collide_player_laser_with_enemy(player_lasers, enemies)
        self.check_collide_player_laser_with_meteorite(player_lasers, meteors, components)

        # úmrtí hráče
        if self.get_health() <= 0 and not self.death:
            self.explode(components)
            self.death = True
            self.set_x(width_win + 200)

    # metoda pro střelbu. Hráč střílí v daných intervalech
    def shoot(self, components, player_lasers):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_shot > self.shoot_delay:
            self.last_shot = time_now
            x = (self.get_x() + self.image.get_width() // 2) - self.laser_img.get_width() // 2
            y = self.get_y() - self.laser_img.get_height()
            laser = Laser(PLAYER_LASER_SPEED, PLAYER_LASER_DAMAGE, -1, x, y, self.laser_img)
            components.add(laser)
            player_lasers.add(laser)
            pygame.mixer.Sound.play(self.laser_sound)

    # kontrola kolize s nepřátelskou lodí
    def check_collide_with_enemy(self, enemies):
        for crash in pygame.sprite.spritecollide(self, enemies, False):
            crash.add_health(SHIPS_CRASH_DAMAGE)
            self.add_health(SHIPS_CRASH_DAMAGE)

    # kontrola kolize s meteoritem
    def check_collide_with_meteorite(self, meteors, components):
        for crash in pygame.sprite.spritecollide(self, meteors, False):
            crash.destroy(components)
            self.add_health(SHIPS_CRASH_DAMAGE)

    # kontrola kolize s laserem od nepřátelských lodí
    def check_collide_with_enemy_laser(self, enemies_lasers):
        for hit in pygame.sprite.spritecollide(self, enemies_lasers, False):
            self.add_health(hit.get_damage())
            hit.kill()

    # kontrola kolize hráčova laseru s nepřátelskou lodí
    def check_collide_player_laser_with_enemy(self, player_lasers, enemies):
        for player_laser, enemy_ships in pygame.sprite.groupcollide(player_lasers, enemies, False, False).items():
            for enemy in enemy_ships:
                enemy.add_health(player_laser.get_damage())
                self.score += PLAYER_SCORE_ENEMY
                player_laser.kill()

    # kontrola kolize hráčova laseru s meteoritem
    def check_collide_player_laser_with_meteorite(self, player_lasers, meteors, components):
        for player_laser, meteorites in pygame.sprite.groupcollide(player_lasers, meteors, False, False).items():
            for meteor in meteorites:
                meteor.destroy(components)
                self.score += PLAYER_SCORE_METEOR
                player_laser.kill()

    def is_death(self):
        return self.death and not self.explosion.alive()

    def broadcast_rect(self, enemies):
        for enemy in enemies:
            enemy.recieve_player_rect(self.get_rect())

    def get_score(self):
        return self.score

# třída nepřátelské lodi
class Enemy(Ship):

    def __init__(self, health, speed, shoot_delay, start_x, start_y, img,
                 laser_img, explosion_sprites, laser_sound, explosion_sound
                 ):
        super().__init__(health, speed, shoot_delay, start_x, start_y, img,
                         laser_img, explosion_sprites, laser_sound, explosion_sound
                         )

    def update(self, height_win, components, enemies_lasers):
        self.add_y(self.speed)
        self.shoot(components, enemies_lasers)

        # kontrola úmrtí
        if self.get_health() <= 0:
            self.explode(components)
            self.kill()

        # pokud je nepřítel mimo obrazovku, zničí se
        if self.get_rect().top > height_win:
            self.kill()

    # metoda pro střelbu. Nepřítel střílí v daných intervalech
    def shoot(self, components, enemies_lasers):
        if (self.player_rect.x + self.player_rect.width // 2) >= self.get_x() and \
                self.player_rect.x <= (self.get_x() + self.image.get_width() // 2):
            time_now = pygame.time.get_ticks()
            if time_now - self.last_shot > self.shoot_delay:
                self.last_shot = time_now
                x = (self.get_x() + self.image.get_width() // 2) - self.laser_img.get_width() // 2
                y = self.get_y() + self.image.get_height()
                laser = Laser(ENEMY_LASER_SPEED, ENEMY_LASER_DAMAGE, 1, x, y, self.laser_img)
                components.add(laser)
                enemies_lasers.add(laser)
                pygame.mixer.Sound.play(self.laser_sound)

    # metoda získává souřadnice hráče
    def recieve_player_rect(self, rect):
        self.player_rect = rect

# třída meteoritu
class Meteorite(Component):

    def __init__(self, speed, start_x, start_y, img, explosion_sprites, explosion_sound, *groups):
        super().__init__(start_x, start_y, img, *groups)
        self.speed = speed
        self.original_image = img
        self.explosion_sprites = explosion_sprites
        self.explosion_sound = explosion_sound
        self.angle = 0

    def update(self, height_win):
        self.add_y(self.speed)

        self.image = pygame.transform.rotate(self.original_image, self.angle) # rotace obrázku
        self.angle = (self.angle + 1) % 360  # nový úhel

        # pokud je meteorit mimo obrazovku, zničí se
        if self.get_rect().top > height_win:
            self.kill()

    # metoda zničí meteorit
    def destroy(self, components):
        self.explode(components)
        self.kill()

# třída pro generování nepřátelských lodí a meteoritů
class EnemiesAndMeteoritesGenerator:

    def __init__(self, enemy_gen_delay, meteor_gen_delay, explosion_sprites,  explosion_sound):
        self.enemy_gen_delay = enemy_gen_delay
        self.meteor_gen_delay = meteor_gen_delay
        self.explosion_sprites = explosion_sprites
        self.explosion_sound = explosion_sound
        self.last_enemy_gen = pygame.time.get_ticks()
        self.last_meteorite_gen = pygame.time.get_ticks()

    # generování meteoritů
    def generate_meteorite(self, meteor_img, width_win, components, meteors):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_meteorite_gen > self.meteor_gen_delay:
            self.last_meteorite_gen = time_now
            x = random.randrange(width_win - meteor_img.get_width())
            y = -(meteor_img.get_height() + 10)
            meteorite = Meteorite(METEORITE_SPEED, x, y, meteor_img, self.explosion_sprites, self.explosion_sound)
            components.add(meteorite)
            meteors.add(meteorite)

    # generování nepřátelských lodí
    def generate_enemy(self, enemy_img, enemy_laser_img, laser_sound, width_win, components, enemies):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_enemy_gen > self.enemy_gen_delay:
            self.last_enemy_gen = time_now
            x = random.randrange(width_win - enemy_img.get_width())
            y = -(enemy_img.get_height() + 10)
            enemy = Enemy(
                ENEMY_HEALTH,
                ENEMY_SPEED,
                ENEMY_SHOOT_DELAY,
                x,
                y,
                enemy_img,
                enemy_laser_img,
                self.explosion_sprites,
                laser_sound,
                self.explosion_sound
            )
            components.add(enemy)
            enemies.add(enemy)

# třída pro efekt výbuchu
class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, explosion_sprites, frame_rate, *groups):
        super().__init__(*groups)
        self.explosion_sprites = explosion_sprites
        self.image = self.explosion_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_sprites): # pokud bude poslední sprite efektu, celý efekt se zničí
                self.kill()
            else: # jinak pokračuj na další sprite efektu
                center = self.rect.center
                self.image = self.explosion_sprites[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
