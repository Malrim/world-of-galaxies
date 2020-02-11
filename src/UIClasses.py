import pygame

# region CONSTANTS

BLACK_COLOR = (0, 0, 0)

# endregion

class UIComponent:

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def draw(self, win):
        pass

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

class UIText(UIComponent):

    def __init__(self, text, font, pos_x, pos_y, color=(255, 255, 255)):
        super().__init__(pos_x, pos_y)
        self.font = font
        self.text = self.font.render(text, True, color)
        self.color = color

    def update_text(self, text, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = self.font.render(text, True, self.color)

    def draw(self, win):
        win.blit(self.text, (self.pos_x, self.pos_y))

class UIImage(UIComponent):

    def __init__(self, img, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.img = img

    def draw(self, win):
        win.blit(self.img, (self.pos_x, self.pos_y))

class UIButton(UIComponent):

    def __init__(self, text, font, img_inactive, img_hover, pos_x, pos_y, clicked=None):
        super().__init__(pos_x, pos_y)
        size_text = font.size(text)
        txt_pos_x = pos_x + (img_inactive.get_width() / 2) - (size_text[0] / 2)
        txt_pos_y = pos_y + (img_inactive.get_height() / 2) - (size_text[1] / 2)
        self.ui_text = UIText(text, font, txt_pos_x, txt_pos_y)
        self.img = img_inactive
        self.img_inactive = img_inactive
        self.img_hover = img_hover
        self.active = True
        self.clicked = clicked

        self.click = pygame.mouse.get_pressed()
        self.last_click = self.click

    def update(self):
        if not self.active:
            return

        mouse = pygame.mouse.get_pos()
        self.last_click = self.click
        self.click = pygame.mouse.get_pressed()
        if self.pos_x + self.img.get_width() > mouse[0] > self.pos_x and \
                self.pos_y + self.img.get_height() > mouse[1] > self.pos_y:
            self.img = self.img_hover
            if (self.click[0] == 1 and self.last_click[0] == 0) and self.clicked is not None:
                self.clicked()
        else:
            self.img = self.img_inactive

    def draw(self, win):
        if not self.active:
            return

        win.blit(self.img, (self.pos_x, self.pos_y))
        self.ui_text.draw(win)

    def set_active(self, active):
        self.active = active

class PlayerHUD(UIComponent):

    def __init__(self, number_lives, img_health, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.number_lives = number_lives
        self.img_health = img_health
        self.ui_images = []
        for i in range(0, number_lives):
            if i == 0:
                self.ui_images.append(UIImage(img_health, self.pos_x, self.pos_y))
            else:
                self.ui_images.append(UIImage(img_health,
                                              self.pos_x + self.img_health.get_width() * i + 10 * i,
                                              self.pos_y)
                                      )

    def update_lives(self, lives):
        del_lives = self.number_lives - lives
        if del_lives <= len(self.ui_images) - 1:
            for _ in range(0, del_lives):
                self.ui_images.pop(-1)
                self.number_lives -= 1
        else:
            self.ui_images.clear()

    def draw(self, win):
        for ui_image in self.ui_images:
            ui_image.draw(win)
