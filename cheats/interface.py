import arcade
import arcade.gui

class Cheats(arcade.View):
    def __init__(self):
        super().__init__
    
    def on_draw(self):
        arcade.start_render()


    def on_key_press(self, key: int, modifiers: int): 
        #modifiers = shift/ctrl/alt...
        """Called whenever a key is pressed. """
        if key == arcade.key.F10:
            # User hits F10 : 
            """
            toggle ligne
            """
            
