from .character import Character
from PyQt5.QtGui import QPixmap
from .coords import Coordinate

class Knife:
    def __init__(self, character:Character):
        self.character = character
        self.knife = QPixmap('2d-game/assets/knife.png')
        self.y = character.pos.y + character.height()//3
        self.power = 10
        self.direction = character.direction
        self.angle = 0
        self.rotation_speed = 25

        if self.direction == "right":
            self.x = character.pos.x + character.width()//2
            self.k_speed = 15
            self.rotation_speed = 50
        elif self.direction == "left":
            self.x = character.pos.x - character.width()//2
            self.k_speed = -15
            self.rotation_speed = -50

        self.pos = Coordinate(self.x, self.y)

    def move(self):
        self.pos.x += self.k_speed
        self.angle += self.rotation_speed

    def draw(self,painter,bg_offset:int):
        scr_x, scr_y = self.pos.screen(bg_offset)
        if self.direction == "right":
            pixmap = self.knife
        elif self.direction == "left":
            pixmap = self.knife

        center_x = pixmap.width()//2
        center_y = pixmap.height()//2

        painter.save()
        painter.translate(scr_x + center_x, scr_y + center_y)
        painter.rotate(self.angle)
        painter.drawPixmap(-center_x, -center_y, pixmap)
        painter.restore()
    
    def width(self):
        return self.knife.width()
    
    def height(self):
        return self.knife.height()