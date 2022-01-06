import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer

st = SentenceTransformer("xlm-r-bert-base-nli-stsb-mean-tokens")
data = pd.read_csv("./comments.csv")

comments = data[['textClean', 'videoId']]

text = comments["textClean"].values.tolist()
labels = comments.index.to_list()
# encodage de chaque commentaire en un vecteur de R^768 ce qui nous permettra de faire une ACP
embs = st.encode(text)
pca = PCA(2).fit_transform(embs)

# Pour la légende des graphes, on identifie le numéro de video de chaque commentaire
dico_font_video = {}

for i, videoid in enumerate(comments.videoId.unique()):
    dico_font_video[videoid] = i

font = [dico_font_video[videoid] for videoid in comments.videoId]

# On réunit les commentaires par clusters (dans R^768), qu'on affiche sur l'ACP dans R^2
kmeans = KMeans(5, n_init=20, max_iter=3000).fit(embs)

center_indices = [
    int(np.argmin([np.sum((x - centroid) ** 2) for x in embs]))
    for centroid in kmeans.cluster_centers_]
# On récupère les commentaires les plus proches de chaque centroid
commentaires_representants = [comments.textClean[i] for i in center_indices]

file = open("./graphs/represent_comments.md", 'w', encoding='utf-8')
for i, texte in enumerate(commentaires_representants):
    line = f'{i + 1} : ' + texte + '  \n'
    file.write(line)
file.close()

# Différentes visualisation (répartition des clusters et des vidéos)
plt.subplots(figsize=(16, 8))

data = pd.DataFrame(np.array([pca[:, 0], pca[:, 1], font, kmeans.labels_]).transpose(),
                    columns=['x', 'y', 'font', 'label'])
data = data.sample(frac=1)

plt.subplot(121)
sns.scatterplot(data=data,
                x='x',
                y='y',
                hue='label',
                style='label',
                s=100,
                hue_norm=(0, 6),
                alpha=.8,
                palette='hsv',
                legend='full')
# Centroids mis en évidence
sns.scatterplot(x=[pca[i, 0] for i in center_indices],
                y=[pca[i, 1] for i in center_indices],
                style=[i for i in range(len(center_indices))],
                s=300,
                legend=False)
plt.title("ACP des commentaires + clustering")

plt.subplot(122)

sns.scatterplot(data=data,
                x='x',
                y='y',
                hue='font',
                hue_norm=(0, 23),
                s=50,
                palette='hsv',
                alpha=.5,
                legend='full')
plt.title("ACP des commentaires par video")

plt.savefig('./graphs/acp1.png', format='png')

# Calcul de l'enveloppe convexe pour avoir des affichages individuels par vidéo facile à comparer entre eux
hull = ConvexHull(pca)

fig, axs = plt.subplots(4, 5, figsize=(14, 10))
for i, ax in enumerate(np.array(axs).flatten()):
    sns.scatterplot(x=[pca[j, 0] for j in range(len(font)) if font[j] == i],
                    y=[pca[j, 1] for j in range(len(font)) if font[j] == i],
                    s=50,
                    ax=ax)
    for simplex in hull.simplices:
        ax.plot(pca[simplex, 0], pca[simplex, 1], 'c')
    ax.set_title(f'Video {i + 1}', fontsize=10)
    ax.axis('off')

plt.savefig('./graphs/acp_comparaison.png', format='png')

# Enveloppe convexe uniquement avec indexation pour étudier les commentaires à la frontière
fig, ax = plt.subplots()
for simplex in hull.simplices:
    plt.plot(pca[simplex, 0], pca[simplex, 1], 'c')
bound = np.array([pca[i] for i in hull.vertices])
plt.scatter(x=bound[:, 0], y=bound[:, 1], color='r')

for name, vect in zip(range(len(bound)), bound):
    plt.annotate(name + 1, vect)

plt.savefig('./graphs/acp_convex_hull.png', format='png')

file = open("./graphs/extreme_comments.md", 'w', encoding='utf-8')
for i, ind in enumerate(hull.vertices):
    line = f'{i + 1} : ' + text[ind] + '  \n'
    file.write(line)
file.close()


def find_remerciement(string):
    return ('merci' in string) or ('thank' in string) or ('thx' in string)


data = data.sort_index()  # On remet les commentaire dans l'ordre de leurs indices
remerciements = data.iloc[[i for i in range(len(data)) if find_remerciement(text[i])]]

pca_remerciements = np.array(remerciements[['x','y']])
hull_remerciements = ConvexHull(pca_remerciements)

sns.scatterplot(data=remerciements,
                x='x',
                y='y',
                s=200,
                alpha=.4,
                legend='full')
for simplex in hull.simplices:
    plt.plot(pca[simplex, 0], pca[simplex, 1], 'c')
for simplex in hull_remerciements.simplices:
    plt.plot(pca_remerciements[simplex, 0], pca_remerciements[simplex, 1], 'r')
plt.title("Commentaires de remerciement")
plt.savefig('./graphs/acp_remerciements.png', format='png')