import os
import requests
import re
import subprocess
from bs4 import BeautifulSoup
from pyfzf.pyfzf import FzfPrompt

os.system('clear' if os.name == 'posix' else 'cls')

fzf = FzfPrompt()

base_url = "https://myanimelist.net/"

tosho_url = "https://animetosho.org/" 



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

def _get_span_text(page, key, typing, bypass_link=False):
    for span in page:
        if span.get_text() == key:
            first_link = span.parent.a
            if first_link and not bypass_link:
                if typing == str:
                    return first_link.text
                if typing == list:
                    res = [link.get_text().strip() for link in span.parent.findChildren("a")]
                    if "add some" in res:
                        res.remove("add some")
                    return res
            else:
                results = span.parent.findChildren(text=True, recursive=True)
                result = results[results.index(key) + 1].strip()
                if result == "Unknown":
                    return None
                else:
                    if typing == int:
                        num = re.sub("[^0-9]", "", result)
                        if num:
                            return int(num)
                        else:
                            return None
                    if typing == str:
                        return result
                    if typing == list:
                        return [element.strip() for element in result.split(",")]
    if typing == list:
        return []
    return None

search_url = search_anime(anime_name)
titles = get_animes(search_url)

selected_anime = fzf.prompt(titles["titles"])
selected_anime = selected_anime[0]

if selected_anime:
    title_index = titles["titles"].index(selected_anime)
    corresponding_link = titles["links"][title_index]
    
    print(f"You selected: {selected_anime}")
    print(f"Corresponding Link: {corresponding_link}")

    # Fetch and parse the selected anime's page
    response = requests.get(corresponding_link)
    soup = BeautifulSoup(response.content, "html.parser")

    # Example usage of _get_span_text function
    # Adjust 'key' and 'typing' as needed based on what you're looking for on the page
   
    global episodes

    episodes = _get_span_text(soup.find_all("span"), "Episodes:", str)
    # print(f": {episodes}")

def print_episodes(episodes):
    
    start = 1

    global episode_list

    episode_list = []

    episodes = int(episodes)

    for i in range(start , episodes + 1):
        
        episode_list.append(i)

    return episode_list

# Search for anime


# Display titles and let user select one
print(titles)

print_episodes(episodes)

print(episode_list)
selected_episode = fzf.prompt(episode_list)
# print(selected_episode[0])
selected_episode = selected_episode[0]

search_query = selected_anime + " " + selected_episode 

search_url = f"search?q={search_query}"

final_url = tosho_url+search_url

response = requests.get(final_url)

soup = BeautifulSoup(response.content, "html.parser")

links = soup.find_all("a" , href=lambda href: href and href.startswith("https://animetosho.org/view/"))

selected_link = links[0]

print(selected_link)

selected_url = selected_link["href"]

torrent_links_response = requests.get(selected_url)

torrent_soup = BeautifulSoup(torrent_links_response.content , "html.parser")

torrent_links = torrent_soup.find_all("a", href=lambda href: href and href.startswith("https://animetosho.org/storage/torrent/"))

torrents = [torrent["href"] for torrent in torrent_links]

if torrents:

    response = requests.get(torrents[0])

    if response.status_code == 200:

        with open(f"./anime/{selected_anime}.torrent", "wb") as f:

            f.write(response.content)

        print("File downloaded successfully")

    else:

        print("Failed to download the file.")

else:

    print("No torrents avaiable for this anime")

links = ""


# search_url = search_anime(anime_name)
# titles = get_animes(search_url)
# print(titles)
# selected_anime = fzf.prompt(titles["titles"])
# print(selected_anime[0])
# selected_anime = selected_anime[0]
# if selected_anime[0]:
#     title_index= titles["titles"].index(selected_anime)
#     
#     corresponding_link = titles["links"][title_index]
#
#     print(f"You selected: {selected_anime}")
#     print(f"Corresponding Link: {corresponding_link}")
#
# selected_anime_url = corresponding_link
