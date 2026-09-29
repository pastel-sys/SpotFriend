import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
from .models import User

#python C:\Users\Admin\Documents\CS50W\FinalProject\spot\services.py
load_dotenv()
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

def get_scrobbles(user):
    db_user = User.objects.get(id=1)
    last_uts_db = db_user.last_uts

    scrobbles_list = []
    scrobbles = {}
    lastfm_scrobbles_response = requests.get(f'https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={LASTFM_API_KEY}&format=json')
    for track in lastfm_scrobbles_response.json()["recenttracks"]["track"]:
        try: 
            scrobbles = {
                "artist": track["artist"]["#text"],
                "album": track["album"]["#text"],
                "image": track["image"],
                "song": track["name"],
                "uts": int(track["date"]["uts"]),
                "date": track["date"]["#text"]
            } 
            scrobbles_list.append(scrobbles)
            last_uts = int(track["date"]["uts"])
        except:
            continue

        if last_uts == last_uts_db: 
            return([])
        else:
            return(scrobbles_list)

    db_user.last_uts = last_uts
    db_user.save()
