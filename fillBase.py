from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import sqlbase
from sqlbase import Auteur, Genre, Serie, Tome, Asso_SerieGenre, Dessinateur, Type

import getDatas
from getDatas import parseUrl

# ----------------------------------------------------------------------------------------------------------- #
#     Main     #

indexSerie = 'https://www.manga-news.com/index.php/series/' + 'A'
bibliotheque = {}
# génération des url vers chaque lettre de l'alphabet
# alphabet = list(string.ascii_uppercase) + [' ']
# for letter in alphabet :
#     # print(letter)
#     urlSerie = indexSerie + letter
#     # print(urlSerie)
#bibliotheque.update(parser.parseUrl(indexSerie))

for key in list(bibliotheque.keys()):
    print(key)

exit(0)