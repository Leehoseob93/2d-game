from PyQt5.QtCore import Qt

class CharacterManager:
    def __init__(self, character):
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