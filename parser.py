from bs4 import BeautifulSoup
import urllib.request
import string
import pprint

# ----------------- FONCTION QUI PARSE L'INDEX HTML DE TOUTES LES LETTRES DE L'ALPHABET -------------------- #
def parseUrl(url) :
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

    # parcourt de tous les 'a' récupérés et les stocke dans une map
    mapSerie = {}
    for child in listTd :
        # print(child.string + ' - ' + child['href']) #affiche le nom du manga et l'url de sa page
        mapSerie[child['href']] = child.string.strip(' \t\n\r')

    return mapSerie
#}
# ----------------------------------------------------------------------------------------------------------- #

# -------------- RECUPERATION DES INFOS DE LA SERIE EN PARCOURANT LA LISTE LI DU UL "entryInfos" ------------ #
def recupInfosSerie(listLi) :
#{
    # première ligne de la liste qui contient les li (converti en liste)
    # on récupère le deuxième éléments du contenu de ce li sur lequel on enlève certains caractères spéciaux
    titreVO = list(listLi)[0].contents[2].strip(' \t\r\n:')
    print("Titre VO : " + str(titreVO))

    titreTraduit = list(listLi)[1].contents[2].strip(' \t\r\n:')
    print("Titre traduit :" + str(titreTraduit))

    dessinateur = list(listLi)[2].contents[2].string.strip(' \t\r\n:')
    print("Dessinateur : " + str(dessinateur))

    scenariste = list(listLi)[3].contents[2].string.strip(' \t\r\n:')
    print("Scénariste : " + str(scenariste))

    editeurVF = list(listLi)[4].contents[2].string.strip(' \t\r\n:')
    print("Editeur VF : " + str(editeurVF))

    typeManga = list(listLi)[6].contents[2].string.strip(' \t\r\n:')
    print("Type : " + str(typeManga))

    genres = ""
    for child in list(listLi)[7].find_all('a') :
        genres += child.string.strip(' \t\r\n:') + ", "
    print("Genre : " + str(genres))

    editeurVO = list(listLi)[8].contents[2].string.strip(' \t\r\n:')
    print("Editeur VO : " + str(editeurVO))

    origine = list(listLi)[11].contents[1].string.strip(' \t\r\n:').replace(' ', '')
    print("Origine : " + str(origine))
#}
# ----------------------------------------------------------------------------------------------------------- #

# ----------------------------- FONCTION QUI PARSE LE CONTENU D'UNE SERIE ----------------------------------- #
def parseSerie(url) :
#{
    # récupération du code source de la page html
    html = urllib.request.urlopen(url).read()
    # page html récupérée ci-dessus et mise au format 'beautiful soup'
    soup = BeautifulSoup(html, "html.parser") 

    # récupération de la liste des li contenu dans le ul="entryInfos"
    # find_all retourne une liste de 1 seul car il n'y a qu'un seul "entryInfos" d'où le [0] pour éviter de faire un for sur un seul élément.
    # on applique à nouveau le find_all sur les balises ('li') pour récupère une liste qui contient tous les li (> 0 élément)
    listLi = soup.find_all(class_="entryInfos")[0].find_all('li')

    recupInfosSerie(listLi)
#}
# ----------------------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------------------- #
#     Main     #

#url principale
indexSerie = 'https://www.manga-news.com/index.php/series/'
bibliotheque = {}

bibliotheque.update(parseUrl('https://www.manga-news.com/index.php/series/' + 'A'))

#récupère une clé de la bibliothèque
#transforme le type retourné par bibliotheque.keys() en type 'List'
key = list(bibliotheque.keys())[0]
# print(key)

parseSerie(key)

exit(0)

# génération des url vers chaque lettre de l'alphabet
alphabet = list(string.ascii_uppercase) + [' ']
for letter in alphabet :
    # print(letter)
    urlSerie = indexSerie + letter
    # print(urlSerie)
    bibliotheque.update(parseUrl(urlSerie))

# ----------------------------------------------------------------------------------------------------------- #