from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET= ""
# fill your details
REDIRECT_URL = "http://localhost:8888/callback" 
# Set this redirect URL inside your Spotify account

titles = []

def get_songs(year):
    global titles
    url = "https://www.billboard.com/charts/hot-100/" + date 

    response = requests.get(url=url)
    contents = response.text
    soup = BeautifulSoup(contents, "html.parser")

    titles = soup.find_all(name="h3", class_="a-no-trucate")

    # top100 = []
    # top100 = [title.getText().strip() for title in titles]
    # print(top100)
    # return top100

def make_playlist(date):
    sp = spotipy.Spotify(
        auth_manager= SpotifyOAuth(
            scope= "user-library-read playlist-modify-private",
            redirect_uri= REDIRECT_URL,
            client_id= SPOTIFY_CLIENT_ID,
            client_secret= SPOTIFY_CLIENT_SECRET,
            show_dialog= False,
            cache_path= "token.txt"
        )
    )

    user_id = sp.current_user()["id"]
    # print(user_id)

    urls = [sp.search(title)['tracks']['items'][0]['uri'] for title in titles]
    # print(urls)
    PLAYLIST_ID = sp.user_playlist_create(
            user= user_id, 
            public=False,
            name=f"{date} BillBoard-100"
            )['id']

    sp.user_playlist_add_tracks(playlist_id=PLAYLIST_ID,
                                tracks=urls,
                                user= user_id
                                )

date = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD:")

songs = get_songs(date)
make_playlist(date)
