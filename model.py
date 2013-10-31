from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from sqlalchemy import Column, Integer, String, DateTime, Date
import correlation
import math


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

        user_ratings = {}
        paired_ratings = []
        for rating in self.ratings:
            user_ratings[rating.movie_id] = rating

        for rating in user2.ratings:
            user_rating = user_ratings.get(rating.movie_id)
            if user_rating:
                paired_ratings.append( (user_rating.rating, rating.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return None

        # rating_pairs = []
        # overlap = {}
 
        # for rating in self.ratings:
        #     overlap[rating.movie_id] = rating.rating
        # for rating in user2.ratings:
        #     if overlap.get(rating.movie_id) != None:
        #         rating_pairs.append((overlap.get(rating.movie_id), rating.rating))
        # correlation_value = correlation.pearson(rating_pairs)

        # if correlation_value > 1:
        #     correlation_value = math.floor(correlation_value)
        # elif correlation_value < -1:
        #     correlation_value = math.ceil(correlation_value)

        # return correlation_value


    def prediction(self, movie_id):

        # get other users' ratings of this movie
        other_ratings = get_ratings_by_movie_id(movie_id)
        other_users = []

        #create list of all other users who have rated the movie
        for r in other_ratings:
            other_users.append(r.user)  

        #create tuple list of the other users and their ratings to input into Pearson Coefficient
        list_of_compares = []

        for other_u in other_users:

            list_of_compares.append((self.similarity(other_u), other_u.id))

        list_of_sorted_compares = sorted(list_of_compares, reverse=True)

        most_similar_user_id = list_of_sorted_compares[0][1]
        similarity_coefficient = list_of_sorted_compares[0][0]
        most_similar_user_rating = (get_rating_by_user_id(movie_id,most_similar_user_id)).rating
        guessed_rating = similarity_coefficient * most_similar_user_rating
        

        return guessed_rating





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
    if user == []:
        return None
    else:
        return user[0]

def get_user_object_by_id(id):
    user = session.query(User).filter_by(id = id).all()
    if user == []:
        return None
    else:
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
