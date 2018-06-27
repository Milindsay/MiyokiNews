from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import sqlbase
from sqlbase import Auteur, Genre, Serie, Tome, Asso_SerieGenre, Dessinateur, Type

#connection à la base
engine = create_engine('mysql://root:@localhost/miyokinews?charset=utf8', encoding="utf-8")
iengine = inspect(engine)
connection = engine.connect()

# use _SessionFactory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)
session = _SessionFactory()

tables = iengine.get_table_names()

#Si la table 'auteur' existe déjà alors on ne la créée pas sinon oui 
if Auteur.__tablename__ in tables:
    print("found Auteur")
else:
    Auteur.__table__.create(engine)


if Genre.__tablename__ in tables:
    print("found Genre")
else:
    Genre.__table__.create(engine)

    
if Type.__tablename__ in tables:
    print("found Type")
else:
    Type.__table__.create(engine)


if Tome.__tablename__ in tables:
    print("found Tome")
else:
    Tome.__table__.create(engine)


if Serie.__tablename__ in tables:
    print("found Serie")
else:
    Serie.__table__.create(engine)


if Asso_SerieGenre.__tablename__ in tables:
    print("found Asso_SerieGenre")
else:
    Asso_SerieGenre.__table__.create(engine)
    

if Dessinateur.__tablename__ in tables:
    print("found Dessinateur")
else:
    Dessinateur.__table__.create(engine)


#Tests insertion BDD
a = Auteur()
a.nom = "yukiru sugisaki" 
session.add(a)

d = Dessinateur(nom="yukiru sugisaki")
session.add(d)

g1 = Genre(nom="Aventure")
session.add(g1)
g2 = Genre(nom="SF")
session.add(g2)

t = Type(nom="Shojo")
session.add(t)

session.flush()

s = Serie()
s.titre = "Lagoon engine"
#s.titre_VO = "ラグーンエンジン"
s.nb_VO = 7
s.nb_VF = 7
s.origine = "Japon - 2002"
s.resume = "Les frères En et Jin sont les descendants d'une famille d'exorcistes d'un genre particulier: ils ont pour mission de repousser des \"maga\", entités spirituelles négatives. Pour y parvenir, un seul moyen, trouver le véritable nom de leur ennemis avant ces derniers. De la même façon, nul ne connait les vrais noms d'En et de Jin, pas même leurs parents."
s.auteur_id = a.id
s.dessinateur_id = d.id
s.type_id = t.id
session.add(s)

session.flush()

t = Tome()
t.num = "1"
t.resume = "Les frères En et Jin sont les descendants d'une famille d'exorcistes d'un genre particulier : ils ont pour mission de repousser des \"maga\", entités spirituelles négatives. Pour y parvenir, un seul moyen, trouver le véritable nom de leur ennemis avant ces derniers. De la même façon, nul ne connait les vrais noms d'En et de Jin, pas même leurs parents."
t.date = "13 Septembre 2006"
t.serie_id = s.id
session.add(t)

asso1 = Asso_SerieGenre()
asso1.serie_id = s.id
asso1.genre_id = g1.id
session.add(asso1)

asso2 = Asso_SerieGenre()
asso2.serie_id = s.id
asso2.genre_id = g2.id
session.add(asso2)
#tout envoyer sur la bdd
session.commit() 

series = session.query(Serie).all()
print(series)