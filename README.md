# Fignos

Ce logiciel a pour objectif de permettre une meilleure gestion des stocks de boisson lors du gala des Arts et Métiers de Bordeaux (la Nuit des Fignos).

## Pour bien commencer

Pour tester et utiliser le logiciel, suivez les instructions suivantes :

### Prérequis

Ce logiciel nécessite une version fonctionnnelle de python version 3 (3.5 conseillée) et la bibliothèque pyQt en version 5.

Sous Debian ou Ubuntu, exécutez les commandes suivantes :
* `sudo apt-get install python3`  
* `sudo pip3 install pyqt5` ou `sudo apt-get install python3-pyqt5`

Sous Windows, installez python depuis le site officiel et tapez dans la console :
* `pip3 install pyqt5`

### Utilisation

Une fois les fichiers présents sur votre ordinateur, lancez le programme qui vous intéresse via le fichier bash dédié :
* `sh serveur` ou `sh client`

## Version

Ce logiciel est actuellement en version 0.0.1.

## Auteurs

Ce logiciel a été développé par l'équipe des T\&lek'ss de Bordel'ss (216 et .17).

## Thuys git

Pour gérer le projet on utilise le logiciel git :

### Clone

Cette commande permet de cloner le dépôt sur votre machine.

Placez vous dans le dossier parent de celui où vous souhaitez travailler :
* `cd [chemin relatif du dossier depuis le répertoire actuel ou chemin absolu]`
    * Exemple : `cd mes-projets` ou `cd /home/mon-compte/mes-projets`

Clonez le dépôt :
* `git clone git@gitlab.com:telek_s/fignos.git`

### Push

Ces commandes permettent de publier sur le serveur les changements que vous avez effectué.

Ajoutez les fichiers que vous souhaitez sauvegarder :
* `git add [nom du (des) fichier(s) ou chaine de sélection]`
    * Exemples : `git add .` ou `git add *.py`

Ajoutez les informations de modification :
* `git commit`

Publiez les modificationsque vous avez effectuées :
* `git push origin dev`

### Pull

Ces commandes permettent de récupérer la dernière version du logiciel sur le serveur en ignorant les possibles conflits.

Sauvegardez vos changements non enregistrés (optionnel) :
* `git stash`

Récupérez la dernière version du serveur :
* `git pull origin dev`

Récupérez les changements non sauvegardés :
* `git stash pop`

