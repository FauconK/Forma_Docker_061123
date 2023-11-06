# Forma_Docker

# Déployer un premier site web avec un Docker File

* Cloner le dépot github
* Compléter le code de monpremierdocker/site.py
  * On utilise flask pour faire tourner notre site web
  * Les requirements python pour le site web sont dans requirements.txt
  * flask run permet de lancer le site
  * Ne pas oublier d'export les variables d'env:
	* ENV FLASK_APP=site.py
	* ENV FLASK_RUN_HOST=0.0.0.0
* Créer un docker file 
  * On utilisera python:3.10-alpine comme image de base
    * L'avantage de alpine est que c'est une distribution très légère donc qui se lancera rapidement
  * Ne pas oublier de copier le requirement dans le docker
    * On utilise pip install pour installer des librairies
  * Le site sera sur le port 5000 (HTTP)
* Tester le site

## References 
* [Getting started with Flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/)
* [Containerize an application](https://docs.docker.com/get-started/02_our_app/)

# TP Docker Compose
## Vérification de l'installation de Docker et de Docker Compose
D'abord Docker :
```shell
docker version
```
Docker Compose :
```shell
docker compose version
```
Ensuite on vérifie le lancement de docker :
```shell
docker ps
```
Si à une des trois commandes, le message suivant apparaît, il faut démarrer Docker :
```
Cannot connect to the Docker daemon at unix:///Users/user/.docker/run/docker.sock. Is the docker daemon running?
```

## TP1 - Nginx
### Introduction
Pour cette partie, nous allons utiliser Nginx, Nginx est un logiciel qui aide à gérer les sites web. Il peut servir des pages web, équilibrer la charge du trafic, améliorer la sécurité, et bien plus encore. Il est apprécié pour sa rapidité et sa flexibilité, ce qui en fait un choix populaire pour de nombreux sites web et applications en ligne. 
Voici un schéma expliquant le rôle de Nginx :
!["Schéma Nginx"](images/Pasted%20image%2020231106015621.png)

Plus précisément, nous allons utiliser l'image Docker Nginx.
Une image Docker Nginx est comme un "conteneur" qui contient un serveur web Nginx prêt à l'emploi. Vous pouvez utiliser cette image pour facilement exécuter des serveurs web Nginx dans des environnements isolés et répétables, ce qui simplifie la gestion de sites web. C'est un peu comme avoir une boîte contenant tout ce dont vous avez besoin pour faire fonctionner Nginx, prête à être déployée sur un ordinateur.

### Préparation
```shell
mkdir mon-site-web
cd mon-site-web
```
Nous allons à l'intérieur de ce répertoire créer un site web basique que nous allons servir avec Nginx. 
Nous allons créer un fichier ``index.html`` avec le contenu suivant.
```html
<!DOCTYPE html>
<html>
<head>
    <title>Mon Site Web Docker Compose</title>
</head>
<body>
    <h1>Bienvenue sur mon site web Docker Compose !</h1>
    <p>Ceci est une démonstration de site web statique pour Docker Compose.</p>
</body>
</html>
```
### Fichier docker compose
Nous allons ensuite, créer un fichier ``docker-compose.yml``.
Le nom de ce fichier est __très important__ puisque lorsqu'on lance notre container avec docker compose, il va automatiquement chercher ce fichier. 
Le fichier docker compose comporte plusieurs sections, nous allons les détailler. 
Chaque fichier docker compose commence par une ligne qui explicite la version de la syntaxe du fichier qu'on utilise. Pour ce TP, nous allons utiliser la version 3 de la syntaxe car c'est la syntaxe la plus récente.
```yaml
version: '3'
```
Ensuite, nous allons définir avec le mot clé __service__, nos différents services, pour ce TP, nous n'avons qu'un seul service.
```yaml
services:
  le-nom-de-mon-service:
```
Vous pouvez donner n'importe quel nom à ce service et remarquer le niveau d'indentation qui est très important. Moi je vais appeler le service ``mon-site-web``
Maintenant, je dois préciser __les caractéristiques__ de mon service, pour ce service là nous avons besoin de 3 paramètres:
- Une image
- Un port
- Notre fichier `index.html`

Pour des questions de lisibilité nous allons aussi donner un nom à notre container en rajoutant la ligne suivante (facultatif):
```yaml
services:
  mon-site-web:
	  container_name: mon-container
```

On rajoute l'image Nginx à notre fichier docker compose tout en précisant d'utiliser la version la plus récente de l'image (pour les curieux, les versions de l'image Docker Nginx sont trouvable sur [Docker Hub](https://hub.docker.com/_/nginx/)).
```yaml
services:
  mon-site-web:
	  container_name: mon-container
	  image: nginx:latest
```
Pour le port, on va demander à Docker d'exposer le port 80 du conteneur Nginx sur le port 8080 de votre machine hôte.
```yaml
services:
  mon-site-web:
	  container_name: mon-container
	  image: nginx:latest
	  ports:
		  - "8080:80"
```
Pour finir, il nous reste plus qu'à donner le notre fichier ``index.html`` au conteneur. 
Le serveur web Nginx sert tous les fichiers qui se trouvent dans son répertoire `/usr/share/nginx/html/`. Nous allons donc dire à Nginx de mettre notre fichier ``index.html`` dans le dossier `/usr/share/nginx/html` du conteneur.
```yaml
version: '3'
services:
  mon-site-web:
	container_name: mon-container
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./index.html:/usr/share/nginx/html/index.html
```
### Lancement de notre conteneur
A l’intérieur de notre répertoire de travail, on execute la commande suivante.
```shell
docker-compose up -d
```
Si cette commande vous renvoie une erreur ou que si vous avez l'impression que le conteneur ne démarre pas, lancer la commande sans le `-d` cela vous permettra d'avoir des logs et de debug votre container.
Puis on visite l'url suivant : http://localhost:8080/
Et on devrait voir la page suivante !["Image navigateur"](images/Pasted%20image%2020231106023433.png)
### Arrêter le conteneur et le supprimer
Il y a deux choses à supprimer, notre conteneur, et notre image de conteneur. Pour lister les conteneur on utiliser la commande `docker ps` (`ps`, signifiant process status), cependant cette commande ne renvoie uniquement les conteneurs en exécution et pas les conteneurs qui sont déjà arrêtés, pour tout afficher, on va rajouter le flag `--all`.  Là, on identifie bien notre conteneur dans la liste grâce à la commande suivante.
```shell
docker ps --all
```
Avant de supprimer notre conteneur il faut l’arrêter.
```shell
docker stop mon-container
```
`mon-container`étant le nom que j'ai donné à mon conteneur.
Ensuite on peut supprimer notre conteneur.
```shell
docker rm mon-container
```
Une fois que le conteneur est supprimé, on peut supprimer l'image Nginx que Docker a téléchargé pour nous.
D’abord, on liste les images.
```shell
docker image list
```
On identifie les images que l'on veut supprimer ici c'est l'image Nginx puis on fait
```shell
docker image rm nginx
```

Voilà voilà c'est la fin de ce TP. 
Félicitations, nous avez appris à décrire votre conteneur dans un fichier `docker-compose.yml` et à le lancer.

## TP2 - WordPress
### Introduction
Dans cette partie, nous allons déployer localement WordPress sur votre ordinateur en utilisant des conteneurs et un fichier `docker-compose.yml`. Cette partie contrairement à la partie précédente est une vraie utilisation qu'on pourrait avoir de Docker. Avant de déployer un logiciel pour notre entreprise/asso on peut être amené à le tester sur notre machine pour voir s'il convient bien aux attentes de l'organisation. 

__Qu'est ce que WordPress ?__ 
WordPress est un système de gestion de contenu (CMS) open-source populaire pour la création de sites web et de blogs. Il offre une interface conviviale, des thèmes et des plugins pour personnaliser votre site, une gestion de contenu flexible, des fonctionnalités de blogging avancées, et il est optimisé pour les moteurs de recherche. WordPress est largement utilisé et bénéficie d'une grande communauté de soutien.
En gros wordpress est un logiciel permettant de faire des sites web sans devoir coder.
Aujourd’hui [43% des sites web sont créés avec WordPress.](https://www.ionos.fr/digitalguide/hebergement/blogs/quest-ce-que-wordpress/)

Dans un premier temps, il faut réfléchir à l’architecture de notre déploiement. 
Il nous faudra en gros d'après la documentation 
- Un conteneur WordPress
	- Un endroit où stocker les plugins, les thèmes...
	- Un moyen de laisser l'utilisateur se connecter à WordPress
- Un conteneur pour la base de donnée
	- Un endroit où stocker les données des utilisateurs( les comptes, les sites web...)
	- Un moyen de laisser WordPress se connecter à la base de donnée.

Avec un schéma ça donne ça
![[docker.drawio 1.png]]
On va commencer à décrire cette architecture multi-conteneur dans un fichier `docker-compose.yml`.
### Fichier docker compose
Nous allons dans un premier temps créer un nouveau dossier vide.
```shell
mkdir mon-wordpress
cd mon-wordpress
```
Ensuite on va créer un fichier `docker-compose.yml`.
À l’intérieur de ce fichier, nous allons créer deux services, un service `wordpress`pour WordPress et un service `db` pour la base de donnée.
Notre fichier docker compose ressemble donc à ça pour le moment.
```yaml
services:
	db:
	wordpress:
```
Nous allons rajouter les images pour les deux conteneurs.
Pour la db nous allons utiliser une image MariaDB, qui est la base de donnée relationnel recommandée pour WordPress, nous allons utiliser une version spéciale pour être sûr que ça marche sur l'ordinateur de tous le monde.
Ça donne donc ça
```yaml
services:
	db:
		image: mariadb:10.6.4-focal
	wordpress:
		image: wordpress:latest
```
Maintenant, nous aimerions que les deux conteneurs puissent communiquer entre eux. Plus précisément, on aimerais que la base de donnée expose ses ports 3306 et 33060 au conteneur wordpress. Du côté de wordpress, on aimerait rendre son interface accessible par l'utilisateur sur le port 80.
```yaml
services:
	db:
		image: mariadb:10.6.4-focal
		expose:
			- 3306
			- 33060
	wordpress:
		image: wordpress:latest
		ports:
			- 80:80
```
Ici, `ports` est utilisé pour exposer des ports des conteneurs à l'hôte pour un accès externe, tandis que `expose` est utilisé pour permettre aux conteneurs dans le même réseau Docker de communiquer entre eux sans exposer ces ports à l'extérieur du réseau.

Nous allons à présent définir un __Volume Docker__ où wordpress et la base de donnée peuvent stocker leurs données. Un volume Docker est un moyen de stocker des données en dehors du conteneur lui-même, mais de manière à ce que le conteneur puisse y accéder. Cela permet de partager et de persister des données entre différents conteneurs et de conserver des données même si un conteneur est arrêté ou supprimé. Les volumes Docker sont utilisés pour stocker des fichiers, des bases de données, des configurations, etc., de manière à ce qu'ils soient accessibles et préservés même lorsque les conteneurs qui les utilisent sont démarrés, arrêtés ou supprimés.
```yaml
services:
	db:
		image: mariadb:10.6.4-focal
		expose:
			- 3306
			- 33060
		volumes:
			- db_data:/var/lib/mysql
	wordpress:
		image: wordpress:latest
		ports:
			- 80:80
		volumes:
			- wp_data:/var/www/html
volumes:
  db_data:
  wp_data:
```

Nous allons maintenant passer quelques variables d'environnement aux deux conteneurs, ces variables d'environnement sont des variables définies par la documentation de wordpress. 
Une variable d'environnement Docker est une valeur spécifique que vous pouvez définir pour influencer le comportement d'un conteneur Docker. C'est comme une petite note que vous donnez au conteneur pour lui dire comment se comporter. Par exemple, vous pouvez définir une variable d'environnement pour spécifier un mot de passe, une URL, ou d'autres paramètres nécessaires à une application qui s'exécute dans le conteneur. Ces variables sont utilisées par les applications à l'intérieur du conteneur pour configurer leur fonctionnement.
Nous allons définir les variables suivantes
Pour wordpress:
 - WORDPRESS_DB_HOST=db
 - WORDPRESS_DB_USER=wordpress
 - WORDPRESS_DB_PASSWORD=wordpress
 - WORDPRESS_DB_NAME=wordpress
Pour la base de donnée
- MYSQL_ROOT_PASSWORD=somewordpress
- MYSQL_DATABASE=wordpress
- MYSQL_USER=wordpress
- MYSQL_PASSWORD=wordpress

A noté que vous être libre de changer la valeur de ces variables.
Voici ce que ça donne
```yaml
services:
	db:
		image: mariadb:10.6.4-focal
		expose:
			- 3306
			- 33060
		volumes:
			- db_data:/var/lib/mysql
		environment:
			- MYSQL_ROOT_PASSWORD=somewordpress
			- MYSQL_DATABASE=wordpress
			- MYSQL_USER=wordpress
			- MYSQL_PASSWORD=wordpress
	wordpress:
		image: wordpress:latest
		ports:
			- 80:80
		volumes:
			- wp_data:/var/www/html
		environment:
			- WORDPRESS_DB_HOST=db
			- WORDPRESS_DB_USER=wordpress
			- WORDPRESS_DB_PASSWORD=wordpress
			- WORDPRESS_DB_NAME=wordpress
volumes:
  db_data:
  wp_data:
```

Nous avons bientôt fini, nous devons juste préciser aux conteneurs quoi faire au cas où il y a un plantage, c'est optionnel mais c'est recommandé.
Nous allons rajouter `restart: always` aux deux containers cela dit aux containers de toujours redémarrer s'il y a un plantage.
```yaml
services:
	db:
		image: mariadb:10.6.4-focal
		expose:
			- 3306
			- 33060
		volumes:
			- db_data:/var/lib/mysql
		environment:
			- MYSQL_ROOT_PASSWORD=somewordpress
			- MYSQL_DATABASE=wordpress
			- MYSQL_USER=wordpress
			- MYSQL_PASSWORD=wordpress
		restart: always
	wordpress:
		image: wordpress:latest
		ports:
			- 80:80
		volumes:
			- wp_data:/var/www/html
		environment:
			- WORDPRESS_DB_HOST=db
			- WORDPRESS_DB_USER=wordpress
			- WORDPRESS_DB_PASSWORD=wordpress
			- WORDPRESS_DB_NAME=wordpress
		restart: always
volumes:
  db_data:
  wp_data:
```
Pour finir, d'après la documentation de la base de donnée, il faut rajouter un argument supplémentaire pour configurer le conteneur de la base de donnée MariaDB pour utiliser une méthode d'authentification spécifique.
On rajoute donc la ligne suivante à la configuration de la base de donnée.
```yaml
command: '--default-authentication-plugin=mysql_native_password'
```
Le fichier `docker-compose.yaml` final ressemble à ça
```yaml
services:
	db:
		image: mariadb:10.6.4-focal
		expose:
			- 3306
			- 33060
		volumes:
			- db_data:/var/lib/mysql
		environment:
			- MYSQL_ROOT_PASSWORD=somewordpress
			- MYSQL_DATABASE=wordpress
			- MYSQL_USER=wordpress
			- MYSQL_PASSWORD=wordpress
		restart: always
		command: '--default-authentication-plugin=mysql_native_password'
	wordpress:
		image: wordpress:latest
		ports:
			- 80:80
		volumes:
			- wp_data:/var/www/html
		environment:
			- WORDPRESS_DB_HOST=db
			- WORDPRESS_DB_USER=wordpress
			- WORDPRESS_DB_PASSWORD=wordpress
			- WORDPRESS_DB_NAME=wordpress
		restart: always
volumes:
  db_data:
  wp_data:
```

Maintenant, pour lancer les conteneurs docker. On execute dans le répertoire de ce fichier la commande suivante.
```shell
docker compose up -d
```
Si on a l'impression qu'il y a un problème, on peut retirer le `-d` pour voir exactement ce qu'il se passe.

Ensuite nous pouvons nous rendre sur http://localhost (ou http://localhost:80 pour certain). 
Nous devrions voir la page suivante s'afficher !["Image WordPress"](images/Pasted%20image%2020231106141526.png)
!["Image WordPress 2"](images/Pasted%20image%2020231106141540.png)
Il ne reste plus qu'a configurer WordPress mais cela est en dehors de la porté de ce TP. Pour ceux qui souhaitent approfondir l’installation de WordPress voici deux liens utiles. [Installation en 5min](https://fr.wordpress.org/support/article/how-to-install-wordpress/) et [les premiers pas avec WordPress](https://fr.wordpress.org/support/article/first-steps-with-wordpress/).

###  Arrêter les containers et les supprimer
Il suffit de faire comme dans le TP1 - Nginx pour supprimer les conteneurs et les images. Ce qu'il y a de plus à supprimer c'est les volumes qui stockent la configuration de WordPress et de la base de donnée.
Pour les lister on fait
```shell
docker volume ls
```
Puis on fait pour supprimer
```shell
docker volume rm db_data
```
et
```shell
docker volume rm wp_data
```
On peut vérifier avec la commande suivante si tous les volumes sont bien supprimés 
```shell
docker volume ls
```

Voilà vous savez maintenant comment créer un fichier `docker-compose.yml` pour décrire un déploiement, vous connaissez la structure du fichier docker-compose et vous avez appris comment utiliser quelque directives comme
- Utiliser la directive `image` pour spécifier l'image de conteneur à utiliser pour chaque service.
- Utiliser la directive `expose` pour définir les ports à exposer pour permettre la communication entre les conteneurs dans le même réseau Docker.
- Utiliser la directive `ports` pour définir les ports à exposer pour l'utilisateur.
- Utiliser la directive `volumes` pour créer et attacher des volumes Docker aux services afin de stocker les données de manière persistante.
- Utiliser la directive `environment` pour configurer des variables d'environnement spécifiques pour chaque service.
- Utiliser la directive `restart` pour spécifier la règle de redémarrage, comme "always".
- Utiliser la directive `command` pour fournir des arguments de commande personnalisés pour les conteneurs.

FIN.
