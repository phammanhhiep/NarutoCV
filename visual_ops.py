import pygame
import time
import global_variables as gb
import jutsu_signs


black = (0,0,0)
fake_sequence = []
pygame.init()


# --------------------------------------------------------------------------------------------------------------
# Visual FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()
#
#
# def message_display(text, location, size, win):
#     font_text = pygame.font.Font('freesansbold.ttf', size)
#     textsurf, textrect = text_objects(text, font_text)
#     textrect.center = location
#     win.blit(textsurf, textrect)


# def track(text, location, size):
#     message_display(text, location, size, win)


def prepare(jutsu, win):
    procedure = VisualCue(msg=str(jutsu.get_sequence()), w=gb.display_width, h=(gb.display_height*0.0625),
                          text_color=black, typ=[], seq=fake_sequence, x=0, y=gb.display_height * .75, win=win)

    text_ = "You have selected: " + str(jutsu.icon_name)
    font = pygame.font.Font("freesansbold.ttf", int(9.259259259259259e-05 * gb.display_area * .5))

    textsurf, textRect = text_objects(text_, font)
    textRect.center = (gb.display_width/2, (gb.display_height*.25))
    win.blit(textsurf, textRect)

    pygame.display.update()

    time.sleep(3)
    return procedure


# ------------------------------------------------------------------------------
# GAME LOOP CLASSES
# ------------------------------------------------------------------------------
class Button:

    font = pygame.font.Font("freesansbold.ttf", int(3.7037037037037037e-05 * gb.display_area * .5))
    is_clicked = False
    clickable = False
    class_clickable = False

    def __init__(self, msg, x, y, w, h, color, alpha, win):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r, self.g, self.b = color
        self.alpha = alpha
        self.win = win

    def create_text(self):
        textsurf, textRect = text_objects(self.msg, self.font)
        textRect.center = ((self.x + (self.w/2)), (self.y + (self.h/2)))
        return textsurf, textRect

    def create_button(self):
        # clickable = self.click_status()
        # if self.clickable:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
            self.clickable = True
            Button.class_clickable = True

            button = pygame.Surface((self.w, self.h), pygame.SRCALPHA)  # per-pixel alpha
            button.fill((self.r, self.g, self.b, self.alpha))  # notice the alpha value in the color
            self.win.blit(button, (self.x, self.y))

            if click[0] == 1:
                print('clicked')
                self.is_clicked = True
        else:
            self.clickable = False
            # Button.class_clickable = False
            button = pygame.draw.rect(self.win, (self.r, self.g, self.b), (self.x, self.y, self.w, self.h))

        text, rect = self.create_text()
        self.win.blit(text, rect)

    # else:
    #     button = pygame.Surface((self.w, self.h), pygame.SRCALPHA)  # per-pixel alpha
    #     button.fill((self.r, self.g, self.b, self.alpha))  # notice the alpha value in the color
    #     self.win.blit(button, (self.x, self.y))
    #     text, rect = self.create_text()
    #     self.win.blit(text, rect)








