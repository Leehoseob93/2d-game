from game.character import Character
from PyQt5.QtGui import QPixmap

class Knife:
    def __init__(self, character:Character):
        self.knife_right = QPixmap('assets/knife_right.png')
        self.knife_left = QPixmap('assets/knife_left.png')
        self.y = character.y + character.height()//3
        self.direction = character.direction
        self.angle = 0
        self.rotation_speed = 25

        if self.direction == "right":
            self.x = character.x + character.width()//2
            self.k_speed = 15
            self.rotation_speed = 50
        elif self.direction == "left":
            self.x = character.x - character.width()//2
            self.k_speed = -15
            self.rotattion_speed = -50

    def move(self):
        self.x += self.k_speed
        self.angle += self.rotation_speed

    def draw(self,painter):
        if self.direction == "right":
            pixmap = self.knife_right
        elif self.direction == "left":
            pixmap = self.knife_left

        center_x = pixmap.width()//2
        center_y = pixmap.height()//2

        painter.save()
        painter.translate(self.x + center_x, self.y + center_y)
        painter.rotate(self.angle)
        painter.drawPixmap(-center_x, -center_y, pixmap)
        painter.restore()