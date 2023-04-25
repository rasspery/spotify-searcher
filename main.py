import base64
from requests import post, get
from colorama import Fore, Style
import json

URL = "https://accounts.spotify.com/api/token"
CLIENT_ID = ""
CLIENT_SECRET = ""

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
    }

    result = post(url=URL, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {
        "Authorization": "Bearer " + token
    }

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists...")
        return None
    else:
        return json_result[0]

def search_track(token, track_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"][0]
    if len(json_result) == 0:
        print("No track with this name exists...")
        return None
    else:
        return json_result

def get_songs_by_artist(token, artist_id, country_code):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country_code}"
    headers = get_auth_header(token)
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def get_track(token, track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)
    result = get(url=url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


TOKEN = get_token()

print(Fore.BLACK + Style.BRIGHT + "=========================================")
print(Fore.BLUE + Style.BRIGHT + "Welcome to Spotify Searcher Version 1.0.0")
print(Fore.BLACK + Style.BRIGHT + "=========================================")
print(Fore.GREEN + Style.BRIGHT + "------------- Search Menu -------------")
print(Fore.RED + Style.BRIGHT + "Enter 1" + Style.RESET_ALL +  " - Fetch an artist's top tracks")
print(Fore.RED + Style.BRIGHT + "Enter 2" + Style.RESET_ALL +  " - Fetch an artist's albums")
print(Fore.RED + Style.BRIGHT + "Enter 3" + Style.RESET_ALL +  " - Search a track")
task = int(input(Fore.RED + Style.BRIGHT + "Enter your choice's index: "))
if task == 1:
        print(Fore.BLACK + Style.BRIGHT + "-----------------------------------------")
        artist_name = input(Style.RESET_ALL + "Enter an artist's name[Ex: AC/DC]: ")
        country_code = input(Style.RESET_ALL + "Enter a country's code[Ex: IN]: ")
        if len(country_code) < 2:
                print(f"\n{country_code} is not a valid country code, please try again!")
                quit()
        else:
                result = search_artist(TOKEN, artist_name)
                artist_id = result["id"]
                songs = get_songs_by_artist(TOKEN, artist_id, country_code)
                print(Fore.BLACK + Style.BRIGHT + "-----------------------------------------")
                print(Fore.RED + f"{result['name']}'s top song(s) in {country_code} are:")
                for i, song in enumerate(songs):
                        print(Style.RESET_ALL + f"{i + 1}. {song['name']}")

elif task == 2:
        print(Fore.BLACK + Style.BRIGHT + "-----------------------------------------")
        artist_name = input(Style.RESET_ALL + "Enter an artist's name[Ex: AC/DC]: ")
        result = search_artist(TOKEN, artist_name)
        artist_id = result["id"]
        albums = get_albums_by_artist(TOKEN, artist_id)
        print(Fore.BLACK + Style.BRIGHT + "-----------------------------------------")
        print(Fore.RED + f"{result['name']}'s top album(s) are:")
        for album in albums:
                print(Fore.CYAN + Style.BRIGHT + "Album Name: " + Style.RESET_ALL + f"{album['name']}")
                print(Fore.CYAN + Style.BRIGHT + "Release Date: " + Style.RESET_ALL + f"{album['release_date']}")
                print(Fore.CYAN + Style.BRIGHT + "No. of tracks: " + Style.RESET_ALL +  f"{album['total_tracks']}")
                print(Style.RESET_ALL + "=============================================")
elif task == 3:
        print(Fore.BLACK + Style.BRIGHT + "-----------------------------------------")
        track_name = input(Style.RESET_ALL + "Enter the track's name[Ex: Doin' Time]: ")
        result = search_track(TOKEN, track_name)
        track_id = result["id"]
        track = get_track(TOKEN, track_id)
        
        name = track["name"]
        artst = track["artists"]
        dur = track["duration_ms"]
        duration = round(dur / 60000, 2)
        explicity = track["explicit"]

        print(Fore.BLACK + Style.BRIGHT + "-----------------------------------------")
        print(Fore.RED + "Here's the track you are searching for: ")
        print(Fore.CYAN + Style.BRIGHT + "Name: " + Style.RESET_ALL + name)
        for i in range(0, len(artst)):
                artist = artst[i]["name"]
                print(Fore.CYAN + Style.BRIGHT + "Artist(s): " + Style.RESET_ALL + artist)
        print(Fore.CYAN + Style.BRIGHT + "Duration: " + Style.RESET_ALL + "~" + str(duration) + " minutes")
        print(Fore.CYAN + Style.BRIGHT + "Is Explicit?: " + Style.RESET_ALL + str(explicity))
else:
        print(f"\n{task} is not a valid index, please try again!")
        quit()