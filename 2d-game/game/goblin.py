import random
from PyQt5.QtGui import QPixmap, QTransform, QFont
from PyQt5.QtCore import Qt, QRect
from .background import Background
from .coords import Coordinate

class Goblin:
    def __init__(self, background:Background, char_abs_x:int):
        self.background = background
        self.gob = QPixmap("2d-game/assets/goblin.png")
        
        self.init_coords()
        self.init_status()

        if char_abs_x - self.pos.x > 0:
            self.direction = "right"
        elif char_abs_x - self.pos.x <= 0:
            self.direction = "left"

    def init_coords(self):
        max_x = max(0, self.background.width() - self.gob.width())
        spawn_x = random.randint(0,max_x)
        ground_y = self.background.height() - self.gob.height()
        self.pos = Coordinate(spawn_x, ground_y)
        
    def init_status(self):
        self.speed = 1
        self.power = 25
        self.hp = 50
        self.max_hp = 50
        self.is_dead = False

    def move(self, char_abs_x:int):
        if char_abs_x - self.pos.x > 0:
            self.direction = "right"
        elif char_abs_x - self.pos.x <= 0:
            self.direction = "left"

        if self.direction == "right":
            self.pos.x += self.speed
        elif self.direction == "left":
            self.pos.x -= self.speed
    
    def draw(self,painter,bg_offset):
        scr_x, scr_y = self.pos.screen(bg_offset)
        pixmap = self.gob

        if self.direction == "right":
            painter.drawPixmap(scr_x, scr_y, pixmap)
        elif self.direction == "left":
            pixmap = pixmap.transformed(QTransform().scale(-1, 1))
            painter.drawPixmap(scr_x, scr_y, pixmap)

        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial',10))

        hp_text = f'{self.hp}/{self.max_hp}'
        text_rect = QRect(scr_x, scr_y-15, self.width(), 15)

        painter.drawText(text_rect, Qt.AlignCenter, hp_text)

    def take_damage(self, damage:int):
        self.hp -= damage
        if self.hp <= 0:
            self.is_dead = True
        
    def get_screen_rect(self,bg_offset:int):
        scr_x, scr_y = self.pos.screen(bg_offset)
        return QRect(scr_x, scr_y, self.width(), self.height())
    
    def get_world_rect(self):
        return QRect(self.pos.x, self.pos.y, self.width(), self.height())

    def width(self):
        return self.gob.width()
    
    def height(self):
        return self.gob.height()