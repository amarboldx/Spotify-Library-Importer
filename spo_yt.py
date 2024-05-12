import os
import json
import pandas as pd

from json.decoder import JSONDecodeError

from googleapiclient.errors import HttpError


from spotify import Spotify
from youtube import Youtube
from pytube import YouTube as YoutubeDL



youtube = Youtube('client_secrets/client_secret.json').google_auth_service()

sp = Spotify('client_secrets/creds.json').spotify_auth_service()
user = sp.current_user()
playlists = sp.current_user_playlists() #set global for methods to use




#Used for printing songs, since spotify doesnt allow over 100 iterations ffs
def save_songs(choice):
    playlist_songs = []
    limit = 100
    offset = 0
    ind = 0
    while True:
        songs = sp.playlist_items(playlists['items'][choice-1]['uri'],limit=limit, offset=offset)
        playlist_name = playlists['items'][choice-1]['name']
        for i, song in enumerate(songs['items']):
            artists = ", ".join([artist['name'] for artist in song['track']['artists']])
            song_name = song['track']['name']
            #link = yt_search(artists + " " + song_name)
            playlist_songs.append({'artists': artists, 'song_name': song_name}) #, 'url' : link
            ind += 1
        offset += limit
        
        with open('songs.json', 'w') as f:
            json.dump(playlist_songs, f, indent=4)

        if songs['next'] is None:
            break

def print_songs():
    with open('songs.json', 'r') as f:
        data = json.load(f)

    for index, song in enumerate(data, start=1):
        artists = song["artists"]
        song_name = song["song_name"]
        print(f"{index}. {artists} - {song_name}")

def get_ps_title_description(choice):
    tuple = (playlists['items'][choice-1]['name'], playlists['items'][choice-1]['description'])
    return tuple


def yt_search(search_term):
    try:
        response = youtube.search().list(
            part='snippet',
            q=search_term,
            maxResults=1,
            type='video'
        ).execute()
        video_id = response['items'][0]['id']['videoId']
        return video_id
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None
    except IndexError:
        print("No video found for the search term.")
        return None
    

def create_playlist(choice):
    try:
        my_playlists_request = youtube.playlists().list(
            part="snippet",
            maxResults=50,
            mine=True
        )
        my_playlists_response = my_playlists_request.execute()
        my_playlists = my_playlists_response.get("items", [])

        title, description = get_ps_title_description(choice)

        for playlist in my_playlists:
            if title == playlist['snippet']['title']:
                return playlist['id']  # return playlist early if it already exists, skips creation process

        body = {
            'snippet': {
                'title': title,
                'description': description
            },
            'status': {
                'privacyStatus': 'private'
            } 
        } 

        playlists_insert_response = youtube.playlists().insert(
            part='snippet,status',
            body=body
        ).execute()
        
        return playlists_insert_response['id']
    except HttpError as e:
        print(f'An error occurred: {e}')
        return None




def insert_to_playlist(video_id, playlist_id):
    try:
        request_body = {
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }

        response = youtube.playlistItems().insert(
            part='snippet',
            body=request_body
        ).execute()
    except HttpError as e:
        print(f'An error occurred: {e}')


def remove_dup_yt_ps(playlist_id):
    try:
        response = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50
        ).execute()
        playlistItems = response['items']
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()

            playlistItems.extend(response['items'])
            nextPageToken = response.get('nextPageToken')
        
        df_playlistItems = pd.DataFrame(playlistItems)
        df_contentDetails = df_playlistItems['contentDetails'].apply(pd.Series)

        for videoItem in df_playlistItems[df_contentDetails.duplicated()].iterrows():
            youtube.playlistItems().delete(id=videoItem[1]['id']).execute()
    except HttpError as e:
        print(f'An error occurred: {e}')


#Menu method used to list all playlist in user's library
def _list(ind):
    while True:
        print(("----------------------------"))

        for i, playlist in enumerate(playlists['items']):
            print(f"{i+1}. {playlist['name']}")
        print((f"{i+2}. Exit Section"))
        print(("----------------------------"))

        
        try:
            choice = int(input("Please choose a playlist: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        
        if(choice < 0 or choice >= i + 2):
            os.system('cls')
        if(choice >= 1 or choice <= i+1):
            break
    if(choice == i+2):
        return 0
    save_songs(choice)
    if(ind == 1):
        print_songs()
    elif(ind == 2):
        export_to_yt(choice)
    elif(ind == 3):
        youtube_dl()

def youtube_dl():
    with open('songs.json', "r") as file:
        data = json.load(file)
    for song in data:
        yt = YoutubeDL('https://www.youtube.com/watch?v=' + song['url'])
        stream = yt.streams.filter(only_audio=True).first()
        dl = stream.download('downloads/', skip_existing=True, max_retries=3) 
        base, ext = os.path.splitext(dl)
        new_file = base + '.mp3'
        os.rename(dl, new_file) 

    

def export_to_yt(choice):
    ps_id = create_playlist(choice)

    with open('songs.json', "r") as file:
        data = json.load(file)
    for song in data:
        insert_to_playlist(yt_search(song['artists'] + " " + song['song_name']), ps_id)
    remove_dup_yt_ps(ps_id)
            



#Main menu method
def menu():
    while True:
        print()
        print(f"Hello user : {user['display_name']}")
        print()

        print("----------------------------")
        print("1. List Playlists")
        print("2. Export To Youtube")
        print("3. Download Playlist Locally")
        print("4. Exit program")
        print(("----------------------------"))


        try:
            choice = int(input("Please choose a playlist: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

        match choice:
            case 1:
                os.system('cls')
                _list(1)
            case 2:
                os.system('cls')
                _list(2)

            case 3:
                os.system('cls')
                _list(3)
            case 4:
                break
            case _:
                print("Please choose from the menu")

menu()    #Start program
