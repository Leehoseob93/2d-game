import sys
import random
import time
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPixmap, QTransform, QFont
from PyQt5.QtCore import Qt, QTimer, QRect


class Background:
    def __init__(self):
        self.bg = QPixmap("assets/background.png")
        self.offset = 0

    def max_scroll(self,screen_width):
        return self.bg.width() - screen_width

    def scroll_left(self,speed,screen_width = None):
        self.offset = max(0,self.offset - speed)

    def scroll_right(self,speed,screen_width):
        max_scroll = self.bg.width() - screen_width
        self.offset = min(self.max_scroll(screen_width),self.offset + speed)

    def draw(self, painter, screen_width, screen_height):
        painter.drawPixmap(0,0, self.bg.copy(self.offset, 0, screen_width, screen_height))
    
    def height(self):
        return self.bg.height()
    
    def width(self):
        return self.bg.width()
    

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


class Knife:
    def __init__(self, character:Character):
        self.knife_right = QPixmap('assets/knife_right.png')
        self.knife_left = QPixmap('assets/knife_left.png')
        self.y = character.y + character.height()//3
        self.power = 10
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
    
    def width(self):
        return self.knife_right.width()
    
    def height(self):
        return self.knife_right.height()
    

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


def main():
    app = QApplication(sys.argv)
    game = GameWidget()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

