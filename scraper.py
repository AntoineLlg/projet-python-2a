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

response = request.execute()

if __name__ == "__main__":
    print(response)
