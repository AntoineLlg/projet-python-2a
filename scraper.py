from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv('APIKEY')

youtube = build('youtube', "v3", developerKey=apikey)

request = youtube.channels().list(
    part='statistics',
    forUsername='dirtybiology'
)

request = youtube.search().list(
    part="snippet",
    eventType="completed",
    q="dirtybiology",
    type='video',
    maxResults=3
)
response = request.execute()

if __name__ == "__main__":
    for item in response['items']:
        print("\n", item['id']
              , item['snippet'])
