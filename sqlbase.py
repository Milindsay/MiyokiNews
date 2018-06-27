import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#Classe de base utilisée par SQLAlchemy pour lier une classe à une base de donnée
Base = declarative_base()

#Classe Série - qui représente la table 'Série'
class Serie(Base):
    __tablename__  = 'serie'
    id             = Column(Integer, primary_key=True)
    nb_VO          = Column(Integer)
    nb_VF          = Column(Integer)
    titre_VO       = Column(Text(1000))
    titre          = Column(Text(1000))
    origine        = Column(Text(1000))
    resume         = Column(Text(1000))
    auteur_id      = Column(Integer, ForeignKey('auteur.id'))
    dessinateur_id = Column(Integer, ForeignKey('dessinateur.id'))
    type_id        = Column(Integer, ForeignKey('type.id'))

    children = relationship("Asso_SerieGenre")

    #surdéfinition de l'opérateur= pour comparer deux entrées de la table 'Serie'. Retourne true si égale, false sinon.
    def __eq__(self, other):
        return type(self)==type(other) and self.titre == other.titre
    #surdéfinition de la fonction toString
    def __str__(self):
        return "Serie : " + self.titre + "  Nb VO : " + str(self.nb_VO) + "  Nb VF : " + str(self.nb_VF)
    #autre méthode éventuellement appelé pour représenter une classe en chaine de caractère
    def __repr__(self):
        return self.__str__()

#Classe Tome - qui représente la table 'Tome'
class Tome(Base):
    __tablename__ = 'tome'
    id            = Column(Integer, primary_key=True)
    num           = Column(String(50))
    date          = Column(String(50))
    resume        = Column(Text(1000))
    image_de_couv = Column(Text(1000))
    serie_id      = Column(Integer, ForeignKey('serie.id'))
    #surdéfinition de l'opérateur= pour comparer deux entrées de la table 'Tome'. Retourne true si égale, false sinon.
    def __eq__(self, other):
        return type(self)==type(other) and self.serie_id == other.serie_id and self.num == other.num
    #surdéfinition de la fonction toString
    def __str__(self):
        return "Tome num : " + self.num + "  date : " + str(self.date)
    #autre méthode éventuellement appelé pour représenter une classe en chaine de caractère
    def __repr__(self):
        return self.__str__()

#Classe Auteur - qui représente la table 'Auteur'
class Auteur(Base):
    __tablename__ = 'auteur'
    id            = Column(Integer, primary_key=True)
    nom           = Column(String(50))
    #surdéfinition de l'opérateur= pour comparer deux entrées de la table 'Auteur'. Retourne true si égale, false sinon.
    def __eq__(self, other):
        return type(self)==type(other) and self.nom == other.nom
    #surdéfinition de la fonction toString
    def __str__(self):
        if self.nom:
            return "Nom : "+ self.nom
        return "None"
    #autre méthode éventuellement appelé pour représenter une classe en chaine de caractère
    def __repr__(self):
        return self.__str__()

#Classe Dessinateur - qui représente la table 'Dessinateur'
class Dessinateur(Base):
    __tablename__ = 'dessinateur'
    id            = Column(Integer, primary_key=True)
    nom           = Column(String(50))
    #surdéfinition de l'opérateur= pour comparer deux entrées de la table 'Dessinateur'. Retourne true si égale, false sinon.
    def __eq__(self, other):
        return type(self)==type(other) and self.nom == other.nom
    #surdéfinition de la fonction toString
    def __str__(self):
        if self.nom:
            return "Nom : "+ self.nom
        return "None"
    #autre méthode éventuellement appelé pour représenter une classe en chaine de caractère
    def __repr__(self):
        return self.__str__()

#Classe Type - qui représente la table 'Type'
class Type(Base):
    __tablename__ = 'type'
    id            = Column(Integer, primary_key=True)
    nom           = Column(String(50))
    #surdéfinition de l'opérateur= pour comparer deux entrées de la table 'Type'. Retourne true si égale, false sinon.
    def __eq__(self, other):
        return type(self)==type(other) and self.nom == other.nom
    #surdéfinition de la fonction toString
    def __str__(self):
        if self.nom:
            return "Nom : "+ self.nom
        return "None"
    #autre méthode éventuellement appelé pour représenter une classe en chaine de caractère
    def __repr__(self):
        return self.__str__()

#Classe Genre - qui représente la table 'Genre'
class Genre(Base):
    __tablename__ = 'genre'
    id            = Column(Integer, primary_key=True)
    nom           = Column(String(50))
    #surdéfinition de l'opérateur= pour comparer deux entrées de la table 'Genre'. Retourne true si égale, false sinon.
    def __eq__(self, other):
        return type(self)==type(other) and self.nom == other.nom

    #surdéfinition de la fonction toString
    def __str__(self):
        if self.nom:
            return "Nom : "+ self.nom
        return "None"
    #autre méthode éventuellement appelé pour représenter une classe en chaine de caractère
    def __repr__(self):
        return self.__str__()

#Classe Association_Série-Genre - qui représente la table 'Asso-SérieGenre'
class Asso_SerieGenre(Base):
    __tablename__ = 'asso_seriegenre'
    serie_id      = Column(Integer, ForeignKey('serie.id'), primary_key=True)
    genre_id      = Column(Integer, ForeignKey('genre.id'), primary_key=True)
    child         = relationship("Genre")