from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Character:
    def __init__(self, x, background):
        self.char = QPixmap("character.png")
        self.x = x
        self.ground_y = background.height() - self.char.height()
        self.y = self.ground_y
        self.speed = 5
        
        self.is_jumping = False
        self.jump_power = 15
        self.jump_velocity = 0
        self.gravity = 1

    def move_left(self):
        self.x -= self.speed
    
    def move_right(self):
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


    def draw(self,painter):
        painter.drawPixmap(self.x, self.y, self.char)

    def width(self):
        return self.char.width()
    
    def height(self):
        return self.char.height()
    
class CharacterManager:
    def __init__(self, character:Character):
        self.character = character
        self.move_left = False
        self.move_right = False

    def key_press(self,key):
        if key == Qt.Key_Left:
            self.move_left = True
        elif key == Qt.Key_Right:
            self.move_right = True

    def key_release(self,key):
        if key == Qt.Key_Left:
            self.move_left = False
        if key == Qt.Key_Right:
            self.move_right = False