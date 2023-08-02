import os
import requests
import subprocess
from bs4 import BeautifulSoup

os.system('clear' if os.name == 'posix' else 'cls')

anime_name = str(input("Enter what anime you want to watch: "))

def download_anime(anime_name):

    search_query = anime_name.replace(' ' , '+')

    base_url = "https://animetosho.org/"

    search_url = f"search?q={search_query}"

    final_url = base_url+search_url

    print(final_url)

    response = requests.get(final_url)

    soup = BeautifulSoup(response.content , "html.parser")

    links = soup.find_all("a" , href=lambda href: href and href.startswith("https://animetosho.org/view/"))

    # print(links)
    
    print("-------------------------- These are your searched anime ---------------------------------------")

    for i, link in enumerate(links , start=1):

        url = link["href"]

        title = link.text

        print(f"{i}. Title: {title}")

        print(f"     URL: {url}")

        print()

    choice = int(input("Enter the number of the anime to download the torrent: "))

    if choice >= 0 and choice <= len(links):

        selected_link = links[choice - 1]

        selected_url = selected_link["href"]

        torrent_links_response = requests.get(selected_url)

        torrent_soup = BeautifulSoup(torrent_links_response.content , "html.parser")

        torrent_links = torrent_soup.find_all("a", href=lambda href: href and href.startswith("https://animetosho.org/storage/torrent/"))
        
        torrents = [torrent["href"] for torrent in torrent_links]

        if torrents:
            
            response = requests.get(torrents[0])
            
            if response.status_code == 200:
            
                with open(f"./anime/{anime_name}.torrent", "wb") as f:
                
                    f.write(response.content)
                
                print("File downloaded successfully")
            
            else:
                
                print("Failed to download the file.")
            
        else: 

            print("No torrents avaiable for this anime")

    links = ""

def extractor(file_path):

    file_path = anime_name

    print(file_path)

    subprocess.run(["aria2c", "-x8" , f"./anime/{file_path}.torrent", "-d" , "./anime/"])

download_anime(anime_name)

extractor(anime_name)
