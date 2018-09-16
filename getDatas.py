from bs4 import BeautifulSoup
import urllib.request
import string
import pprint

# ----------------- FONCTION QUI PARSE L'INDEX HTML DE TOUTES LES LETTRES DE L'ALPHABET ET QUI RETOURNE LA LISTE DES SERIES -------------------- #
def parseUrl(url) :
#{
    # récupération du code source de la page html
    html = urllib.request.urlopen(url).read()
    # page html récupérée ci-dessus et mise au format 'beautiful soup'
    soup = BeautifulSoup(html, "html5lib")

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


# ----------------------------- FONCTION QUI PARSE LE CONTENU D'UN TOME ------------------------------------- #
# -------------- RECUPERATION DES INFOS D'UN TOME EN PARCOURANT LA LISTE LI DU UL "entryInfos" ------------ #
def parseTome(url_tome) :
#{
    # récupération du code source de la page html
    html = urllib.request.urlopen(url_tome).read()
    # page html récupérée ci-dessus et mise au format 'beautiful soup'
    # 'soup' contient tout le contenu html de la page.
    soup = BeautifulSoup(html, "html5lib")

    # récupération de la liste des li contenu dans le ul="entryInfos"
    # find_all retourne une liste de 1 seul car il n'y a qu'un seul "entryInfos" d'où le [0] pour éviter de faire un for sur un seul élément.
    # on applique à nouveau le find_all sur les balises ('li') pour récupère une liste qui contient tous les li (> 0 élément)
    listLi = soup.find_all(class_="entryInfos")[0].find_all('li')

    # on parcourt chaque li du tableau listLi récupéré ci-dessus que l'on a converti en type 'list' de pyhton
    # pour avoir un tableau mis sous forme de []
    for li in list(listLi) :
        # on récupère tous les enfants de type balise "<strong>" de chaque li. On enlève le récursive car il n'y a qu'un seul <strong> dans le li.
        childrens = li.findChildren('strong', recursive=False)
        # on transforme la liste 'childrens' en tableau [] python
        # on test chaque 1er élément de la liste "childrens" car dans ce cas là, findChildren retourne une liste qui a un seul élément dans chaque ligne ex:[<strong>]. S'il y avait eu plusieurs balises strong dans un li, on aurait eu [ <strong>, <strong>, <strong>] 
        # et chaque 1er élement de la liste 'contents' car 'contents' retourne une liste du contenu présent dans la balise strong (dans notre cas) et il n'y a qu'un seul contenu dans la balise strong.
        # si la valeur de contents == "Date de publication" 
        if(list(childrens)[0].contents[0] == "Date de publication") :
            # alors on récupère la valeur de l'attribut 'content' présent dans la balise <meta>
            datePublication = li.meta['content']

    # print("\nDate de publication : " + datePublication)

    # récupération du résumé
    resume = ""    
    for child in soup.find(id="summary").p.children :
        resume += str(child)
    resume = resume.replace('<br/>', '\n')
    # print("\nRésumé :  \n" + resume + "\n")

    # récupération du lien de l'image
    urlImage = soup.find(id="picinfo").a['href']
    # print("Url image : " + urlImage) 

    return datePublication, resume, urlImage
#}
# ----------------------------------------------------------------------------------------------------------- #


# ---------------------------- RECUPERATION DE LA LISTE DES TOMES DE LA SERIE ------------------------------- #
def recupTomesSerie(soup) : 
#{
    # récupération de la liste des tomes contenu dans "serieVolumes"
    tomes = soup.find(id="serieVolumes").find_all(class_="vols")

    # création d'une liste qui contient pour chaque élément l'url vers le tome, l'url vers l'image et le numéro du tome
    listTomes = []

    print("Volumes : ")
    for tome in tomes :
        urlTome = tome.a['href']
        urlImag = tome.a.img['src']
        idVolume = tome.find_all(class_='selection')[0].string
        print(idVolume + " lien : "+ urlTome + " image : " + urlImag)
        listTomes.append([urlTome, urlImag, idVolume])

    return listTomes
# }
# ----------------------------------------------------------------------------------------------------------- #


# -------------------------- RECUPERATION DU NOMBRE DE TOME EN FRANCE ET AU JAPON --------------------------- #
def recupTomesVFVO(soup) :
#{
    # récupération des span contenu dans "numberblock"  
    nbTomesVOVF = soup.find(id="numberblock").find_all("span")
    # création d'une map du style [Key, [NbTomes, Statut]]
    mapVOVF = {}
    
    # on parcourt tous les span
    for span in nbTomesVOVF :
        key = span.string
        # on teste si la clé est égale à "VF"
        if key == 'VF':
            # récupération du nb de tomes
            tomes = list(nbTomesVOVF)[0].contents[2].strip(' \t\r\n:')
            # récupération du statut de la série (en cours, terminé, en pause)
            status = list(nbTomesVOVF)[0].contents[3].string.strip(' \t\r\n:()')
            # insertion de la clé et des valeurs associées dans la map
            mapVOVF[key] = [tomes,status]
        # on teste si la clé est égale à "VO"
        if key == "VO":
            # récupération du nb de tomes
            tomes = list(nbTomesVOVF)[3].contents[1].contents[2].strip(' \t\r\n:')
            # récupération du statut de la série (en cours, terminé, en pause)
            status = list(nbTomesVOVF)[3].contents[1].contents[3].string.strip(' \t\r\n:()')
            # insertion de la clé et des valeurs associées dans la map
            mapVOVF[key] = [tomes, status]

    # # si on trouve 'VO' dans la map alors on affiche la clé et ses valeurs
    # if mapVOVF.get('VO') is not None:
    #     print(" Tomes VO = " + mapVOVF['VO'][0] + " " + mapVOVF['VO'][1])
        
    # # si on trouve 'VF' dans la map alors on affiche la clé et ses valeurs
    # if mapVOVF.get('VF') is not None:
    #     print(" Tomes VF = " + mapVOVF['VF'][0] + " " + mapVOVF['VF'][1])

    return mapVOVF
