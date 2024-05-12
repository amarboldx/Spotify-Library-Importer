# Spotify-Library-Importer

## Set Up

This project uses client secrets from both Google's Oauth2.0 and Spotify's Client secret and Client ID.

set Spotify Client info to environment variables i.e:

If you're on Windows:

$env:SPOTIPY_CLIENT_ID=  
$env:SPOTIPY_CLIENT_SECRET=  
$env:SPOTIPY_REDIRECT_URI=  
$env:SPOTIFY_USER_ID=  

or if you're on LINUX

set SPOTIPY_CLIENT_ID=  
set SPOTIPY_CLIENT_SECRET=  
set SPOTIPY_REDIRECT_URI=  
set SPOTIFY_USER_ID=  


Set your Google Oauth2.0 client secret by uploading your JSON file to client_secret directory and naming it client_secret.json  

## How to run  

To Run the project, you must the activate the virtual environment by running this command:  

```
bin\venv\Scripts\activate  
```

And to run the project:  

```
python.exe spo_yt.py  
```
