import time
from PyQt5.QtCore import QTimer, QRect
from PyQt5.QtCore import QRect
from .background import Background
from .goblin import Goblin
from .character import Character
from .background import Background

class GoblinManager:
    def __init__(self, background:Background, character:Character):
        self.background = background
        self.character = character
        
        self.goblins = []
        
        self.init_timer()

    def init_timer(self):
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_goblin)
        self.spawn_timer.start(5000)
        self.spawn_goblin()

    def spawn_goblin(self):
        char_abs_x = self.character.x + self.background.offset
        new_goblin = Goblin(self.background, char_abs_x)
        self.goblins.append(new_goblin)

    def intersects_knife(self, knives):
        remove_knives = []

        for knife in knives:
            if knife in remove_knives:
                continue
            
            knife_rect = QRect(knife.x, knife.y, knife.width(), knife.height())

            for goblin in self.goblins:
                goblin_rect = goblin.get_screen_rect(self.background.offset)

                if knife_rect.intersects(goblin_rect):
                    goblin.take_damage(knife.power)
                    remove_knives.append(knife)
                    break

        self.goblins = [g for g in self.goblins if g.is_dead == False]
        return [k for k in knives if k not in remove_knives]

    def intersects_char(self):
        character_rect = self.character.get_rect(self.background.offset)

        for goblin in self.goblins:
            goblin_rect = goblin.get_rect()
            if character_rect.intersects(goblin_rect):
                current_time = time.time()
                if current_time - self.character.last_damage_time > self.character.damage_duration:
                    self.character.take_damage(goblin.power)
                    self.character.last_damage_time = current_time
                    break

    