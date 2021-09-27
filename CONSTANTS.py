# Definition des constantes utiles dans tout le projet
# Par exemple, certaines dimensions ou pour realiser des enumerations

# Doc pour les enumerations: https://docs.python.org/fr/3/library/enum.html
from enum import Enum, auto

class Resource(Enum):
    # On utilise les 4 ressources du jeu a de nombreux endroits dans le code
    # Voici donc une enumeration pour harmoniser le tout
    FOOD = auto()
    WOOD = auto()
    GOLD = auto()
    STONE = auto()