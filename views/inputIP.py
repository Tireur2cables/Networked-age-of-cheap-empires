from asyncio import sleep
from multiprocessing.connection import wait
import arcade
import arcade.gui
import cheats_vars

from entity.Unit import BigDaddy
from utils.isometric import grid_pos_to_iso
from utils.vector import Vector

from network.pytoc import *

"""
Additionally, you should have a few commands to influence the AI, force it to launch
an immediate attack, check its state of mind, put your civilisation on autopilot, or
simply exchange the civilisations you and the enemy AI control.
The idea is that you should have commands that enable you to debug and show off
your AI. What commands those are will depend on your AI.
"""
class InputIP(arcade.gui.UIInputText):

    def __init__(self, window, x, y, text, font_name, font_size,  width, height) :
        super().__init__(x=x, y=y, text=text, font_name=font_name, font_size=font_size, width=width, height=height)
        self.window = window
        # restetting variables
        # cheats_vars.global_save_suffix = "0" --- This shouldn't be resetted as it is used to load a save in the menu

    def reset_text(self):
        self.text = "Entrez une IP"

    def on_event(self, event):
        super().on_event(event)
        if len(self.text)>= 1 and "\n" == self.text[-1]:

            txt = "JOIN " + self.window.pseudo + " " + self.text
            send(txt, self.window.ecriture_fd)
            self.reset_text()
        # ce qu'il faut faire pour se connecter
