import wikiGame
import unittest
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import unquote
import io
import sys


class MyTest(unittest.TestCase):

    
    def testFilterUrl(self):
        #Arrange
        url1 = "/wiki/Wikip/test/url"
        url2 = "/wiki/Fichier/test/url"
        url3 = "/test//url"
        url4 = "/test/url"

        #Act

        #Assert
        self.assertEqual(wikiGame.filter_url(url1), False)
        self.assertEqual(wikiGame.filter_url(url2), False)
        self.assertEqual(wikiGame.filter_url(url3), False)
        self.assertEqual(wikiGame.filter_url(url4), True)

    def testPrintAllLinkStoreHash(self):
        #Act
        with urllib.request.urlopen("https://fr.wikipedia.org/wiki/Universit%C3%A9_de_l%27Arkansas_%C3%A0_Little_Rock") as response:
            soup = BeautifulSoup(response, 'html.parser') 

        #Arrange
        arrayWanted = ['/wiki/%C3%89tats-Unis', '/wiki/Arkansas', '/wiki/1927', '/wiki/Universit%C3%A9_publique', '/wiki/Anglais_am%C3%A9ricain', '/wiki/Site_web', '/wiki/Little_Rock', '/wiki/Anglais', '/wiki/Universit%C3%A9', '/wiki/Trojans_d%27Arkansas_Little_Rock']
           
        #Assert
        self.assertEqual(wikiGame.print_all_link_store_hash(soup), arrayWanted)



    #Arrange
    random_url = "https://fr.wikipedia.org/wiki/A%C3%A9rodrome_de_Barra"
    url = "https://fr.wikipedia.org/wiki/A%C3%A9rodrome_de_Barra"
    urlTarget = urllib.request.urlopen(random_url)
    nbCoup =1

    def testCheckWin(self):
               
        #Act
        capturedOutput = io.StringIO()          
        sys.stdout = capturedOutput                
        wikiGame.WikiShell.check_win(self)                                 
        sys.stdout = sys.__stdout__                   
        stringReturn = str(capturedOutput.getvalue())

        #Assert
        self.assertEqual("YOU WIN!!\nnumber of turn :   1\n", stringReturn)

    def testDoShowscore(self):

        #Act
        capturedOutput = io.StringIO()          
        sys.stdout = capturedOutput                
        wikiGame.WikiShell.do_showscore(self, '')                          
        sys.stdout = sys.__stdout__                   
        stringReturn = str(capturedOutput.getvalue())

        #Assert
        self.assertEqual("1\n", stringReturn)