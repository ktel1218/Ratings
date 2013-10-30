from flask import Flask, render_template, redirect, request, session, url_for, flash, jsonify
import model
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Katie IS the best"

#need to create session variables

@app.route("/")
def index():
    return redirect(url_for("all_users"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=['POST'])
def process_registration():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')

    user_id = model.get_user_from_email(email)

    if user_id != None:
        flash("Already registered, please login")
    else:
        if password == confirm_password:
            model.register_user(email, hash(password), int(age), zipcode)
            flash("you've been successfully registered!")
            return redirect(url_for("login"))

            #redirect to userpage
        else:
            flash("Passwords do not match")
            return redirect(url_for("register"))


@app.route("/login")
def login():
    if session.get("user_id"):
        return redirect(url_for("index"))
    else:
        return render_template("login.html")        

@app.route("/login", methods=['POST'])
def process_login():
    email = request.form.get('email')
    password = request.form.get('password')

    #Get USER OBJECT from EMAIL, return OBJECT or NONE
    user = model.get_user_from_email(email)

    if user != None:
        
        if int(user.password) == hash(password):
            session['user_id'] = user.id
            return redirect(url_for("all_users"))
        else:
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))

    else:
        flash("Email not found, please register")
        return redirect(url_for("login"))


@app.route("/users")
def all_users():
    user_list = model.get_all_users()
    return render_template("user_list.html", users = user_list)


@app.route("/users/<user_id>")
def user_ratings(user_id):
    ratings = model.get_ratings_by_user(user_id)
    return render_template("user_ratings.html", ratings = ratings, user_id = user_id)
    return render_template("test.html", ratings= ratings)

@app.route("/movies/<movie_id>")
def movie(movie_id):
    movie = model.get_movie_by_id(movie_id)

    user_id = session.get("user_id")
    user1 = model.get_user_object_by_id(user_id)
    # get other users' ratings of this movie
    other_ratings = model.get_ratings_by_movie_id(movie_id)
    other_users = []

    #create list of all other users who have rated the movie
    for r in other_ratings:
        other_users.append(r.user)  

    #create tuple list of the other users and their ratings to input into Pearson Coefficient
    list_of_compares = []
    for other_u in other_users:
        list_of_compares.append((other_u.id, user1.similarity(other_u)))


    return render_template("movie.html", movie = movie, list_of_compares = list_of_compares)


@app.route("/movies/<movie_id>", methods = ["POST"])
def rate_movie(movie_id):
    rating = request.form.get('rating')
    user_id = session.get("user_id")
    timestamp = datetime.now()

    model.rate_movie(movie_id, rating, user_id, timestamp)
    flash("You rated this movie a " + rating)
    return redirect(url_for("movie", movie_id = movie_id))



# Test for JSON/jQuery
# @app.route("/movies/<movie_id>")
# def movie(movie_id):
#     movie = model.get_movie_by_id(movie_id)
#     return render_template("test.html", movie = movie)

# @app.route("/rate", methods=['POST'])
# def ajax_request():
#     # value = request.form.get("star_value")
#     # model.rate_movie(value, userid, movieid)
#     return "hey this was something cool"


    #view movie, and if logged in, shows rating/allows rating/allows edit of rating
@app.route("/search", methods=["POST"])
def search():
    movie =  request.form.get("search")
    results = model.search_for_movie(movie)

    if results == []:
        flash("No search results found")
    return render_template("search.html", results = results)



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug = True)


