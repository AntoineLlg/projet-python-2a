import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

data = pd.read_csv("comments.csv")

dico = {data.videoId.unique()[i]: 20 - i for i in range(len(data.videoId.unique()))}
data['videoId'] = data['videoId'].replace(to_replace=dico)

info_video = data.groupby('videoId')[['viewCount', 'commentCount', 'videoLikeCount', 'videoDate']].max()

info_video['ratioLike'] = info_video['videoLikeCount'] / info_video['viewCount']
info_video['ratioComment'] = info_video['commentCount'] / info_video['viewCount']

nbr_mois = lambda date: 25 - (int(date[5:7]) + 12 * int(date[3]))
info_video['Ancienneté'] = info_video.videoDate.apply(nbr_mois)

plt.style.use('seaborn')

fig, axs = plt.subplots(2, 2, figsize=(16, 10))

info_video.plot(y='ratioLike', ax=axs[0][0], color='r')
info_video.plot(y='ratioComment', ax=axs[0][0], color='b')
axs[0][0].axis([0, 20, 0, 1])
axs[0][0].set_xlabel("Identifiant de la vidéo")
axs[0][0].set_title("Part d'engagement du public")

info_video.plot(y='ratioLike', ax=axs[1][0], color='r')
info_video.plot(y='ratioComment', ax=axs[1][0], color='b')
axs[1][0].set_xlabel("Identifiant de la vidéo")
axs[1][0].set_title("Comparaison des proportions de like et commentaires")

info_video.plot(y='ratioComment', ax=axs[0][1], color='b')
axs[0][1].set_xlabel("Identifiant de la vidéo")
axs[0][1].set_title("Variation de l'engagement par commentaires")

slope, intercept, r_value, p_value, std_err = linregress(x=info_video.Ancienneté, y=info_video.ratioComment)

info_video.plot.scatter(x='Ancienneté', y='ratioComment', ax=axs[1][1])
axs[1][1].plot(info_video.Ancienneté, slope * info_video.Ancienneté + intercept, color='c')
axs[1][1].set_title("Regression linéaire de l'engagement en commentaires sur l'ancienneté")
axs[1][1].set_xlabel('Ancienneté de la vidéo')
axs[1][1].set_ylabel('Ratio de commentaires par vue')
plt.text(x=0.5, y=0.006, s=f"Slope = {slope:.2e}\nR-squared = {r_value ** 2:.2f} \nP-value = {p_value:.3f}")

plt.savefig('./graphs/description_videos.png', format='png')
