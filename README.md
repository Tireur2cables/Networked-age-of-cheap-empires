# Age Of Cheap Empires

## Prérequis pour lancer le jeu

- Python 3 (version 3.8 minimum - notamment utilisation de ```math.dist()``` apparu avec la version 3.8 )
- ```pip3 install arcade```
- ```pip3 install pathfinding```
- ```pip3 install noise``` requiert Microsoft Tools
- ```pip3 install numpy```

## Comment lancer le jeu

- ```python3 game.py ```

## Description

Ceci est une implémentation en Python du jeu Age of Empires, réalisée à l'occasion du cours Projet de Programmation durant premier semestre de la 3ème année en filière STI à l'INSA CVL.

Nous avons choisis le moteur graphique `The Arcade Library` pour réaliser la partie affichage graphique de notre jeu. (expliquer pourquoi)

Vous pouvez retrouver tous les détails concernant l'architecture de notre jeu dans le fichier `ARCHITECTURE.md`.

## Difficultés rencontrées

Voici les difficultés que nous avons rencontrées :

## Sources POO python

- https://www.pierre-giraud.com/python-apprendre-programmer-cours/introduction-oriente-objet/
- https://learnxinyminutes.com/docs/python/

## La Doc de Arcade Library

- API officielle de The Arcade Library : https://api.arcade.academy/en/latest/index.html
- Pour apprendre The Arcade Library en même temps que Python (avec notamment une section sur l'orienté objet) : https://learn.arcade.academy/en/latest/index.html


## Convention proposées
Ces conventions sont calquées sur PEP 8 :
- Noms de module ( = nom de fichiers) : Zone_Buildable_TownCenter.py avec utilisation de sous-dossiers ? (PEP 8 : exemple_de_nom (le nom doit être court))
- Noms de variables, fonctions & methode : exemple_de_nom
- Noms de classe : ExempleDeNom
- Nom d'exceptions : ExempleDeNom (Toujours finir le nom par "Error" : ImportError)
- Constantes : EXEMPLE_DE_NOM


## Listes des demandes du prof :
(rien de précisé = obligatoire)
(c = conseillé)
(f = facultatif)
(d = proposé mais plutôt déconseillé, "casse-gueule")

1) Python 3 - Done
2) Framework GUI (Pygame, ...) - Done
3) Graphical representation of the map
4) Save & Load
5) (c) thème à peu près équivalent à AoE (antique)
6) Human vs IA
7) (c) RTS
8) (d) Variable Speed
9) (c) génération de map procédural
10) (f) fog of war
11) (d) Replay games
12) (f) + de 2 joueurs (+ de 2 IA)
13) (c) IA vs IA
14) (f) Différentes civilisations
15) (c) Ages
16) Ressources de départs modifiables
17) Cheats code

## Brainstorming
Age of Empires
- Graphismes

- Affichage
  - GUI (interface utilisateur)
  - Input (* lié aux mécanismes)

- Sons

- Mécanisme de jeu
  - Commandes (* lié au GUI)
    - Joueur ou IA
  - Tech tree
  - Map (static)
  - Objets sur la map
    - Constructions (Nature & Habitations)
    - Animaux
    - Personnages joués.
