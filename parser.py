from bs4 import BeautifulSoup
import urllib.request
import string

# ----------------- FONCTION QUI PARSE L'INDEX HTML DE TOUTES LES LETTRES DE L'ALPHABET -------------------- #
def parseIndex(url) :
    #{
    # récupération du code source de la page html
    html = urllib.request.urlopen(url).read()
    # page html récupérée ci-dessus et mise au format 'beautiful soup'
    soup = BeautifulSoup(html, "html.parser")

    # récupération du tbody de la page html
    body = soup.table.tbody

    # récupération de tous les td de tbody qui ont la class='title'
    td = body.find_all(class_='title')
    listTd = []
    for child in td :
        listTd += child.find_all('a') # récupération de tous les 'a' de la liste des td

    print(str(len(listTd)))
    # parcourt de tous les 'a' récupérés
    for child in listTd :
        print(child.string + ' - ' + child['href']) #affiche le nom du manga et l'url de sa page
        # print() #affiche l'url vers la page du manga
#}
# ----------------------------------------------------------------------------------------------------------- #

def parseSerie(url) :
    

# ------------------------------------------------------------------------ #
#     Main     #

#url principale
indexSerie = 'https://www.manga-news.com/index.php/series/'


parseUrl(indexSerie + 'A')
exit(0)

# génération des url vers chaque lettre de l'alphabet
alphabet = list(string.ascii_uppercase) + [' ']
for letter in alphabet :
    # print(letter)
    urlSerie = indexSerie + letter
    # print(urlSerie)
    parseUrl(urlSerie)