# } 
# ----------------------------------------------------------------------------------------------------------- #
    

# -------------- RECUPERATION DES INFOS DE LA SERIE EN PARCOURANT LA LISTE LI DU UL "entryInfos" ------------ #
def recupInfosSerie(soup) :
#{
    # récupération de la liste des li contenu dans le ul="entryInfos"
    # find_all retourne une liste de 1 seul car il n'y a qu'un seul "entryInfos" d'où le [0] pour éviter de faire un for sur un seul élément.
    # on applique à nouveau le find_all sur les balises ('li') pour récupère une liste qui contient tous les li (> 0 élément)
    listLi = soup.find_all(class_="entryInfos")[0].find_all('li')

    mapInfosSerie = {} #map <clé,valeur>
    infosInutiles = ["Illustration", "Code prix", "Code EAN"] #infos que je ne veux pas récupérer

    for li in listLi :
        # récupération de la clé
        key = li.strong.string.strip(' \t\n\r:')

        # if la clé fait partie des infos inutiles alors on passe au suivant
        if li.strong.string in infosInutiles :
            continue
        elif li.strong.string == "Origine" : # cas spécial pour Origine car il y a des <span>
            value = li.contents[1].string.strip(' \t\r\n:').replace(' ', '')
        elif li.strong.string == "Genre" : # cas spécial pour genre qui peut possèder plusieurs genre
            genres = ""
            for child in li.find_all('a') :
                genres += child.string.strip(' \t\r\n:') + ", "
            value = genres
        else : # récupération de value "par défaut"
            value = li.contents[2].string.strip(' \t\n\r:')

        # insertion de la clé et de la valeur dans la map
        mapInfosSerie[key] = value


    return mapInfosSerie
#}
# ----------------------------------------------------------------------------------------------------------- #


# --------------------------------- RECUPERATION DU CONTENU D'UNE SERIE ------------------------------------- #
def parseSerie(url) :
#{
    # récupération du code source de la page html
    html = urllib.request.urlopen(url).read()
    # page html récupérée ci-dessus et mise au format 'beautiful soup'
    soup = BeautifulSoup(html, "html5lib") 

    mapInfosSerie = recupInfosSerie(soup)
    print(" Infos Série : " + str(mapInfosSerie))


    mapVOVF = recupTomesVFVO(soup) 
    # si on trouve 'VO' dans la map alors on affiche la clé et ses valeurs
    if mapVOVF.get('VO') is not None:
        print(" Tomes VO = " + mapVOVF['VO'][0] + " " + mapVOVF['VO'][1])
        
    # si on trouve 'VF' dans la map alors on affiche la clé et ses valeurs
    if mapVOVF.get('VF') is not None:
        print(" Tomes VF = " + mapVOVF['VF'][0] + " " + mapVOVF['VF'][1])


    # récupération du résumé
    resume = ""    
    for child in soup.find(id="summary").p.children :
        resume += str(child)
    resume = resume.replace('<br/>', '\n')
    print("\nRésumé :  \n" + resume + "\n")

    listTomes = recupTomesSerie(soup)
    print("Liste tomes : " + str(listTomes))
    
    # for url in urlTomes :
    #     parseTome(url)
    datePublication, resume, urlImage = parseTome(listTomes[0][0])
    print("Date de publication du tome : " + datePublication)
    print("Résumé du tome : " + resume)
    print("Url de l'image du tome : " + urlImage)
#}
# ----------------------------------------------------------------------------------------------------------- #    




# ----------------------------------------------------------------------------------------------------------- #
#     Main     #

# url principale
indexSerie = 'https://www.manga-news.com/index.php/series/'
bibliotheque = {}

bibliotheque.update(parseUrl('https://www.manga-news.com/index.php/series/' + 'A'))

# # récupère une clé de la bibliothèque
# # transforme le type retourné par bibliotheque.keys() en type 'List'
key = list(bibliotheque.keys())[0]

# # récupération de la liste des séries
parseSerie(key)

exit(0)

# # génération des url vers chaque lettre de l'alphabet
# alphabet = list(string.ascii_uppercase) + [' ']
# for letter in alphabet :
#     # print(letter)
#     urlSerie = indexSerie + letter
#     # print(urlSerie)
#     bibliotheque.update(parseUrl(urlSerie))

# ----------------------------------------------------------------------------------------------------------- #