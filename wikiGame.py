from __future__ import print_function, unicode_literals
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import unquote, quote
from os import system, name
import re
from PyInquirer import prompt

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def filter_url(url):
    exclude_url = (
    "/wiki/Wikip", "/wiki/Fichier", "http", "/wiki/Portail", "/wiki/Spécial", "/wiki/Aide", "/wiki/501c", "#")
    if url.startswith(exclude_url):
        return False


    if "/w/index.php?" in url:
        return False

    return True


def print_all_link_store_hash(soup):
    local_array_link = set()

    for div in soup.find_all("div", {"class": "mw-parser-output"}):
        for link in div.find_all("a"):
            if link.get('href') and filter_url(unquote(link.get('href'))):  # Le lien est-il valide ?
                local_array_link.add(unquote(link.get('href')))

    return local_array_link


def get_question(array_link, url_target, actual_url):
    message_to_send = 'which Link do you want to use ? target is : ' + url_target + ' actual url is : ' + actual_url
    questions = [
        {
            'type': 'list',
            'name': 'link_user',
            'message': message_to_send,
            'choices': array_link,
        }
    ]
    return questions


if __name__ == '__main__':

    random_url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    urlTarget = urllib.request.urlopen(random_url)
    nbCoup = 0
    clear()

    while url != urlTarget.url:
        nbCoup += 1

        with urllib.request.urlopen(url) as response:
            soup = BeautifulSoup(response, 'html.parser')
            array_link = print_all_link_store_hash(soup)

        answers = prompt(get_question(array_link, unquote(urlTarget.url), unquote(response.url)))

        url = "https://fr.wikipedia.org" + quote(answers.get('link_user'))
        clear()

    print("YOU WIN!!")
    print("Nombre de coups utilisé :  ", nbCoup)
