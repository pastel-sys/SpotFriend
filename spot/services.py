import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
from .models import User, Album, Genre, Artist, Track
from colorthief import ColorThief
import io

load_dotenv()
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

# List of words to be aware of when searching for genres of music
no_tags = ["All", "seen live", "favorites", "favourite", "english", "spanish", "español", "french"]

def get_album_tracks(album):
    """Get all the tracks of an album"""
    tracks = Track.objects.filter(album=album)
    return tracks

def register_genre(genre):
    """Register the genre from a album into the database"""
    if genre in no_tags:
       return False
    else:
       if not(Genre.objects.filter(name=genre).exists()):
           genre = Genre.objects.create(name=genre)
           return True
       else:
           return True

def register_tracks(tracks, album_name):
    """Register the tracks from an album into the database"""
    if not(Track.objects.filter(name=tracks).exists()):
        for track in tracks:
            Track.objects.create(name=track["name"], album=Album.objects.get(name=album_name), duration=track["duration"], track_position=track["@attr"]["rank"])
        return True 
    else:
        return False

def colors_palette(album_img):
    """Turns the url data into a file object and then with ColorThief makes a color palette""" 
    image = requests.get(album_img) 
    color_thief = io.BytesIO(image.content)

    color = ColorThief(color_thief)
    palette = color.get_palette(color_count=3, quality=1)
    return palette

def register_favorite_albums(user):
    """Register the 10 favorites album of the user"""
    topalbums_params = {
        "method": "user.gettopalbums",
        "user": f"{user.lastfm_username}",
        "limit": "10",
        "api_key": LASTFM_API_KEY,
        "format": "json"
    }
    
    response_albums = requests.get("https://ws.audioscrobbler.com/2.0/", params=topalbums_params) 
    # Iterate through the response of the user data from lastFM to save it to our database
    for album in response_albums.json()["topalbums"]["album"]:
        artist = album["artist"]["name"]
        album_name = album["name"]
        Album_mbid = album["mbid"]
        Album_Image = album["image"][3]["#text"]
    
        if Artist.objects.filter(name=artist).exists():
            None
        else: 
            artist_params = {
                "method": "artist.gettoptags",
                "artist": artist,
                "limit": "10",
                "api_key": LASTFM_API_KEY,
                "format": "json",
            }
                
            response_artist = (requests.get("https://ws.audioscrobbler.com/2.0/", params=artist_params)).json()

            # Create a new artist 
            new_artist = Artist.objects.create(name=artist, tags_fetched=True)
            tag = 0
            for i in range(3): # only 3 tags per artist 
                new_genre = response_artist["toptags"]["tag"][tag]["name"]
                if register_genre(new_genre) == False:
                    tag += 1
                else: 
                    new_artist.tags.add(Genre.objects.get(name=new_genre))
                    new_artist.save()
                    tag += 1

        if Album.objects.filter(name=album_name).exists():
            None
        else: 
            album_params = {
                "method": "album.getInfo",
                "artist": artist,
                "album": album_name,
                "username": f"{user.lastfm_username}",
                "api_key": LASTFM_API_KEY,
                "format": "json",
            }

            response_album_info = (requests.get("https://ws.audioscrobbler.com/2.0/", params=album_params)).json()
            if Album_mbid:
                musicbrainz_query = (requests.get(f"https://musicbrainz.org/ws/2/release-group/?query=reid:{Album_mbid}&artistname={artist}&releasegroup={album_name}&fmt=json")).json()
                
            album_release = None
            album_principal_tag = ""
            try: # Store the realese date and a tag if it have
                if Album_mbid:
                    album_principal_tag = musicbrainz_query["release-groups"][0]["tags"][0]["name"]
                    if register_genre(album_principal_tag) == False:
                        album_principal_tag = ""
                    album_release = musicbrainz_query["release-groups"][0]["first-release-date"][0:4]
            except:
                None

            if Album.objects.filter(name=album_name).exists():
                None
            else: # Create and stores the album itself
                palette = colors_palette(response_album_info["album"]["image"][3]["#text"])

                if album_principal_tag:
                    new_album = Album.objects.create(name=album_name, artist=Artist.objects.get(name=f"{artist}"), cover=response_album_info["album"]["image"][3]["#text"], release_year=album_release, color_palette=palette)
                    new_album.genres.add(Genre.objects.get(name=album_principal_tag))
                    new_album.save()
                else:
                    new_album = Album.objects.create(name=album_name, artist=Artist.objects.get(name=f"{artist}"), cover=response_album_info["album"]["image"][3]["#text"], release_year=album_release, color_palette=palette)
                
                user_falbums = User.objects.get(username=user)
                user_falbums.favorite_albums.add(new_album)
                register_tracks(response_album_info["album"]["tracks"]["track"], album_name)


            
                

                
