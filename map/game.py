import arcade 
import sys

from arcade.key import A
from .world import World
from .settings import TILE_SIZE

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width; self.height = self.screen.get_size()

        self.World = World(10, 10, self.width, self.height)
    
    def run(self):
        self.playing = True
        while self.playing :
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def draw(self):
       pass
