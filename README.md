# Projet python 2A
**Projet d'informatique de deuxième année à l'ENSAE Paris**  


Le détail de l'analyse réalisée est disponible [dans ce Notebook](https://github.com/taucmar/projet-python-2a/blob/main/rapport_commentaires_youtube.ipynb).  


Les commentaires postés sous les vidéos YouTube sont une source d'information pour les créateurs de contenu, ainsi que les "likes".  
Ils permettent au vidéaste de déterminer si son travail a plu ou non à son audience. Cependant, les Youtubeurs n'ont pas nécessairement le temps de tous les lire. Il nous a donc semblé intéressant d'analyser ces commentaires informatiquement, plutôt que de les traiter un à un.

Pour ce projet, nous nous sommes penchés sur la chaîne YouTube DirtyBiology, qui fait de la vulgarisation scientifique. Notre choix a été motivé par le fait que les commentaires sous ces vidéos sont à la fois nombreux (car la chaîne est relativement connue), en phrases (étant donné l'audience cible) et relativement corrects au niveau de la syntaxe.

Ces conditions réunies, nous devrions avoir des données exploitables pour l'étude que nous souhaitons faire : une analyse de sentiment.  


   ![DirtyBiology](logo_intro2.png#center)  
   *Logo DirtyBiology*  
   [Source](https://teespring.com/fr/stores/dirtybiology-3)


## Prérequis
Tout d'abord, il faut lancer la commande `pip install -r requirements.txt` afin d'installer tous les packages nécessaires au bon fonctionnement de notre code. 

Pour résumer les étapes de notre travail, nous avons fait du web scraping depuis YouTube, ce pour quoi nous avons dû créer une clé API pour l'[API YouTube Data](https://developers.google.com/youtube/v3) via la [Console Google Cloud](https://console.cloud.google.com/home/dashboard?project=api-youtube-333917). Cela permet d'accéder aux données publiques de YouTube de manière anonyme et d'associer des requêtes API à notre projet.  
La marche à suivre est la suivante : créer un projet, et activer l'API suivante dans le tableau de bord : `Youtube Data API v3`. La démarche est très bien expliquée sur [ce site](https://www.sebastiencoenon.fr/blog/nouveautes/52-creation-d-une-cle-api-youtube). 



Le script `scraper.py` va chercher ces données et les stocke dans le fichier `comments.csv`.
Les clés API Google sont confidentielles, nous n'avons donc pas intégré les notres au dépôt GitHub. Le code peut tout de même fonctionner correctement, il faut créer un fichier s'apppelant `".env"` et y placer la ligne suivante :    
```APIKEY="identifiant_de_la_clé"```  
Veuillez bien à ne pas mettre d'espace autour du symbole "=".  
Sinon, le fichier `comments.csv` est lui disponible dans notre dépôt.


  


**Ceci étant fait, nous avons récupéré les 100 commentaires les plus "pertinents" d'une vidéo, et ce sur 20 vidéos différentes. Ceci constitue une base de données de 2000 commentaires, ainsi que des données supplémentaires comme le nombre de likes, le nom d'utilisateur des personnes qui commentent...**

> Concernant le choix des commentaires (limités à 100 par vidéo par l'API), le paramètre `order` spécifie l'ordre dans lequel la réponse de l'API doit lister le flux de commentaires. On peut soit choisir `time` - Le flux de commentaires est sélectionné de manière chronologique. Soit `relevance` - Le flux est classé par pertinence.
C'est cette dernière option que nous avons choisi pour l'analyse de texte.

Le script `cleaning.py` prépare le texte aux applications des autres parties en le nettoyant : il retire  les caractères particuliers (engendrés par des smileys ou des sauts de ligne, par exemple).



## Etude des commentaires de la chaine YouTube DirtyBiology


### Analyse exploratoire quantitative
Nous avons commencé par analyser les données propres aux vidéos et à l'engagement qu'elles suscitent, à travers le nombre de likes et de commentaires qu'elles reçoivent.  

   ![image](/graphs/description_videos.png)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)


Une faible proportion (0.4%) des personnes qui regardent la vidéo vont y laisser un commentaire. De plus, plus la vidéo est ancienne, plus les gens qui la regardent ont tendance à la commenter.

### WordCloud
D'après les vidéos que nous avons étudiées, on voit que les commentaires sont globalement très positifs, beaucoup de remerciements en ressortent et le montage est souvent salué. C'est du moins ce qu'on observe dans les différents WordClouds que nous avons réalisés, par exemple : 

   ![logo](/graphs/logo_dirty_bio.png)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)
   
   
### Polarisation des commentaires
Nous avons réalisé une [analyse de sentiments](https://datafranca.org/wiki/Polarité_de_sentiments), c'est-à-dire interprété et classifié les émotions (positives, négatives et neutres) dans les données textuelles à l’aide de techniques d’analyse de texte.
La **polarité** dans l'analyse des sentiments fait référence à **l'identification de l'orientation des sentiments** dans un langage écrit : la polarité d'un commentaire est un nombre entre -1 et 1 qui "note" l'impression générale que dégage le commentaire (-1 étant très insatisfait et 1 parfaitement satisfait). 

   ![image](sentiment.png#center)   
   [Source](https://blogdigital.beijaflore.com/text-mining-analyse-de-sentiments/)


Voici deux histogrammes de la polarité des commentaires sous une des vidéos YouTube de DirtyBiology :

   ![image](/graphs/histogrammes_polarites.png#center)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)
   
   
Dans cette étude, nous observons des valeurs de polarités allant entre -0.2 et 1. Les histogrammes viennent confirmer le caractère positif des commentaires postés sous cette vidéo.

### Analyse en composantes principales
Pour aller plus loin, une ACP permet de visualiser les différences entre les commentaires, et étudier les plus extrêmes puisque l'ACP conserve un maximum de variance. Dans un premier temps, nous utilisons la bibliothèque [Sentence Transformer](https://github.com/UKPLab/sentence-transformers) pour transformer les phrases en vecteurs réels.  
On réunit les commentaires par **clusters**. On récupère aussi les commentaires les plus proches des centroïdes afin d'avoir des commentaires "représentants".

   ![image](/graphs/acp_clusters.png#center)   
   
Voici les commentaires correspondant aux centroïdes des clusters.  
>0 : un régal, comme d'hab! merci pour ce très beau travail  
1 : édifiant...  
et super vidéo comme d'habitude. trop fier de te soutenir sur teepee. merci à toi pour l'intelligence que tu dispense autour de toi.  
2 : j'adore tes vidéos ! le montage est vraiment bien en plus, continue comme ça  
3 : merci pour ton travail de recherche et de vulgarisation ❤️  
4 : le montage est toujours aussi bon c’est ouf  


Même si l'ACP vise à conserver un maximum de variabilité, on voit encore que les commentaires sont tous similaires et positifs. Ceci suggère que ce qui éloigne les différents clusters les uns des autres ne réside pas dans la positivité ou négativité du commentaire.  

   ![image](/graphs/acp_20vid.png#center)  
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)  
Si l'on regarde le phénomène sur l'ensemble des vidéos, nous constatons qu'aucune ne se démarque particulièrement des autres en terme de réactions dans les commentaires.  



Nous avons aussi voulu mettre en valeur les commentaires remerciant explicitement le vidéaste. 

   ![image](/graphs/acp_remerciements.png#center)   
   [Source](https://github.com/taucmar/projet-python-2a/tree/main/graphs)  
   

Finalement, les remerciements occupent quasiment tout l'espace de commentaires.

## Conclusion  

Il y a beaucoup de manières d'analyser informatiquement les données que YouTube met à disposition des vidéastes. Nous en avons étudié et présenté quelques unes dans ce projet.
Nous avons commencé par analyser les données propres aux vidéos et à l'engagement qu'elles suscitent, à travers le nombre de likes et de commentaires qu'elles reçoivent. Ensuite, nous nous sommes penchés sur le contenu des commentaires. Nous avons étudié les mots qui revenaient le plus souvent, afin de dégager les thèmes majoritairement abordés par les viewers donnant leur opinion à propos de la vidéo. Ensuite, nous avons calculé et analysé la polarité des commentaires, un score entre -1 et 1 qui exprime le sentiment que dégage un commentaire. Enfin, nous avons étudié les différences entre les commentaires à l'aide d'une Analyse en Composantes Principales.
Toutes ces analyses nous ont mené à la conclusion que les commentaires sous les vidéos de DirtyBiology sont en grande majorité positifs, parfois neutres. Parmis leurs nombreuses similarités, la communauté du YouTubeur semble exprimer une vive reconnaissance pour ses vidéos, et une appréciation particulière de la qualité de son travail, notamment l'attention portée au montage.  


