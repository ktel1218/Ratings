from flask import Flask, render_template, redirect, request, session, url_for, flash
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
    rated = False

    ## calls Prediction function if we havent rated it, shows our rating if we have

    rating_obj = model.get_rating_by_user_id(movie_id, user_id)

    if rating_obj == None:
        user = model.get_user_object_by_id(user_id)
        rating = user.prediction(movie_id)

    else:
        rating = rating_obj.rating
        rated = True

    return render_template("movie.html", movie = movie, rating = rating, rated = rated)


@app.route("/movies/<movie_id>", methods = ["POST"])
def rate_movie(movie_id):
    rating = request.form.get('rating')
    user_id = session.get("user_id")
    timestamp = datetime.now()

    model.rate_movie(movie_id, rating, user_id, timestamp)
    return redirect(url_for("movie", movie_id = movie_id))


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