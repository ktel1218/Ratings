import model
import csv
from datetime import datetime

def load_users(session):
    # use u.user
    f = open("seed_data/u.user")
    entries = f.read().split("\n")
    f.close()
    for item in entries:
        item = item.split("|")
        user = model.User(id = int(item[0]), age = int(item[1]), zipcode = item[4])
        session.add(user)

    session.commit()

def load_movies(session):
    f = open("seed_data/u.item")
    entries = f.read().split("\n")
    f.close()
    for item in entries:

        item = item.split("|")
        title = item[1]
        date = item[2]
        if title != "unknown" and date != None:
            date_formatted = datetime.strptime(date, "%d-%b-%Y")
            title_formatted =  title.decode("latin-1")
            movie = model.Movie(id = int(item[0]), title = title_formatted, release_date = date_formatted, url = item[4])
            session.add(movie)
    
    session.commit()


def load_ratings(session):
    # use u.data
    f = open("seed_data/u.data")
    entries = f.read().split("\n")
    f.close()
    for item in entries:
        item = item.split()
        timestamp = int(item[3])
        formatted_time = datetime.utcfromtimestamp(timestamp)
        rating = model.Rating(user_id = int(item[0]), movie_id = int(item[1]), rating = int(item[2]), time_stamp = formatted_time)
        session.add(rating)

    session.commit()



def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)




# open a file
# read a line
# parse a line
# create an object
# add the object to a session
# commit
# repeat until done
