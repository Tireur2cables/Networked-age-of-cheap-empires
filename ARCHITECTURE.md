# Description de l'architecture du jeu

## Commentaire général

Nous nous sommes basés sur une architecture Modèle - Vue - Contrôleur, que nous avons adapté afin d'avoir une souplesse et lisibilité accrue.  
Nous avons utilisé une programmation orientée objet afin d'avoir un code réutilisable et évolutif à souhait.  
Nous avons séparés les fichiers python dans une arborescence décrivant les spécialisations des classes.  

## Structure des fichiers

### Dossier racine

Vous lisez actuellement le fichier ```ARCHITECTURE.md```.  

Le fichier ```README.md``` contient une description du jeu et les instructions nécessaires pour l'utiliser.  

Le fichier ```.gitignore``` contient une liste des fichiers qui ne seront pas pris en compte par git lors des ```git add``` et qui ne seront donc pas ajoutés/mis à jour dans le repository git.  

Les fichiers suivants servent a lancer le projet :  
- ```main.py```  
- ```start.sh```  

Le fichier ```cheats.py``` introduit l'implémentation des cheat code.  
Le fichier ```cheats_vars.py``` contient les variables partagées indiquant si un cheat code est activé ou non.  

Le fichier ```CONSTANTS.py``` contient des constantes nécessaires à plusieurs fichiers.  

Le fichier ```LAUNCH_SETUP.py``` possède les variables de lancement du jeu (plein écran, musique, etc...).  

Le fichier ```save.py``` contient les fonctions utiles pour la sauvegarde d'une partie.  

Le fichier ```game.py``` contient deux objets, l'un (`AoCE`) contenant la définition du programme principal, qui lance la première fenêtre avec la première vue (la vue du menu principal) en prenant en compte les paramètre de lancement de ```LAUNCH_SETUP.py```.  
Mais aussi l'objet `GameView`, qui va permettre d'initialiser (ou réinitialiser si on relance une partie) les variables `model`, `view` et `controler`.  

Les fichiers ```Model.py```, ```View.py``` et ```Controler.py``` contiennent respectivement les définitions des variables `model`, `view` et `controler` citées précédemment.  

Les dossiers [```entity```](#Dossier-entity), [```map```](#Dossier-map), [```Ressources```](#Dossier-Ressources), [```utils```](#Dossier-utils) et [```views```](#Dossier-views) sont détaillés dans les parties suivantes.  

### Dossier entity

Ce dossier contient la définition des différentes classes d’entités manipulables dans une partie de Age of Cheap Empires. Cela comprend donc toutes les unités, les bâtiments, etc...  

### Dossier map

Ce dossier contient les définitions de classe nécessaires à l'affichage et la génération des cartes et de la mini carte.

### Dossier Ressources

Ce dossier contient les images et les sons utilisés dans le projet.  

### Dossier utils

Ce dossier contient la définitions d'objets ou de fonctions qui sont utiles et utilisés dans plusieurs autres classes du jeu, par exemple la conversion des coordonnées entre map, isométriques et cartésiennes.  

### Dossier views

Ce dossier contient dans des fichiers `.py` distincts les différentes views (objets de arcade qui représente un affichage différent dans la fenêtre) qui se succéderont lors d'un parcours normal dans le jeu (sauf la vue en jeu qui elle se situe dans le fichier ```view.py``` de la racine).  
