from PyQt5.QtGui import QPixmap

class Background:
    def __init__(self):
        self.bg = QPixmap("background.png")
        self.offset = 0

    def max_scroll(self,screen_width):
        return self.bg.width() - screen_width

    def scroll_left(self,speed,screen_width):
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