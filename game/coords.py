class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def screen(self, bg_camera_x):
        return self.x - bg_camera_x, self.y
    
    def world(self):
        return self.x, self.y