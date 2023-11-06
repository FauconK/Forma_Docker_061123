# Forma_Docker

## Déployer un premier site web avec un Docker File

* Cloner le dépot github
* Compléter le code de monpremierdocker/site.py
  * On utilise flask pour faire tourner notre site web
  * Les requirements python pour le site web sont dans requirements.txt
  * flask run permet de lancer le site
* Créer un docker file 
  * On utilisera python:3.10-alpine comme image de base
    * L'avantage de alpine est que c'est une distribution très légère donc qui se lancera rapidement
  * Ne pas oublier de copier le requirement dans le docker
    * On utilise pip install pour installer des librairies
  * Le site sera sur le port 5000 (HTTP)
* Tester le site

### References 
* [Getting started with Flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/)
* [Containerize an application](https://docs.docker.com/get-started/02_our_app/)

## Déployer un nginx