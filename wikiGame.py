from bs4 import BeautifulSoup
import urllib.request
import dumper
from urllib.parse import unquote
from os import system, name
import re


# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def filter_div(tag):
    if tag.id == "mw-content-text":
        # and "infobox" not in tag.'class'
        return True


def filter_url(url):
    # certaine url ont deux // de suite, elle sont invalide, il faut les enlever
    if re.search('//', url):
        return False
    if "/w/index.php?" in url:
        return False
    if url.startswith("#"):
        return False
    if url.startswith("/wiki/Wikip"):
        return False
    if url.startswith("/wiki/Fichier"):  # semble stocker tous les fichiers jpg
        return False
    if url.startswith("http"):
        return False
    if url.startswith("/wiki/Portail"):
        return False
    if url.startswith("/wiki/Spécial"):
        return False
    if url.startswith("/wiki/Aide"):
        return False
    if url.startswith("/wiki/501c"):
        return False

    return True


if __name__ == '__main__':

    random_url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    # url = urllib.request.urlopen(random_url)
    urlTarget = urllib.request.urlopen(random_url)
    nbCoup = 0

    while url != urlTarget.url:
        array_link = []
        nbCoup += 1

        with urllib.request.urlopen(url) as response:

            soup = BeautifulSoup(response, 'html.parser')
            for link in soup.find_all("a"):

                if link.get('href') and filter_url(unquote(link.get('href'))):  # est-il valid ?
                    if link.get('href') not in array_link:  # est-il déjà présent dans le tableau
                        array_link.append(link.get('href'))
                        print("link   {}\t: {}".format(len(array_link) - 1, unquote(link.get('href'))))
        print("target is : ", unquote(urlTarget.url))
        print("Actual url is : ", unquote(response.url))
        while True:
            userInput = int(input("please choose a link by it's number : "))
            if len(array_link) > userInput:
                break
        if "://" in array_link[userInput] and "http" in array_link[userInput]:
            url = array_link[userInput]
        else:
            url = "https://fr.wikipedia.org" + array_link[userInput]
        print("url to go is {}".format(url))
        clear()

    print("YOU WIN!!")
    print("Nombre de coups utilisé :  ", nbCoup)
