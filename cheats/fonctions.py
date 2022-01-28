from player import Player
import arcade
import arcade.gui
"""
NINJALUI: get 10000 of each resource.
\
BIGDADDY: spawn very powerful unit at town center.
\
STEROIDS: training, building, research, foraging, farming, and mining times are
instantaneous. . . for all players, not just you.
\

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
    def __init__(self, x, y, text, width, height, text_color, player : Player) :
        super().__init__(x=x, y=y, text=text, width=width, height=height, text_color=text_color)
        self.cheats_list = ['NINJALUI', 'BIGDADDY', 'STEROIDS', 'REVEAL MAP', 'NO FOG']
        self.player = player

    def Ninjalui(self):
        self.player.add_all(10000)
    def Bigdaddy(self):
        print("debug big daddz")
    def Steroids(self):
        print("debug steroidz")

    def reset_text(self):
        self.text = "Enter a cheatcode among NINJALUI, BIGDADDY, STEROIDS, REVEAL MAP, NO FOG"
        
    def on_event(self, event) :
        super().on_event(event)
        if self._active and isinstance(event, arcade.gui.events.UITextEvent):
            if self.text == "NINJALUI":
                self.Ninjalui()
            elif self.text == "BIGDADDY":
                self.Bigdaddy()
            elif self.text == "STEROIDS":
                self.Steroids()
    