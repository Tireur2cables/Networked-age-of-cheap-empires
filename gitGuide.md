# GIT GUIDE #

## Enlever les branches inutiles

`git remote prune origin --dry-run` | permet de lister les remotes qui vont etre supprimées
`git remote prune origin` | permet de les supprimer
`git branch -d nomdelabranche` | supprimer les branches locales restantes

## Enlever des fichiers/dossiers déjà push mais maintenant dans le .gitignore  

`git rm -r --cached .` | Permet de vider `EN ENTIER` le repository.  
`git add .`            | Permet d'ajouter à nouveau l'arborescence au repository en prenant en compte le .gitignore.  
`git commit -m "..."`  | Permet de commit le repository.  
`git push`             | Permet de push le repository sur la branch.  


## LES COMMANDES DE BASE

git `add` [nomdufichier / . pour tous les fichiers]  &nbsp; &nbsp;   | ajoute les fichiers modifiés  
git `commit`  (-m "message de commit") &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;        | valide les modifications  
git `push` &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;  &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp; | envoie les modifications sur le serveur  
git `pull`                                               | télécharge les fichiers du serveur  
git `checkout` [(-b) nomdelabranche]                     | annule les changements en cours, ou change de branche  
git `status`                                             | affiche les changements en cours  

## LES COMMANDES INTERESSANTES

git `log`                                                | affiche l'historique de la branche  
git `fetch`                                              | télécharge le contenu du serveur, sans le fusionner (faire git pull après)  
git `revert` [SHA du commit]                             | annule un commit  
git `push` --set-upstream origin [nomdelabranche]        | créé une nouvelle branche sur le serveur  
git `branch` [-a]                                        | Affiche les branches du projet  
git `rebase` [branche]                                   | Télécharge et fusionne les changements d'une branche dans la votre    

## MERGE DANS LE TERMINAL
branchefille -> Branche que vous allez fusionner  
branchmere -> Branche dans laquelle vous allez la fusionner  

git `fetch` origin  
git `checkout` -b "[branchefille]" "origin/[branchefille]"  
Vous avez maintenant téléchargé les modifications, vous pouvez les parcourir.  
git `fetch` origin  
git `checkout` "origin/[branchemere]"  
git `merge` --no-ff "[branchefille]"  
Ici il y aura potentiellement des conflits, que vous pouvez résoudre facilement.  
git `push` origin "branchemere"

## PETIT EXEMPLE

git `pull` -> Je télécharge les données qui sont sur le serveur  
git `checkout` gitGuide -> Je vais jeter un coup d’œil au super guide que nous avons pour me rafraîchir la mémoire sur l'utilisation de git  
git `checkout` develop -> Il est l'heure de travailler, je vais sur la branche develop  
git `checkout` -b ajoutCSS -> Je veut commencer le CSS du site, je fais donc une branche qui part de develop et qui s'appel ajoutCSS  
-> Je travail sur ma branche  
git `add` master.css -> J'ajoute le fichier que je viens de créer dans git  
git `commit` -m "Ajout des première lignes de CSS" -> Je commit mes changements  
git `push` --set-upstream origin ajoutCSS -> Je publie ma branche sur le serveur  

-> Plus tard  
-> Je fais des changements sur mon fichier CSS  
git `status` -> Pour voir les fichers que j'ai modifiés  
-> Mais Nicolas trouvais le fond du site plus jolie en violet, il a push un changement sur le fichier sur lequel je travaillais  
-> Je ne peut pas push mes changements, il y a un conflit  
git `pull` -> Je télécharge les nouveaux changements, le terminal (ou Atom(pour ne citer que lui)) m'indique qu'il y a un conflit  
-> Dans mon fichier il y a des grosses balises qui entourent les zones de conflit, a moi de choisir comment je les résout, ce que je garde et ce que je supprime  
git `add` master.css -> Je valide mes choix  
git `commit` -m "résolution du conflit entre Nicolas et moi" -> Je commit mon changement sur mon répertoire local  
git `push` -> Je push les nouveaux changements sur le serveur  



Sur atom tout se fait très bien, dans le menu en bas a droite, vous pouvez pull, push, add, commit et résoudre les conflits
