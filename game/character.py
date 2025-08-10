from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QRect
from .background import Background

class Character:
    def __init__(self, x, background:Background):
        self.char = QPixmap("assets/character.png")
        self.char_right = QPixmap("assets/character_right.png")
        self.char_left = QPixmap("assets/character_left.png")
        self.x = x
        self.ground_y = background.height() - self.char.height()
        self.y = self.ground_y
        self.speed = 5
        self.hp = 100
        self.max_hp = 100
        self.is_dead = False
        self.direction = "right"
        self.last_damage_time = 0
        self.damage_duration = 1
        
        self.is_jumping = False
        self.jump_power = 15
        self.jump_velocity = 0
        self.gravity = 1

    def move_left(self):
        self.direction = "left"
        self.x -= self.speed
    
    def move_right(self):
        self.direction = "right"
        self.x += self.speed

    def start_jump(self):
        if self.is_jumping == False:
            self.is_jumping = True
            self.jump_velocity = self.jump_power

    def update_jump(self):
        if self.is_jumping == True:
            self.y -= self.jump_velocity
            self.jump_velocity -= self.gravity

            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False

    def take_damage(self, damage:int):
        self.hp -= damage
        if self.hp <= 0:
            self.is_dead = True

    def draw(self,painter,bg_offset:int):
        if self.direction == "right":
            painter.drawPixmap(self.x, self.y, self.char_right)
        elif self.direction == "left":
            painter.drawPixmap(self.x, self.y, self.char_left)
        
        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial',10))

        hp_text = f'{self.hp}/{self.max_hp}'
        text_rect = QRect(self.x-5, self.y-20, self.width()+25, 20)

        painter.drawText(text_rect, Qt.AlignCenter, hp_text)

    def get_rect(self,bg_offset:int):
        paint_x = self.x + bg_offset
        return QRect(paint_x, self.y, self.width(), self.height())

    def width(self):
        return self.char.width()
    
    def height(self):
        return self.char.height()