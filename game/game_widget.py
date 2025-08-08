from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QPixmap
from game.character import Character
from game.background import Background
from game.controller import CharacterManager

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('2D 횡스크롤 게임')
        self.setFixedSize(800,480)

        self.background = Background()
        self.character = Character(100, self.background)
        self.controller = CharacterManager(self.character)

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

    def keyPressEvent(self, event):
        self.controller.key_press(event.key())
        if event.key() == Qt.Key_Space:
            self.character.start_jump()

    def keyReleaseEvent(self, event):
        self.controller.key_release(event.key())

    def game_loop(self):
        speed = self.character.speed
        max_scroll = self.background.max_scroll(self.width())

        if self.controller.move_right:
            if self.character.x < self.width() // 2:
                self.character.move_right()
            elif self.background.offset < max_scroll:
                self.background.scroll_right(speed,self.width())
            else:
                if self.character.x < self.width() - self.character.width():
                    self.character.move_right()

        if self.controller.move_left:
            if self.character.x > self.width() // 2:
                self.character.move_left()
            elif self.background.offset > 0:
                self.background.scroll_left(speed,self.width())
            else:
                if self.character.x > 0:
                    self.character.move_left()

        self.character.update_jump()

        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        self.background.draw(painter, self.width(), self.height())
        self.character.draw(painter)