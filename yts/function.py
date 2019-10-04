import requests
from requests.exceptions import HTTPError
from termcolor import colored, cprint
from prettytable import PrettyTable

ENDPOINT        = "https://yts.lt/api/v2/list_movies.json"
LIMIT           = 15
DEFAULT_PARAM   = {' limit':LIMIT}

def requests_movies(query=False):
    parameter = {**DEFAULT_PARAM, **query} if query else DEFAULT_PARAM
    try:
        response = requests.get(ENDPOINT,params=parameter)
        return response.json()
    except HTTPError as http_error:
        print("[!] Http Error Occured : {http_error}")
    except Exception as error:
        print("[!] Another Error Occured : {error}")

def latest(query=False):
    signature()
    cprint('[!] Requesting movies....', 'red', 'on_white')
    movies = requests_movies() if not query else requests_movies(query)
    format_view(movies)
    menu()

def signature():
    print("""\
     __         .__  .__           __             .___      
    |  | ____ __|  | |__|         |  | ______   __| _/____  
    |  |/ /  |  \  | |  |  ______ |  |/ /  _ \ / __ |/ __ \ 
    |    <|  |  /  |_|  | /_____/ |    <  <_> ) /_/ \  ___/ 
    |__|_ \____/|____/__|         |__|_ \____/\____ |\___  >
        \/                            \/          \/    \/ 
    -----------------------------------wenkhairu@gmail.com---
        """)

def menu():
    cprint('[1] Download All Torrent File', 'yellow')
    cprint('[2] Download All Movies', 'green')
    cprint('[3] Download By ID', 'magenta')
    input(colored('[1] Your choise Juragan ? : '))

def format_view(movies):
    cprint('[!] Success', 'green', 'on_white')
    views = PrettyTable()
    views.field_names = ["ID","TITLE","YEAR","RATING","QUALITY","FORMAT","SIZE"]
    views.align["TITLE"] = "l"
    views.align["FORMAT"] = "r"
    views.align["SIZE"] = "r"
    if len(movies["data"]["movies"]) > 0 :
        for movie in movies["data"]["movies"]:
            title = (movie["title"][:50] + '..') if len(movie["title"]) > 50 else movie["title"]
            rating_color = 'red' if movie["rating"] <= 6 else 'green'
            properties = [
                movie["id"],
                title,
                movie["year"],
                colored(movie["rating"], rating_color),
                movie["torrents"][0]["quality"],
                colored(movie["torrents"][0]["type"],'green'),
                colored(movie["torrents"][0]["size"], 'yellow')
            ]
            views.add_row(properties)
        print(views)
    else:
        print("[!] Can't find any movies")