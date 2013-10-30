from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from sqlalchemy import Column, Integer, String, DateTime, Date
import correlation



engine = create_engine("sqlite:///ratings.db", echo = False)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))
Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key= True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def similarity(self, user2):

        rating_pairs = []
        overlap = {}

        for rating in self.ratings:
            overlap[rating.movie_id] = rating.rating

        for rating in user2.ratings:
            if overlap.get(rating.movie_id) != None:
                rating_pairs.append((overlap.get(rating.movie_id), rating.rating))

        return correlation.pearson(rating_pairs)      


class Movie(Base):
    __tablename__="movies"

    id = Column(Integer, primary_key = True)
    title = Column(String(100))
    release_date = Column(Date)
    url = Column(String(2083))

class Rating(Base):
    __tablename__="ratings"

    id= Column(Integer, primary_key= True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rating = Column(Integer)
    time_stamp = Column(DateTime)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))


### End class declarations
    

def main():
    """nothing doing"""

def initialize_tables():    
    """Initialize tables"""
    global ENGINE
    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Base.metadata.create_all(ENGINE)

def get_user_from_email(email):
    user = session.query(User).filter_by(email = email).all()
    #print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ model user",user
    if user == []:
        return None
    else:
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ model user.password",user[0].password
        return user[0]

def authenticate(email, password):
    user = session.query(User).filter_by(email = email).all()
    if user == []:
        return None
    else:

        return user[0]

def register_user(email, password, age, zipcode):
    new_user = User(email = email, password = password, age = age, zipcode = zipcode)
    session.add(new_user)
    session.commit()

def get_user_object_by_id(id):
    user = session.query(User).filter_by(id = id).all()
    if user == []:
        return None
    else:
        return user[0]

def get_all_users():
    return session.query(User).limit(40).all()

def get_ratings_by_user(user_id):
    return session.query(Rating).filter_by(user_id = user_id).all()

def get_movie_by_id(movie_id):
    movie = session.query(Movie).filter_by(id = movie_id).all()
    if movie == []:
        return None
    else:
        return movie[0]

def search_for_movie(movie):
    return session.query(Movie).filter(Movie.title.like("%" + movie + "%")).all()

def get_rating_by_user_id(movie_id, user_id):
    rating = session.query(Rating).filter_by(movie_id = movie_id).filter_by(user_id=user_id).all()
    if rating == []:
        return None
    else:
        return rating[0]

def get_ratings_by_movie_id(movie_id):
    ratings = session.query(Rating).filter_by(movie_id = movie_id).all()
    if ratings == []:
        return None
    else:
        return ratings

def rate_movie(movie_id, rating, user_id, time_stamp):
    existing_rating = get_rating_by_user_id(movie_id, user_id)
    if existing_rating == None:
        new_rating = Rating(movie_id = movie_id, rating= rating, user_id=user_id, time_stamp=time_stamp)
        session.add(new_rating)
    else:
        existing_rating.rating = rating
        existing_rating.time_stamp = time_stamp
    
    session.commit()

if __name__ == "__main__":
    main()