class CharacterIcon:

    p1_x = gb.display_width * .025  # 30 before
    p2_x = gb.display_width * (7/8)
    top_y = gb.display_height / 5
    middle_y = gb.display_height * (2 / 5)
    bottom_y = gb.display_height * (3 / 5)
    folder = 'character_icons/'
    icon_size = (int(gb.display_width * .1), int(gb.display_height * .15))  # 120,120 before

    class_clickable = False
    class_isclicked = False

    char_highlighted = False
    attacked_queue = []
    class_turn = True

    def __init__(self, icon_name, player_num, icon_num, win):
        self.icon_name = icon_name
        self.player_num = player_num
        self.icon_num = icon_num
        self.win = win
        self.clickable = False
        self.health = 100

    def get_x(self):
        if self.player_num == 1:
            x_location = self.p1_x
        elif self.player_num == 2:
            x_location = self.p2_x
        else:
            return "invalid PLAYER number provided to Class Icon get_x method"
        return x_location

    def get_y(self):
        if self.icon_num == 1:
            y_location = self.top_y
        elif self.icon_num == 2:
            y_location = self.middle_y
        elif self.icon_num == 3:
            y_location = self.bottom_y
        else:
            return "invalid ICON number provided to Class Icon get_y method"
        return y_location

    def get_image_from_string(self):
        try:
            path = self.folder + self.icon_name + ".jpg"
            img = pygame.image.load(path)
        except Exception as e:
            try:
                path = self.folder + self.icon_name + ".png"
                img = pygame.image.load(path)
            except Exception as e:
                return f"Couldn't find jpg nor png for icon {self.icon_name}."
        return img

    def resize_image(self):
        img = self.get_image_from_string()
        resized = pygame.transform.scale(img, self.icon_size)
        return resized

    def click_status(self):
        mouse = pygame.mouse.get_pos()
        x, y = self.get_x(), self.get_y()
        size = self.icon_size[0]

        if (x + size) > mouse[0] > x and (y + size) > mouse[1] > y: self.clickable = True
        else: self.clickable = False
        return self.clickable

    def display_image(self):
        if self.health <= 0:
            self.die()

        x, y = self.get_x(), self.get_y()
        img = self.resize_image()

        if Jutsu_Icon.class_isclicked:
            if CharacterIcon.class_turn and self.player_num == 2 or not CharacterIcon.class_turn and self.player_num == 1:
                img = img.convert()
                img.set_alpha(100)

                if self.click_status():
                    print(" Mouse over character")
                    CharacterIcon.char_highlighted = True
                    click = pygame.mouse.get_pressed()
                    if click[0] == 1:
                        print('Character Clicked On')
                        CharacterIcon.attacked_queue = self

        self.win.blit(img, (x, y))
        self.display_bar()



    def die(self):
        input('death' + str(self.icon_name))

    def display_bar(self):
        x, y = self.get_x(), self.get_y() + self.icon_size[1] + (gb.display_height * 0.00625)
        bar_width = int(self.icon_size[0] * (self.health / 100))
        bar = pygame.Surface((bar_width, 10), pygame.SRCALPHA)  # per-pixel alpha
        bar.fill((255, 0, 0, 255))  # notice the alpha value in the color

        msg1 = f"Health:  {self.health}"
        font = pygame.font.Font("freesansbold.ttf", int(1.8518518518518518e-05 * gb.display_area * .5))
        textsurf, textRect = text_objects(msg1, font)
        textRect.center = (x + (self.icon_size[0] / 2), y + (gb.display_height * 0.0225))  # was 18

        self.win.blit(bar, (x, y))
        self.win.blit(textsurf, textRect)







class Jutsu_Icon(CharacterIcon):

    icon_size = (int(gb.display_width * 0.06666666666666667), int(gb.display_height * 0.1))  # was 80,80
    x_offset = gb.display_width // 12
    jutsu_que = []
    folder = 'jutsu_icons/'

    def __init__(self, icon_name, player_num, icon_num, parent_icon, win):
        super().__init__(icon_name, player_num, icon_num, win)
        self.parent_icon = parent_icon

    def get_x(self):
        x_p = self.parent_icon.get_x()
        if self.player_num == 1:
            x_p += (gb.display_width * .025)  # was 30
            x = x_p + (self.x_offset * self.icon_num)
        elif self.player_num == 2:
            x = x_p - (self.x_offset * self.icon_num)  # mirror effect
        else:
            return "invalid player number provided to jutsu_get_x"
        return x

    def get_y(self):
        y_p = self.parent_icon.get_y()
        y = y_p + (gb.display_height * 0.025)
        return y

    def display_image(self):
        x, y = self.get_x(), self.get_y()
        img = self.resize_image()

        if self.click_status():
            Jutsu_Icon.class_clickable = True
            print(f"Mouse is over Icon {self.icon_name}")

            img = img.convert()
            img.set_alpha(100)

            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                Jutsu_Icon.class_isclicked = True

                # queue up jutsu
                Jutsu_Icon.jutsu_que = self
                print('jutsu icon clicked')

        if not Jutsu_Icon.class_clickable:
            click = pygame.mouse.get_pressed()
            if CharacterIcon.char_highlighted:
                # If we click on a character with a jutsu queued up
                if click[0] == 1:
                    Jutsu_Icon.class_isclicked = False
            if not CharacterIcon.char_highlighted:
                # If we click away from everything with a queued character
                if click[0] == 1:
                    print("CLICKED AWAY")
                    Jutsu_Icon.class_isclicked = False
                    Jutsu_Icon.jutsu_que = []

        self.win.blit(img, (x, y))
        self.display_name()

    def display_name(self):
        msg1 = self.icon_name
        msg2 = f"Damage: {self.get_damage()}"
        font = pygame.font.Font("freesansbold.ttf", int(2.2222222222222223e-05 * gb.display_area * .5))
        x, y = (self.get_x() + self.icon_size[0] / 2, self.get_y() + self.icon_size[1] + (gb.display_height * 0.0125))

        textsurf, textRect = text_objects(msg1, font)
        textsurf2, textRect2 = text_objects(msg2, font)
        textRect.center = (x,y)
        textRect2.center = (x, y + (gb.display_height * 0.01875))

        self.win.blit(textsurf, textRect)
        self.win.blit(textsurf2, textRect2)

    def get_damage(self):
        for item in jutsu_signs.chars_signs:
            if list(item.values())[0] == self.parent_icon.icon_name:
                return item[self.icon_name][1]
        else:
            return "Character not found in chars list from damage signs"




