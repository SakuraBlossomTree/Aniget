import os
import requests
import subprocess
from bs4 import BeautifulSoup
from pyfzf.pyfzf import FzfPrompt

os.system('clear' if os.name == 'posix' else 'cls')

fzf = FzfPrompt()

base_url = "https://myanimelist.net/"

anime_name = str(input("Enter your anime: ")) 

def search_anime(anime_name):
    
    anime_name = anime_name.replace(' ' , '+')

    search_endpoint = f"search/all?q={anime_name}&cat=all"

    search_url = base_url + search_endpoint

    return search_url

def get_animes(search_url):
    
    response = requests.get(search_url)

    soup = BeautifulSoup(response.content, "html.parser")

    animes_links = soup.find_all("a", href=lambda href: href and href.startswith("https://myanimelist.net/anime/"))

    titles = {
        "links": [],
        "titles": [],
    }

    for i, link in enumerate(animes_links, start=1):
        url = link["href"].strip()
        title = link.text.strip()
        if title == '':
            continue
        # print(url)
        # print(title)
        else:
            titles["links"].append(url)
            titles["titles"].append(title)


    return titles


search_url = search_anime(anime_name)
titles = get_animes(search_url)
print(titles)
selected_anime = fzf.prompt(titles["titles"])
print(selected_anime[0])
selected_anime = selected_anime[0]
if selected_anime[0]:
    title_index= titles["titles"].index(selected_anime)
    
    corresponding_link = titles["links"][title_index]

    print(f"You selected: {selected_anime}")
    print(f"Corresponding Link: {corresponding_link}")




