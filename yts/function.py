import requests
from requests.exceptions import HTTPError
from termcolor import colored, cprint
from prettytable import PrettyTable
from pathlib import Path
from queue import Queue
from threading import Thread
import os,re
import subprocess

ENDPOINT        = "https://yts.lt/api/v2/list_movies.json"
DETAIL          = "https://yts.lt/api/v2/movie_details.json"
LIMIT           = 15
DEFAULT_PARAM   = {' limit':LIMIT}

torrents_links = []

def requests_movies(query=False):
    parameter = {**DEFAULT_PARAM, **query} if query else DEFAULT_PARAM
    try:
        response = requests.get(ENDPOINT,params=parameter)
        return response.json()
    except HTTPError as http_error:
        print("[!] Http Error Occured : {}".format(http_error))
    except Exception as error:
        print("[!] Another Error Occured : {}".format(error))

def latest(query=False):
    cprint('[!] Requesting movies....', 'red', 'on_white')
    movies = requests_movies() if not query else requests_movies(query)
    res = format_view(movies)
    return res

def download_by_id(id):
    try:
        response = requests.get(DETAIL,params={'movie_id':id})
        res = response.json()
        cprint('[!] {}'.format(res["data"]["movie"]["title"]), 'red', 'on_white')
        n = 0
        for i in res["data"]["movie"]["torrents"] :
            cprint("[{}] {} {} {}".format(n,i["quality"],i["type"],i["size"]))
            n += 1

        quality = input(">> ")
        rs = res["data"]["movie"]["torrents"][int(quality)]["url"]
        r = requests.get(rs)
        filename = get_filename_from_cd(r.headers.get('content-disposition'))  
        with open(filename, 'wb') as f:
            f.write(r.content)

        cprint('[!] Downloading movies....{}'.format(res["data"]["movie"]["title"]), 'green', 'on_white')
        subprocess.call("aria2c \"{}\"".format(filename), shell=True)

    except HTTPError as http_error:
        print("[!] Http Error Occured : {}".format(http_error))

def format_view(movies):
    views = PrettyTable()
    views.field_names = ["ID","TITLE","YEAR","RATING","QUALITY","FORMAT","SIZE"]
    views.align["TITLE"] = "l"
    views.align["FORMAT"] = "r"
    views.align["SIZE"] = "r"
    try:
        if len(movies["data"]["movies"]) > 0 :
            for movie in movies["data"]["movies"]:
                title = (movie["title"][:50] + '..') if len(movie["title"]) > 50 else movie["title"]
                rating_color = 'red' if movie["rating"] <= 6 else 'green'
                torrents = movie["torrents"][1] if len( movie["torrents"]) > 1 else movie["torrents"][0]
                torrents_links.append(torrents["url"])
                properties = [
                    movie["id"],
                    title,
                    movie["year"],
                    colored(movie["rating"], rating_color),
                    torrents["quality"],
                    colored(torrents["type"],'green'),
                    colored(torrents["size"], 'yellow')
                ]
                views.add_row(properties)
            return views
        else:
            return False
    except Exception as error:
        return False

class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            directory, link = self.queue.get()
            try:
                download_torrents(directory, link)
            finally:
                self.queue.task_done()

def download_all_torrent():
    download_dir = setup_download_dir()
    queue = Queue()
    for x in range(8):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
        
    for link in torrents_links:
        queue.put((download_dir, link))

    queue.join()

def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0].replace('"','')

def download_torrents(directory, link):
    r = requests.get(link)
    filename = get_filename_from_cd(r.headers.get('content-disposition'))  
    download_path = directory / filename
    with open(download_path, 'wb') as f:
        f.write(r.content)

def setup_download_dir():
    download_dir = Path('torrents')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir