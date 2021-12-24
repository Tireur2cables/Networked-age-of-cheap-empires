import arcade
import arcade.gui


#Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"


#class Cheats(arcade.View)???????
# def __init__(self):
#         super().__init__
# def on_draw(self):
#         arcade.start_render()
n = 'NINJALUI'; b = 'BIGDADDY'; s = 'STEROIDS'; r_m = 'REVEAL MAP'; n_f = 'NO FOG'
cheats_list = [n, b, s, r_m, n_f, n.lower(), b.lower(), s.lower(), r_m.lower(), n_f.lower()]
cheat_list_display = ['NINJALUI', 'BIGDADDY', 'STEROIDS', 'REVEAL MAP', 'NO FOG', 'ninjalui', 'bigdaddy', 'steroids', 'reveal map', 'no fog']
print(cheats_list)

def on_key_press(self, key: int, modifiers: int): 
        #modifiers = shift/ctrl/alt...
        """Called whenever a key is pressed. """
        if key == arcade.key.F10:
            # User hits F10 : 
            """
            toggle ligne
            """
            arcade.draw_text(f"Enter a cheatcode among {cheat_list_display}", 1, SCREEN_HEIGHT-1)  #marche pas, relou
    
