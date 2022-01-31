from asyncio import sleep
from multiprocessing.connection import wait
import arcade
import arcade.gui
import CONSTANTS

from entity.Unit import BigDaddy
from utils.isometric import grid_pos_to_iso
from utils.vector import Vector

"""
NINJALUI: get 10000 of each resource.
\
BIGDADDY: spawn very powerful unit at town center.
\
STEROIDS: training, building, research, foraging, farming, and mining times are
instantaneous. . . for all players, not just you.
\
Additionally, you should have a few commands to influence the AI, force it to launch
an immediate attack, check its state of mind, put your civilisation on autopilot, or
simply exchange the civilisations you and the enemy AI control.
The idea is that you should have commands that enable you to debug and show off
your AI. What commands those are will depend on your AI.
"""
"""
idées : key pour toggle une ligne pour rentrer les cheats code : F10
if un cheat code est rentré : execute cheatcode pour un player en particulier
else : renvoie sur l'écran : "ce cheat code n'est pas implémenté ; liste les
cheat codes available ;
"""


class CheatsInput(arcade.gui.UIInputText):
    STEROIDS = False
    def __init__(self, x, y, text, width, height, text_color, game) : 
        super().__init__(x=x, y=y, text=text, width=width, height=height, text_color=text_color)
        self.cheats_list = ['NINJALUI', 'BIGDADDY', 'STEROIDS', 'REVEAL MAP', 'NO FOG']
        self.game = game
        self.triggered = False 

    def Ninjalui(self):
        self.game.players["player"].add_all(10000)
        self.game.game_view.update_resources_gui()

    def Bigdaddy(self):
        print("Bigdaddy")
        bigdaddz = BigDaddy(grid_pos_to_iso(self.game.players["player"].town_center.grid_position - Vector(1, 1)), "player")
        self.game.game_controller.add_entity_to_game(bigdaddz)

    def Steroids(self):
        print("ON STEROIDS!!!")
        CheatsInput.STEROIDS = not CheatsInput.STEROIDS

    def reset_text(self):
        self.text = "Enter a cheat code"


    def on_enter_pressed(self) :
        print(f"Cheatcode entered : {self.text}")
        if self.text == "NINJALUI":
            self.Ninjalui()
        elif self.text == "BIGDADDY":
            self.Bigdaddy()
        elif self.text == "STEROIDS":
            self.Steroids()
        self.reset_text()