import urllib.request
from urllib.parse import unquote
from os import system, name
import sys
import re
import cmd
from bs4 import BeautifulSoup

'''Docstring very good'''
# define our clear function
def clear():
    """Clear screen for linux or windows"""
    # for windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def filter_url(url):

    exclude_url = (
        "/wiki/Wikip", "/wiki/Fichier", "http", "/wiki/Portail",
        "/wiki/Spécial", "/wiki/Aide", "/wiki/501c", "#")
    if url.startswith(exclude_url):
        return False

    # j'utilise des regex pour éviter les problèmes
    # d'encodage des accent dans les noms des catégories
    # (je ne sais pas ce que ca donnera dans d'autre langue par contre)
    if re.search('^/wiki/Cat.gorie:', url):
        return False
    if re.search('^/wiki/Discussion:', url):
        return False
    if re.search('^/wiki/Mod.le:', url):
        return False
    if re.search('^/wiki/Projet:', url):
        return False

    # certaine url ont deux // de suite, elles sont invalide, il faut les enlever
    if re.search('//', url):
        return False
    if "/w/index.php?" in url:
        return False

    return True


def print_all_link_store_hash(soup):
    array_link = []
    for div in soup.find_all("main", {"id": "content"}):
        for link in div.find_all("a"):
            if link.get('href') and filter_url(unquote(link.get('href'))):  # est-il valid ?
                if link.get('href') not in array_link:  # est-il déjà présent dans le tableau
                    array_link.append(link.get('href'))
                    print("link   {}\t: {}".format(len(array_link) - 1, unquote(link.get_text())))

    return array_link


class WikiShell(cmd.Cmd):
    random_url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"

    urlTarget = urllib.request.urlopen(random_url)
    nb_coup = 0
    array_link = []
    history = []

    intro = 'Welcome to the wiki game. Type help or ? to list commands.\n'
    prompt = '(wikiGame) '
    file = None

    def __init__(self):
        super().__init__()
        self.make_soup()

    def do_print(self, arg):
        """print again every possibility to select"""
        # this is not an optimized function : we call back http server
        # instead of putting data in a cache.
        # to add a cache we should completly change array_link format to store
        # link and text from an href, witch would be bothersome
        self.make_soup()

    def do_showscore(self, args):
        """show actual score"""
        print(self.nb_coup)

    def do_exit(self, arg):
        """print history and exit"""
        self.do_history('')
        sys.exit(0)

    def do_history(self, args):
        """print every link used up until now"""
        print("history is : ")
        print(*self.history, sep="\n")

    def default(self, arg):
        """default action is to take the number as the next link. if not a number, print help"""
        if arg.isdigit():
            self.do_number(arg)
        else:
            print("please use one of the defined command, or use a number to navigate between link")
            self.do_help('')

    def do_cancel(self, arg):
        """rollback last link used, but keep number of turn as is"""
        url = self.history[-1]
        self.history.pop()

    def do_number(self, link_number):
        """use link number x (given in parameter)"""
        if not link_number.isdigit or len(self.array_link) < int(link_number):
            self.do_print('')
            print(link_number + " is not valid, please select a number in the list")
            return

        self.url = "https://fr.wikipedia.org" + self.array_link[int(link_number)]
        self.history.append(self.url)
        self.nb_coup += 1
        self.check_win()
        print("url to go is {}".format(self.url))
        self.make_soup()

    def make_soup(self):
        with urllib.request.urlopen(self.url) as response:
            soup = BeautifulSoup(response, 'html.parser')
            self.array_link = print_all_link_store_hash(soup)

        print("target is : ", unquote(self.urlTarget.url))
        print("Actual url is : ", unquote(response.url))

    def check_win(self):
        if self.url == self.urlTarget.url:
            print("YOU WIN!!")
            print("number of turn :  ", self.nb_coup)
            sys.exit(0)


if __name__ == '__main__':
    WikiShell().cmdloop()
