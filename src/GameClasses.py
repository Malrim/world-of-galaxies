import pygame, random

class Background:

    def __init__(self, scrolling_speed, start_x, start_y, img):
        self.scrolling_speed = scrolling_speed
        self.pos_x = start_x
        self.pos_y = start_y
        self.img = img

    def scrolling(self, height_win):
        if self.pos_y < height_win:
            self.pos_y += self.scrolling_speed
        else:
            self.pos_y = 0

    def draw(self, win):
        win.blit(self.img, (self.pos_x, self.pos_y))
        win.blit(self.img, (self.pos_x, -self.img.get_height() + self.pos_y))

class Component(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y, img, *groups):
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_img(self):
        return self.image

class Ship(Component):

    def __init__(self, health, speed, shoot_delay, start_x, start_y, img, laser_img):
        super().__init__(start_x, start_y, img)
        self.health = health
        self.speed = speed
        self.shoot_delay = shoot_delay
        self.last_shot = pygame.time.get_ticks()
        self.laser_img = laser_img

    def get_health(self):
        return self.health

class Laser(Component):

    def __init__(self, speed, direction, start_x, start_y, img):
        super().__init__(start_x, start_y, img)
        self.speed = speed
        self.direction = direction

    def update(self, height_win):
        self.rect.y += (self.speed * self.direction)

        # if the laser is off-screen
        if self.rect.bottom < 0 or self.rect.top > height_win:
            self.kill()

class Player(Ship):

    def __init__(self, health, number_lasers, speed, shoot_delay, start_x, start_y, img, laser_img):
        super().__init__(health, speed, shoot_delay, start_x, start_y, img, laser_img)
        self.number_lasers = number_lasers
        self.max_number_lasers = number_lasers

    def update(self, components, player_lasers, enemies, enemies_lasers):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_SPACE]:
            self.shoot(components, player_lasers)

        self.broadcast_rect(enemies)
        self.collide_with_enemy_laser(enemies_lasers)

    def shoot(self, components, player_lasers):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_shot > self.shoot_delay:
            self.last_shot = time_now
            x = (self.rect.x + self.image.get_width() // 2) - self.laser_img.get_width() // 2
            y = self.rect.y - self.laser_img.get_height()
            laser = Laser(8, -1, x, y, self.laser_img)
            components.add(laser)
            player_lasers.add(laser)

    def collide_with_enemy_laser(self, enemies_lasers):
        if pygame.sprite.spritecollide(self, enemies_lasers, True):
            print("hit!")

    def broadcast_rect(self, enemies):
        for enemy in enemies:
            enemy.recieve_player_rect(self.rect)

class Enemy(Ship):

    def __init__(self, health, speed, shoot_delay, start_x, start_y, img, laser_img):
        super().__init__(health, speed, shoot_delay, start_x, start_y, img, laser_img)

    def update(self, height_win, components, enemies_lasers):
        self.rect.y += self.speed
        self.shoot(components, enemies_lasers)

        # if the enemy is off-screen
        if self.rect.top > height_win:
            self.kill()

    def shoot(self, components, enemies_lasers):
        if (self.player_rect.x + self.player_rect.width // 2) >= self.rect.x and self.player_rect.x <= (self.rect.x + self.image.get_width() // 2):
            time_now = pygame.time.get_ticks()
            if time_now - self.last_shot > self.shoot_delay:
                self.last_shot = time_now
                x = (self.rect.x + self.image.get_width() // 2) - self.laser_img.get_width() // 2
                y = self.rect.y + self.image.get_height()
                laser = Laser(8, 1, x, y, self.laser_img)
                components.add(laser)
                enemies_lasers.add(laser)

    def recieve_player_rect(self, rect):
        self.player_rect = rect

class EnemiesAndAsteroidsGenerator:

    def __init__(self, gen_delay):
        self.gen_delay = gen_delay
        self.last_object = pygame.time.get_ticks()

    def generate(self, enemy_img, enemy_laser_img, width_win, components, enemies):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_object > self.gen_delay:
            self.last_object = time_now
            x = random.randrange(width_win - enemy_img.get_width())
            y = -(enemy_img.get_height() + 10)
            enemy = Enemy(100, 3, 500, x, y, enemy_img, enemy_laser_img)
            components.add(enemy)
            enemies.add(enemy)


#region UI classes
#endregion