# -----------------------------------------------------------------------------------------------
# WEAVING LOOP CLASSES
# -----------------------------------------------------------------------------------------------
class VisualCue:

    box_color = (150, 150, 150)
    box_outline = (200, 200, 200)

    def __init__(self, msg, w, h, text_color, typ, seq, win, x=None, y=None, image_str=None):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r, self.g, self.b = text_color
        self.typ = typ
        self.seq = seq
        self.win = win
        self.image_str = image_str

        if self.typ == 'header':
            self.font = pygame.font.Font("freesansbold.ttf", int(0.00014814814814814815 * gb.display_area * .5))
        elif self.typ == 'prompt':
            self.font = pygame.font.Font("freesansbold.ttf", int(7.407407407407407e-05 * gb.display_area * .5))
        elif self.typ == 'jutsu':
            self.font = pygame.font.Font("freesansbold.ttf", int(5.555555555555556e-05 * gb.display_area * .5))
        else:
            self.font = pygame.font.Font("freesansbold.ttf", int(9.259259259259259e-05 * gb.display_area * .5))

    def get_x(self):
        if self.typ == 'header':
            self.x = gb.display_width // 2 - (self.w // 2)
        elif self.typ == 'prompt':
            self.x = gb.display_width * ((len(self.seq) + 1) / 6) - (gb.display_width * 0.125)  # 150
        elif self.typ == 'jutsu':
            self.x = gb.display_width * (len(self.seq) / 6) - (gb.display_width * 0.083333333333)  # 100
        elif self.typ == 'image':
            self.x = gb.display_width * (len(self.seq) / 6) - (gb.display_width * 0.1)  # 120)
        return self.x

    def get_y(self):
        if self.typ == 'header':
            self.y = (gb.display_height * 0.025)  # 20
        elif self.typ == 'prompt':
            self.y = (gb.display_height * 0.1625)  # 130
        elif self.typ == 'jutsu':
            self.y = (gb.display_height * 0.3)  # 240
        elif self.typ == 'image':
            self.y = (gb.display_height * 0.3625)  # 290
        return self.y

    def text_objects(self):
        textsurface = self.font.render(self.msg, True, (self.r, self.g, self.b))
        return textsurface, textsurface.get_rect()

    def create_text(self):
        if self.x is None:
            self.x = self.get_x()
        if self.y is None:
            self.y = self.get_y()
        textsurf, textRect = self.text_objects()
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
        return textsurf, textRect

    def display_image(self):
        location = (self.get_x(), self.get_y())
        img = pygame.image.load(self.image_str)
        self.win.blit(img, location)

    def create_cue(self):
        if self.x is None:
            self.x = self.get_x()
        if self.y is None:
            self.y = self.get_y()
        button = pygame.draw.rect(self.win, self.box_color, (self.x, self.y, self.w, self.h))
        text, rect = self.create_text()
        self.win.blit(text, rect)
