from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
apikey = os.getenv('APIKEY')  # clé personnelle à configurer sur le site des API Google

youtube = build('youtube', "v3", developerKey=apikey)

# récupération d'informations à propos de la chaine YouTube DirtyBiology

request = youtube.channels().list(
    part='statistics',
    forUsername='dirtybiology'
)
general_statistics = request.execute()
channel_id = general_statistics['items'][0]['id']

request = youtube.search().list(
    part="id,snippet",
    channelId=channel_id,
    order='date',
    maxResults=20
)
response = request.execute()
video_ids = []
more_info = []
for item in response['items']:
    video_ids.append(item['id']['videoId'])
    more_info.append({'videoTitle': item['snippet']['title'], 'videoDate': item['snippet']['publishedAt']})
# Scraping des commentaires des vidéos cibles

comments_list = []

for videoId in video_ids:
    specific_info = more_info[video_ids.index(videoId)]
    # Requête pour obtenir jusqu'à 100 (maximum autorisé par l'API) commentaires sur une vidéo YouTube
    request = youtube.videos().list(
        part='statistics',
        id=videoId
    )
    response = request.execute()
    stats = response['items'][0]['statistics']
    stats.pop('favoriteCount')
    stats['videoLikeCount'] = stats.pop('likeCount')
    specific_info = {**stats, **specific_info}

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=videoId,
        maxResults=100,
        order='relevance'
    )
    response = request.execute()

    # Stockage des sorties dans une dataframe
    for item in response['items']:
        snippet = item['snippet']['topLevelComment']['snippet']
        snippet['authorChannelId'] = snippet['authorChannelId']['value']  # lissage
        snippet['commentLikeCount'] = snippet.pop('likeCount')
        comments_list.append({**snippet, **specific_info})

data = pd.DataFrame(comments_list)

# Stockage dans un fichier en dehors du script
data.to_csv(path_or_buf='./comments.csv',
            index=False)
