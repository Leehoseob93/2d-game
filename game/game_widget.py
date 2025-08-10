import time
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QFont
from .character import Character
from .background import Background
from .controller import CharacterManager
from .knife import Knife
from .goblin import Goblin

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

        self.goblins = []
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_goblin)
        self.spawn_timer.start(5000)
        self.spawn_goblin()

        self.knives = []

    def spawn_goblin(self):
        char_abs_x = self.character.x + self.background.offset
        new_goblin = Goblin(self.background, char_abs_x)
        self.goblins.append(new_goblin)

    def keyPressEvent(self, event):
        self.controller.key_press(event.key())
        if event.key() == Qt.Key_Space:
            self.character.start_jump()

        if event.key() == Qt.Key_A:
            new_knife = Knife(self.character)
            self.knives.append(new_knife)

    def keyReleaseEvent(self, event):
        self.controller.key_release(event.key())

    def check_collision(self):
        remove_knives = []

        for knife in self.knives:
            if knife in remove_knives:
                continue

            knife_rect = QRect(knife.x, knife.y, knife.width(), knife.height())

            for goblin in self.goblins:
                goblin_rect = goblin.get_screen_rect(self.background.offset)

                if knife_rect.intersects(goblin_rect):
                    goblin.take_damage(knife.power)
                    remove_knives.append(knife)
                    break

        character_rect = self.character.get_rect(self.background.offset)
        
        for goblin in self.goblins:
            goblin_rect = goblin.get_rect()
            if character_rect.intersects(goblin_rect):
                current_time = time.time()
                if current_time - self.character.last_damage_time > self.character.damage_duration:
                    self.character.take_damage(goblin.power)
                    self.character.last_damage_time = current_time
                    break
        

        self.goblins = [g for g in self.goblins if g.is_dead == False]
        self.knives = [k for k in self.knives if k not in remove_knives]


    def game_loop(self):
        if self.character.is_dead == False:
            speed = self.character.speed
            max_scroll = self.background.max_scroll(self.width())

            if self.controller.move_right:
                self.character.direction = "right"
                if self.character.x < self.width() // 2:
                    self.character.move_right()
                elif self.background.offset < max_scroll:
                    self.background.scroll_right(speed,self.width())
                else:
                    if self.character.x < self.width() - self.character.width():
                        self.character.move_right()

            if self.controller.move_left:
                self.character.direction = "left"
                if self.character.x > self.width() // 2:
                    self.character.move_left()
                elif self.background.offset > 0:
                    self.background.scroll_left(speed)
                else:
                    if self.character.x > 0:
                        self.character.move_left()

            self.character.update_jump()

            for knife in self.knives:
                knife.move()

            for goblin in self.goblins:
                char_abs_x = self.character.x + self.background.offset
                goblin.move(char_abs_x)

            self.check_collision()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.character.is_dead == False:
            self.background.draw(painter, self.width(), self.height())
            self.character.draw(painter,self.background.offset)

            for knife in self.knives:
                knife.draw(painter)

            for goblin in self.goblins:
                goblin.draw(painter, self.background.offset)

        else:
            painter.setBrush(Qt.black)
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.rect())

            painter.setPen(Qt.white)
            painter.setFont(QFont('Arial', 40, QFont.Bold))

            painter.drawText(self.rect(), Qt.AlignCenter, "GAME OVER")