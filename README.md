# projet-python-2a
**Projet d'informatique de deuxième année dans le cadre du cursus de l'ENSAE Paris**  

Les commentaires postés sous les vidéos YouTube sont une source d'information pour les créateurs de contenu, ainsi que les "likes".  
Ils permettent au vidéaste de déterminer si son travail a plu ou non à son audience. Cependant, les Youtubeurs n'ont pas nécessairement le temps de tous les lire. Il nous a donc semblé intéressant d'analyser ces commentaires informatiquement, plutôt que de les traiter un à un.

Pour ce projet, nous nous sommes penchés sur la chaîne YouTube DirtyBiology, qui fait de la vulgarisation scientifique. Notre choix a été motivé par le fait que les commentaires sous de telles vidéos sont à la fois nombreux (car la chaîne est relativement connue), constructifs (de par le contenu scientifique) et relativement corrects au niveau de la syntaxe.

Ces conditions réunies, nous devrions avoir des données exploitables pour l'étude que nous souhaitons faire : une analyse de sentiment.  


   ![DirtyBiology](logo_intro2.png#center)  
   *Logo DirtyBiology*  
   [Source](https://teespring.com/fr/stores/dirtybiology-3)


## Prérequis
Tout d'abord, il faut lancer le `pip install -r requirements.txt` afin d'installer tous les packages nécessaires au bon fonctionnement de notre code. 

Pour résumer les étapes de notre travail, nous avons fait du web scraping depuis YouTube, ce pour quoi nous avons dû créer une clé API avec l'[API YouTube Data](https://developers.google.com/youtube/v3). Cela permet d'accéder aux données publiques de YouTube de manière anonyme et d'associer des requêtes API à notre projet.  
Pour créer une clé API YouTube, il faut se commecter dans la [Console Google Cloud](https://console.cloud.google.com/home/dashboard?project=api-youtube-333917), créer un projet, et activer l'API suivante dans le tableau de bord : `Youtube Data API v3`. La démarche est très bien expliquée sur [ce site](https://www.sebastiencoenon.fr/blog/nouveautes/52-creation-d-une-cle-api-youtube). 



Le script `scraper.py` va chercher ces données et les stocke dans le fichier `comments.csv`  
Les API Google fonctionnent avec des clés d'identification confidentielles, qui n'apparaissent par conséquent pas dans le dépot GitHub. Pour faire fonctionner le script correctement, il faut créer un fichier s'apppelant `".env"` et y placer la ligne suivante :  
```APIKEY="identifiant_de_la_clé"```


  


**Ceci étant fait, nous avons récupéré les 100 commentaires les plus "pertinents" d'une vidéo, et ce sur 20 vidéos différentes. Ceci constitue une base de données de 2000 commentaires, ainsi que des données supplémentaires comme le nombre de likes, le nom d'utilisateur des personnes qui commentent...**

> Concernant le choix des commentaires (limités à 100 par vidéo), le paramètre `order` spécifie l'ordre dans lequel la réponse de l'API doit lister le flux de commentaires. On peut soit choisir `time` - Le flux de commentaires est sélectionné de manière chronologique. Soit `relevance` - Le flux est classé par pertinence.
C'est ce que nous avons choisi pour l'analyse de texte.

## Conclusion
D'après les vidéos que nous avons étudiées, on voit que les commentaires sont globalement très positifs, beaucoup de remerciements en ressortent et le montage est souvent salué. C'est du moins ce qu'on observe dans les différents WordCloud que nous avons réalisés, par exemple : 

   ![WordCloud](/graphs/logo_dirty_bio.png)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)
   
   
### Polarisation des commentaires
Nous allons de réaliser une [analyse de sentiments](https://datafranca.org/wiki/Polarité_de_sentiments), c'est-à-dire l’interprétation et la classification des émotions (positives, négatives et neutres) dans les données textuelles à l’aide de techniques d’analyse de texte.
La **polarité** dans l'analyse des sentiments fait référence à **l'identification de l'orientation des sentiments** (positif, neutre et négatif) dans un langage écrit. La polarité d'un commentaire est un nombre entre -1 et 1 qui "note" l'impression générale du commentaire (0 étant neutre et 1 étant parfaitement satisfaisant). 

   ![WordCloud](sentiment.png#center)   
   [Source](https://blogdigital.beijaflore.com/text-mining-analyse-de-sentiments/)

Voici un histogramme de la polarité des commentaires sous une vidéo YouTube de DirtyBiology :

   ![WordCloud](/graphs/histogram_polarity.png#center)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)
   
Dans cette étude, nous observons des valeurs de polarités allant entre -0.2 et 1. L'histogramme vient confirmer le caractère positif des commentaires postés sous les vidéos.

### Analyse en composantes principales
Pour aller encore plus loin, nous allons faire une ACP pour visualiser les différences entre les commentaires, et étudier les plus extrêmes, puisque l'ACP conserve un maximum de variance. Dans un premier temps, nous utilisons la bibliothèque [Sentence Transformer](https://github.com/UKPLab/sentence-transformers) pour transformer les phrases en vecteurs réels. On peut ensuite encoder le texte, ce qui les transforme en vecteurs de $\mathbb{R}^{768}$, qu'on projette après dans $\mathbb{R}^{2}$.  
On réunit les commentaires par **clusters**. On récupère aussi les commentaires les plus proches des centroïdes afin d'avoir des commentaires "représentants".

   ![WordCloud](/graphs/acp1.png#center)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)

Les commentaires centroides sont tous positifs.  
Cela qui suggère que ce qui éloigne les différents clusters les uns des autres ne réside pas dans la positivité ou négativité du commentaire.  


Pour vérfier encore ces similarités, on affiche simultannément l'ACP pour chaque nuage de point plutôt que de les superposer.
Afin de pouvoir les comparer visuellement facilement, on entoure les nuages de points par l'enveloppe convexe du nuage total :

   ![WordCloud](/graphs/acp_comparaison.png#center)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)

Les nuages de points semblent se déplacer de gauche à droite principalement, mais les variations ne sont pas énormes. Concrètement, les vidéos suscitent des réations similaires. 

   ![WordCloud](/graphs/acp_convex_hull.png#center)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)

On remarque tout de suite que les commentaires de la région en haut à gauche (1, 2, 12, 13 et 14) partagent tous le même mot : "merci" et saluent la qualité et l'intérêt qu'ils ont pour la vidéo *('passionnant', 'enrichissant', 'intéressant', 'beau travail', 'travail de qualité')*. Les commentaires du bas sont également élogieux. Tandis que les commentaires de la région opposée intègrent du langage fleuri *(6: 'bordel', 8: 'merde')* et sont moins élogieux. Le commentaire le plus à droite semble venir d'un professeur voulant se renseigner.  
On peut donc supposer que plus on se déplace vers la partie gauche de l'espace, plus les commentaires sont élogieux, et les remerciements nombreux.

Le détail de l'analyse réalisée est disponible [ici](https://github.com/taucmar/projet-python-2a/blob/main/rapport_commentaires_youtube.ipynb).

