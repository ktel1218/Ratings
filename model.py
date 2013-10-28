from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

ENGINE = None
Session = None
Base = declarative_base()

### Class declarations go here
class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key= True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)


class Movie(Base):
    __tablename__="movies"

    id = Column(Integer, primary_key = True)
    title = Column(String(100))
    release_date = Column(Date)
    url = Column(String(2083))

class Rating(Base):
    __tablename__="ratings"

    id= Column(Integer, primary_key= True)
    user_id = Column(Integer)
    movie_id = Column(Integer)
    rating = Column(Integer)
    time_stamp = Column(DateTime)

    # ratings = relationship("Movie", back_ref = "id")


### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo = True)
    Session = sessionmaker(bind=ENGINE)
    return Session()

def main():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo = True)
    Session = sessionmaker(bind=ENGINE)


def initialize_tables():    
    """Initialize tables"""
    global ENGINE
    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Base.metadata.create_all(ENGINE)

if __name__ == "__main__":
    main()
