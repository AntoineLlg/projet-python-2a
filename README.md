# projet-python-2a
Projet d'informatique de deuxième année dans le cadre du cursus de l'ENSAE Paris  

Les commentaires postés sous les vidéos YouTube sont une source d'information pour les créateurs de contenu, ainsi que les "likes". Ils permettent au vidéaste de déterminer si son travail a plu ou non à son audience. Cependant, les Youtubeurs n'ont pas nécessairement le temps de tous les lire. Il nous a donc semblé intéressant d'analyser ces commentaires informatiquement, plutôt que de les traiter un à un.

Pour ce projet, nous nous sommes penchés sur la chaîne YouTube DirtyBiology, qui fait de la vulgarisation scientifique. Notre choix a été motivé par le fait que les commentaires sous de telles vidéos sont à la fois nombreux (car la chaîne est relativement connue), constructifs (de par le contenu scientifique) et relativement corrects au niveau de la syntaxe.

Ces conditions réunies, nous devrions avoir des données exploitables pour l'étude que nous souhaitons faire : une analyse de sentiment.


![DirtyBiology](dirtybiology.png#center)  
[Source](https://www.pinterest.fr/pin/148689225175699166/#center)


## Prérequis
Tout d'abord, il faut lancer le `pip install -r requirements.txt` afin d'installer tous les packages nécessaires au bon fonctionnement de notre code. 

Pour résumer les étapes de notre travail, nous avons fait du web scraping depuis YouTube, ce pour quoi nous avons dû créer une clé API avec l'[API YouTube Data](https://developers.google.com/youtube/v3). Cela permet d'accéder aux données publiques de YouTube de manière anonyme et d'associer des requêtes API à notre projet. 

Ceci étant fait, nous avons récupéré les 100 commentaires les plus "pertinents" d'une vidéo, et ce sur 20 vidéos différentes. Ceci constitue une base de données de 2000 commentaires, ainsi que des données supplémentaires comme le nombre de likes, le nom d'utilisateur des personnes qui commentent...


Le script `scraper.py` va chercher ces données et les stocke dans le fichier `comments.csv`  
Les API Google fonctionnent avec des clés d'identification confidentielles, qui n'apparaissent par conséquent pas dans le dépot GitHub. Pour faire fonctionner le script correctement, il faut créer un fichier s'apppelant `".env"` et y placer la ligne suivante :  
`APIKEY="identifiant_de_la_clé"`

Concernant le choix des commentaires (limités à 100 par vidéo), le paramètre `order` spécifie l'ordre dans lequel la réponse de l'API doit lister le flux de commentaires. On peut soit choisir `time` - Le flux de commentaires est sélectionné de manière chronologique. Soit `relevance` - Le flux est classé par pertinence.
C'est ce que nous avons choisi pour l'analyse de texte.

