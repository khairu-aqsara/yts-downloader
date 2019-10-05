from termcolor import colored, cprint
from yts.function import latest,download_all_torrent,download_by_id
import os,time

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

def reset_screen():
    os.system('clear')
    signature()

def main_menu():
    reset_screen()
    cprint('YTS MOVIES DOWNLOADER', 'green', 'on_white')
    cprint("[a] View Latest Movies","yellow")
    cprint("[b] Search Movies","green")
    cprint("[c] Top 50 IMDB Movies","magenta")
    choice = input('>> [a/b/c] : ')
    
    if choice == 'a':
        movies = latest()
        reset_screen()
        if movies:
            submenu(movies)
        else:
            cprint("[!] No Movies found","red")
            cprint("[1] Any key to back","yellow")
            input(">> ")
            main_menu()
    elif choice == 'b':
        reset_screen()
        cprint('SEARCH YTS MOVIES', 'green', 'on_white')
        cprint("Title/Actor/Director","yellow")
        search = input(">> ")
        movie_to_search = {'query_term':search,'sort_by':'year'}
        movies = latest(movie_to_search)
        if movies:
            submenu(movies)
        else :
            cprint("[!] No Data Found","red","on_white")
    elif choice == 'c':
        reset_screen()
        cprint('TOP 50 IMDB MOVIES', 'green', 'on_white')
        movie_to_search = {'sort_by':'rating','limit':50}
        movies = latest(movie_to_search)
        if movies:
            submenu(movies)
        else :
            cprint("[!] No Data Found","red","on_white")


def submenu(movies):
    reset_screen()
    print(movies)
    cprint("[a] Download All Torrent File","yellow")
    cprint("[b] Download By Movies ID","yellow")
    cprint("[x] Back","yellow")
    key = input(">> ")
    if key == 'a':
        cprint('[+] Downloading Torrents {}'.format('.'*10), 'red', 'on_white')
        download_all_torrent()
        cprint('[+] Download Completed', 'green', 'on_white')
        time.sleep(2)
        main_menu()
    elif key == 'b':
        id = input("Movie ID : ")
        download_by_id(id)