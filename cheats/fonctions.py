from player import Player

"""
NINJALUI: get 10000 of each resource.
\
BIGDADDY: spawn very powerful unit at town center.
\
STEROIDS: training, building, research, foraging, farming, and mining times are
instantaneous. . . for all players, not just you.
\
REVEAL MAP: Reveal the entire map, exactly as though you had explored it,
which means that enemy units are not revealed, while trees, and stone and gold
mines are. Enemy buildings are not revealed. Issuing the command again toggles
effect.
\
NO FOG: Remove the fog of war. Any explored part of the is therefore fully
visible as though under the line of sight of your units. Issuing the command again
toggles effect.
\
Additionally, you should have a few commands to influence the AI, force it to launch
an immediate attack, check its state of mind, put your civilisation on autopilot, or
simply exchange the civilisations you and the enemy AI control.
The idea is that you should have commands that enable you to debug and show off
your AI. What commands those are will depend on your AI.
"""
"""
idées : bouton pour toggle une ligne pour rentrer les cheats code : ²
if un cheat code est rentré : execute cheatcode pour un player en particulier
else : renvoie sur l'écran : "ce cheat code n'est pas implémenté ; liste les 
cheat codes available ; 
"""
def Ninjalui(player : Player, ):
    Player.add_all(player, 10000)

def Bigdaddy():
    pass
def Steroids():
    pass
def RevealMap():
    pass
def NoFog():
    pass
