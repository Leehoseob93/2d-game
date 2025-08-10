import random
from PyQt5.QtGui import QPixmap, QTransform, QFont
from PyQt5.QtCore import Qt, QRect
from .background import Background

class Goblin:
    def __init__(self, background:Background, char_abs_x:int):
        self.gob = QPixmap("assets/goblin.png")
        self.x = random.randint(0,background.width())
        self.y = background.height() - self.gob.height()
        self.speed = 1
        self.power = 25
        self.hp = 50
        self.max_hp = 50
        self.is_dead = False

        if char_abs_x - self.x > 0:
            self.direction = "right"
        elif char_abs_x - self.x <= 0:
            self.direction = "left"

    def move(self, char_abs_x:int):
        
        if char_abs_x - self.x > 0:
            self.direction = "right"
        elif char_abs_x - self.x <= 0:
            self.direction = "left"

        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
    
    def draw(self,painter,bg_offset):
        paint_x = self.x - bg_offset
        pixmap = self.gob

        if self.direction == "right":
            painter.drawPixmap(paint_x, self.y, pixmap)
        elif self.direction == "left":
            pixmap = pixmap.transformed(QTransform().scale(-1, 1))
            painter.drawPixmap(paint_x, self.y, pixmap)

        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial',10))

        hp_text = f'{self.hp}/{self.max_hp}'
        text_rect = QRect(paint_x, self.y-15, self.width(), 15)

        painter.drawText(text_rect, Qt.AlignCenter, hp_text)

    def take_damage(self, damage:int):
        self.hp -= damage
        if self.hp <= 0:
            self.is_dead = True
        
    def get_screen_rect(self,bg_offset:int):
        paint_x = self.x - bg_offset
        return QRect(paint_x, self.y, self.width(), self.height())
    
    def get_rect(self):
        return QRect(self.x, self.y, self.width(), self.height())

    def width(self):
        return self.gob.width()
    
    def height(self):
        return self.gob.height()