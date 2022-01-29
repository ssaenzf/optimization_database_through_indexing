import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select
from datetime import date, datetime
import random
import pymongo
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import desc

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si2", echo=False)
#db_meta = MetaData(bind=db_engine)
# declarando las tablas
# clase base que mantiene el catalogo de clases y tablas
Base = declarative_base()
#Clases donde se mapeará la base de datos
#MongoClient
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongoClient["si1"]
class imdb_movies(Base):
    __tablename__ = 'imdb_movies'

    movieid = Column(Integer, primary_key=True)
    movietitle = Column(String)
    movierelease = Column(String)
    movietype = Column(Integer)
    year = Column(Integer)
    issuspended = Column(Integer)

class imdb_directormovies(Base):
    __tablename__ = 'imdb_directormovies'

    directorid = Column(Integer, primary_key=True)
    movieid = Column(Integer)
    numpartitipation = Column(Integer)
    ascharacter = Column(String)
    participation = Column(String)
    isarchivefootage = Column(Integer)
    isuncredited = Column(Integer)
    iscodirector = Column(Integer)
    ispilot = Column(Integer)
    ischief = Column(Integer)
    ishead = Column(Integer)

class imdb_directors(Base):
    __tablename__ = 'imdb_directors'

    directorid = Column(Integer, primary_key=True)
    directorname = Column(String)

class imdb_actormovies(Base):
    __tablename__ = 'imdb_actormovies'

    actorid = Column(Integer, primary_key=True)
    movieid = Column(Integer)
    numparticipation = Column(Integer)
    character = Column(String)
    ascharacter = Column(String)
    isvoice = Column(Integer)
    isarchivefootage = Column(Integer)
    isuncredited = Column(Integer)
    creditsposition = Column(Integer)

class imdb_actors(Base):
    __tablename__ = 'imdb_actors'

    actorid = Column(Integer, primary_key=True)
    actorname = Column(String)
    gender = Column(String)

class imdb_moviegenres(Base):
    __tablename__ = 'imdb_moviegenres'

    movieid = Column(Integer, primary_key=True)
    genre = Column(String, primary_key=True)

def database_create():
    try:
        # conexion a la base de datos sql y creacion de sesion
        Session = sessionmaker(bind=db_engine)
        session = Session()
        topUSA=db["topUSA"]
        topUSA.drop()   #se elmina si ya estaba de antes
        topUSA=db["topUSA"]
        print(sqlalchemy.__version__)
        pelis = session.query(imdb_movies).order_by(desc(imdb_movies.year))[0:800]  #error
        for peli in pelis:
            #busqueda generos
            moviegenres=session.query(imdb_moviegenres).filter_by(movieid=peli.movieid)
            nombres_generos = []
            for moviegenre in moviegenres:
                nombres_generos.append(moviegenre.genre)
            #busqueda directores
            moviedirectors=session.query(imdb_directormovies).filter_by(movieid=peli.movieid)
            directores = []
            for moviedirector in moviedirectors:
                directores.append(session.query(imdb_directors).filter_by(directorid=moviedirector.directorid)[0])
            nombres_directores = []
            for director in directores:
                nombres_directores.append(director.directorname) #string
            #busqueda actores
            movieactors=session.query(imdb_actormovies).filter_by(movieid=peli.movieid)
            actores = []
            for movieactor in movieactors:
                actores.append(session.query(imdb_actors).filter_by(actorid=movieactor.actorid)[0])
            nombres_actores = []
            for actor in actores:
                nombres_actores.append(actor.actorname) #string
            doc = {
            "title": peli.movietitle,
            "genres": nombres_generos,
            "year": peli.year,
            "directors": nombres_directores,
            "actors": nombres_actores,
            "most_related_movies": [],
            "related_movies": [] }
            topUSA.insert_one(doc)

        #Busqueda de los related
        for peli in topUSA.find():
            most_related_movies=[]
            related_movies=[]
            if (len(peli.get("genres"))==1):
                for peli2 in topUSA.find():
                    for genre1 in peli2.get("genres"):
                        if (peli.get("genres")[0]==genre1):
                            most_related_movies.append(peli2.get("title"))
                related_movies = []
            else:
                for peli2 in topUSA.find():
                    total=len(peli.get("genres"))
                    mitad=len(peli.get("genres"))/2
                    ngenres = 0
                    for genre1 in peli2.get("genres"):
                        for genre2 in peli.get("genres"):
                            if genre2==genre1:
                                ngenres=ngenres+1
                    #ya tenemos en que medida se parecen
                    if(ngenres==mitad):
                        related_movies.append(peli2.get("title"))
                    if(ngenres==total):
                        most_related_movies.append(peli2.get("title"))
            #insercion de los related
            #nuevos valores
            topUSA.update({"title":peli.get("title")}, {"$set":{"most_related_movies":most_related_movies, "related_movies":related_movies}})
        #falta los related, mediante el update


        mongoClient.close()

    except:
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'Something is broken'

if __name__ == '__main__':
    print('Starting Mongo Database Creation')
    database_create()
