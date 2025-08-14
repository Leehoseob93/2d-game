from PyQt5.QtGui import QPixmap, QFont, QTransform
from PyQt5.QtCore import Qt, QRect
from .background import Background
from .coords import Coordinate

class Character:
    def __init__(self, x, background:Background):
        self.char = QPixmap("2d-game/assets/character.png")
        self.background = background
        self.pos = Coordinate(x, self.ground_y())

        self.init_status()
        self.init_jump()

    def init_status(self):
        self.speed = 5
        self.hp = 100
        self.max_hp = 100
        self.is_dead = False
        self.direction = "right"
        self.last_damage_time = 0
        self.damage_duration = 1

    def init_jump(self):
        self.is_jumping = False
        self.jump_power = 15
        self.jump_velocity = 0
        self.gravity = 1

    def ground_y(self):
        return self.background.height() - self.char.height()

    def move_left(self):
        self.direction = "left"
        self.pos.x -= self.speed
    
    def move_right(self):
        self.direction = "right"
        self.pos.x += self.speed

    def start_jump(self):
        if self.is_jumping == False:
            self.is_jumping = True
            self.jump_velocity = self.jump_power

    def update_jump(self):
        if self.is_jumping == True:
            self.pos.y -= self.jump_velocity
            self.jump_velocity -= self.gravity
            ground_y = self.ground_y()
            if self.pos.y >= ground_y:
                self.pos.y = ground_y
                self.is_jumping = False

    def take_damage(self, damage:int):
        self.hp -= damage
        if self.hp <= 0:
            self.is_dead = True

    def draw(self,painter, bg_offset:int):
        pixmap_r = self.char
        pixmap_l = self.char.transformed(QTransform().scale(-1, 1))
        scr_x, scr_y = self.pos.screen(bg_offset)
        if self.direction == "right":
            painter.drawPixmap(scr_x, scr_y, pixmap_r)
        elif self.direction == "left":
            painter.drawPixmap(scr_x, scr_y, pixmap_l)
        
        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial',10))

        hp_text = f'{self.hp}/{self.max_hp}'
        text_rect = QRect(scr_x-5, scr_y-20, self.width()+25, 20)

        painter.drawText(text_rect, Qt.AlignCenter, hp_text)

    def get_rect(self, bg_offset):
        scr_x, scr_y = self.pos.screen(bg_offset)
        return QRect(scr_x, scr_y, self.width(), self.height())

    def width(self):
        return self.char.width()
    
    def height(self):
        return self.char.height()