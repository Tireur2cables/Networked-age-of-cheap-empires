from CONSTANTS import Resource as Res

class Player:
    def __init__(self, IA: bool=True, qtyFood: int=200, qtyWood: int=200, qtyGold: int=100, qtyStone: int=200) -> None:
        self.IA = IA
        self.resource = {Res.FOOD : qtyFood, Res.WOOD : qtyWood, Res.STONE : qtyStone, Res.GOLD : qtyGold}#utilisation de l'enumeration Resource

