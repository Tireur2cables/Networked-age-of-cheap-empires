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

Les dossiers [```entity```](#Dossier-entity), ```map```, ```Ressources```, ```utils``` et ```view``` sont détaillés dans les parties suivantes.  

### Dossier entity

### Dossier map

### Dossier Ressources

### Dossier utils

### Dossier views
