import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, abort, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pymongo.errors import DuplicateKeyError

import certifi # For establishing trusted connection to AtlasDB
import re
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Makes it explicit when the secret key isn't configured, so the application can't run without it
if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "SECRET_KEY must be set in the environment."
    )

login_manager = LoginManager(app)
login_manager.login_view = "login"

client = MongoClient(os.getenv("MONGO_URI") ,tlsCAFile = certifi.where()) # where to find trusted certificate to verify Atlas connection
db = client[os.getenv("MONGO_DBNAME")]
db.users.create_index("username_normalized", unique=True)

LIMITS = {
    "text": 1000,
    "title": 80,
    "genre": 30,
    "platform": 30,
    "description": 500,
    "username": 30,
    "password": 128
}

YEAR_MIN, YEAR_MAX = 1950, 2030

# Makes these limits available to every template we have
@app.context_processor
def inject_limits():
    return {"limits": LIMITS, "year_min": YEAR_MIN, "year_max": YEAR_MAX}


def length_errors(values):
    # Values: {"reviewer": "...", "text", "..."} -> list of error messages
    errors = []
    for name, text in values.items():      # e.g. name="title", text="Celeste"
        if len(text) > LIMITS[name]:       # LIMITS["text"] is 1000
            errors.append(f"{name.capitalize()} must be {LIMITS[name]} characters or fewer (currently {len(text)}).")
    return errors


def get_game_or_404(game_id):
    try:
        game = db.games.find_one({"_id": ObjectId(game_id)})
    except InvalidId:
        game = None
    if game is None:
        abort(404)
    return game


def read_game_form():
    # Reads game form fields from the request, and trims them
    fields = ("title", "genre", "platform", "year", "description")
    return {name: request.form.get(name, "").strip() for name in fields}


def validate_game(form):
    # Returns errors and year, used by both add and edit routes
    errors = []
    if not all(form.values()):
        errors.append("Please fill in every field.")
    errors += length_errors({
        "title": form["title"],
        "genre": form["genre"],
        "platform": form["platform"],
        "description": form["description"],
    })
    year = None
    try:
        year = int(form["year"])
        if not YEAR_MIN <= year <= YEAR_MAX:
            errors.append(f"Year must be between {YEAR_MIN} and {YEAR_MAX}.")
    except ValueError:
        errors.append("Year must be a number.")
    return errors, year


def update_average_rating(game_id):
    reviews = list(db.reviews.find({"game_id": game_id}))
    if len(reviews) == 0:
        average = None
    else:
        total = 0
        for rev in reviews:
            total += rev["rating"]
        average = round(total/len(reviews), 1)
    db.games.update_one(
        {"_id": game_id}, 
        {"$set": {"average_rating": average}}
    )


def owns_review(review):
    return (
        review is not None
        and review.get("user_id") is not None
        and str(review["user_id"]) == str(current_user.get_id())
    )


def owns_game(game):
    return (
        game is not None
        and game.get("added_by") is not None
        and str(game["added_by"]) == str(current_user.get_id())
    )


@app.route("/")
def home():
    # Checks if a sorting algorithm has been selected, if it hasn't (or random sort has been inputted) defaults to title ascending (A-Z)
    sort = request.args.get("sort", "title_asc")

    if sort == "title_desc":
        games = list(db.games.find().sort("title", -1))
    elif sort == "rating_desc":
        games = list(db.games.find().sort("average_rating", -1))
    elif sort == "rating_asc":
        games = list(db.games.find().sort("average_rating", 1))
    else:
        sort = "title_asc"
        games = list(db.games.find().sort("title", 1))

    # Games with no reviews always go to the bottom when sorting by rating
    if sort in ("rating_desc", "rating_asc"):
        rated = [game for game in games if game.get("average_rating") is not None]
        unrated = [game for game in games if game.get("average_rating") is None]
        games = rated + unrated
    
    return render_template("home.html", games=games, sort=sort)

@app.route("/game/<game_id>")
def game_detail(game_id):
    game = get_game_or_404(game_id)

    reviews = list(
        db.reviews.find({"game_id": game["_id"]})
        .sort("created_at", -1)
    )

    rating_counts = {i: 0 for i in range(1, 11)}

    for review in reviews:
        rating = review.get("rating")
        if rating in rating_counts:
            rating_counts[rating] += 1

    total_reviews = len(reviews)
    max_rating_count = max(rating_counts.values(), default=0)

    return render_template(
        "game_detail.html",
        game=game,
        reviews=reviews,
        rating_counts=rating_counts,
        total_reviews=total_reviews,
        max_rating_count=max_rating_count
    )

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    games = []
    if query:
        pattern = re.escape(query)
        games = list(db.games.find({
            "$or": [
                {"title": {"$regex": pattern, "$options": "i"}},
                {"genre": {"$regex": pattern, "$options": "i"}},
            ]
        }).sort("title", 1))
    return render_template("search.html", games=games, query=query)

@app.route("/add-game", methods=["GET", "POST"])
@login_required
def add_game():
    errors = []
    form = {"title": "", "genre": "", "platform": "", "year": "", "description": ""}

    if request.method == "POST":
        # Copy what the user typed into form, so we can re-show it on errors, and validate inputs
        form = read_game_form()
        image_url = request.form.get("image_url", "").strip()
        cover_file = request.files.get("cover_file")
        errors, year = validate_game(form)
        form["image_url"] = image_url
        if cover_file and cover_file.filename:
            filename = secure_filename(cover_file.filename)
            if not filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp")
            ):
                errors.append(
                    "Please upload a PNG, JPG, JPEG, or WEBP image."
                )
            else:
                upload_folder = os.path.join(
                    app.static_folder,
                    "uploads"
                )
                os.makedirs(
                    upload_folder,
                    exist_ok=True
                )
                cover_file.save(
                    os.path.join(
                        upload_folder,
                        filename
                    )
                )
                image_url = "uploads/" + filename
        elif image_url:
            if not (
                image_url.startswith("http://")
                or image_url.startswith("https://")
            ):
                errors.append("Please enter a valid image URL.")
            else:
                image_url = image_url

        # If no errors, save and go to new game's page
        if not errors:
            result = db.games.insert_one({
                "title": form["title"],
                "genre": form["genre"],
                "platform": form["platform"],
                "year": year,
                "description": form["description"],
                "average_rating": None,
                "image_url": image_url,
                "added_by": ObjectId(current_user.get_id()),
                "added_by_username": current_user.username,
            })
            flash("Game added successfully.", "success")
            return redirect(url_for("game_detail", game_id=result.inserted_id))
    # GET request, or errors, show the form (with errors and kept values)
    return render_template("add_game.html", errors=errors, form=form)

@app.route("/game/<game_id>/review", methods=["GET", "POST"])
@login_required
def write_review(game_id):
    # Look up the game, a bad or unknown id is a 404. Have to do this with new modules bc of ObjectId
    game = get_game_or_404(game_id)

    errors = []
    form = {"rating": "", "text": ""}

    if request.method == "POST":
        form["rating"] = request.form.get("rating", "").strip()
        form["text"] = request.form.get("text", "").strip()

        rating = int(form["rating"])

        # Validation
        if not form["text"]:
            errors.append("Please write a review.")
        if not form["rating"]:
            errors.append("Please choose a rating.")

        errors += length_errors({"text": form["text"]})

        if not errors:
            now = datetime.now(timezone.utc)
            db.reviews.insert_one({
                "game_id": game["_id"], # ObjectId, not the string from the URL
                "user_id": ObjectId(current_user.id),
                "reviewer": current_user.username,
                "rating": rating,
                "text": form["text"],
                "likes": 0,
                "dislikes": 0,
                "created_at": now,
                "updated_at": now,
            })
            update_average_rating(game["_id"])
            flash("Review posted successfully.", "success")
            return redirect(f"/game/{game_id}")

    return render_template("write_review.html", game=game, errors=errors, form=form)


@app.route("/game/<game_id>/edit", methods=["GET", "POST"])
@login_required
def edit_game(game_id):
    game = get_game_or_404(game_id)

    if not owns_game(game):
        abort(403)

    errors = []

    # Start with the saved values so the form is pre-filled
    form = {
        "title": game.get("title", ""),
        "genre": game.get("genre", ""),
        "platform": game.get("platform", ""),
        "year": game.get("year", ""),
        "description": game.get("description", ""),
        "image_url": (
            game.get("image_url", "")
            if (game.get("image_url") or "").startswith(("http://", "https://"))
            else ""
        ),
    }

    if request.method == "POST":
        form = read_game_form()
        errors, year = validate_game(form)

        image_url = request.form.get("image_url", "").strip()

        # If a new file was uploaded, save it
        cover_file = request.files.get("cover_file")

        if cover_file and cover_file.filename:
            filename = secure_filename(cover_file.filename)
            cover_file.save(os.path.join(app.static_folder, "uploads", filename))
            image_url = "uploads/" + filename

        # If no URL or file was provided, keep the existing cover
        if not image_url:
            image_url = game.get("image_url", "")

        form["image_url"] = image_url

        if not errors:
            db.games.update_one(
                {"_id": game["_id"]},
                {"$set": {**form}}   # form values
            )
            flash("Game edited successfully.", "success")
            return redirect(url_for("game_detail", game_id=game["_id"]))

    return render_template("add_game.html", errors=errors, form=form, game=game, editing=True)


@app.route("/game/<game_id>/delete", methods=["POST"])
@login_required
def delete_game(game_id):
    game = get_game_or_404(game_id)

    if not owns_game(game):
        abort(403)

    db.reviews.delete_many({"game_id": game["_id"]})   # reviews first, so none are orphaned
    db.games.delete_one({"_id": game["_id"]})
    flash("Game deleted successfully.", "success")
    return redirect(url_for("home"))

@app.route("/review/<review_id>/edit", methods=["GET","POST"])
@login_required
def edit_review(review_id):
    try:
        review = db.reviews.find_one({"_id":ObjectId(review_id)})
    except InvalidId:
        abort(404)

    if review is None:
        abort(404)

    if not owns_review(review):
        abort(403)

    game = get_game_or_404(str(review["game_id"]))

    errors = []

    form = {
        "rating": str(review["rating"]),
        "text": review["text"]
    }

    if request.method == "POST":
        form["rating"] = request.form.get("rating", "").strip()
        form["text"] = request.form.get("text", "").strip()

        if not form["text"]:
            errors.append("Please write a review.")

        errors += length_errors({"text": form["text"]})

        try:
            rating = int(form["rating"])
            if rating < 1 or rating > 10:
                errors.append("Rating must be between 1 and 10.")
        except ValueError:
            errors.append("Please choose a valid rating.")

        if not errors:
            db.reviews.update_one(
                {"_id": review["_id"]},
                {"$set": {
                    "rating": rating,
                    "text": form["text"],
                    "updated_at": datetime.now(timezone.utc)
                }}
            )

            update_average_rating(game["_id"])

            flash("Review edited successfully.", "success")
            return redirect(
                url_for("game_detail", game_id=game["_id"])
            )

    return render_template(
        "edit_review.html",
        game=game,
        review=review,
        form=form,
        errors=errors
        )



@app.route("/review/<review_id>/delete", methods=["POST"])
def delete_review(review_id):
    try:
        review = db.reviews.find_one({"_id": ObjectId(review_id)})
    except (InvalidId, TypeError):
        abort(404)

    if review is None:
        abort(404)

    if not owns_review(review):
        abort(403)

    game_id = review["game_id"]

    db.reviews.delete_one({"_id": review["_id"]})

    update_average_rating(game_id)

    flash("Review deleted successfully.", "success")
    return redirect(url_for("game_detail", game_id=game_id))

@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    errors = []

    if request.method == "POST":

        entered_username = request.form.get("username", "").strip()
        username_normalized = entered_username.lower()

        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validate required fields
        if not entered_username:
            errors.append("Please enter a username.")

        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")

        # Validate maximum character lengths
        errors += length_errors({
            "username": entered_username,
            "password": password
        })

        # Check matching passwords
        if password != confirm_password:
            errors.append("Passwords do not match.")

        # Return validation errors
        if errors:
            return render_template(
                "create_account.html",
                error=errors[0],
                username=entered_username
            ), 400

        hashed_password = generate_password_hash(password)

        user = {
            "username": entered_username,
            "username_normalized": username_normalized,
            "password": hashed_password
        }

        try:
            db.users.insert_one(user)
        except DuplicateKeyError:
            return render_template(
                "create_account.html",
                error="This username is already taken.",
                username=entered_username
            ), 409

        flash("Account created successfully.", "success")
        return redirect(url_for("home"))

    return render_template("create_account.html", error=None, username="")

class User(UserMixin):
    def __init__(self, user_document):
        self.id = str(user_document["_id"])
        self.username = user_document["username"]

@login_manager.user_loader
def load_user(user_id):
    try:
        user_document = db.users.find_one({
            "_id": ObjectId(user_id)
        })
    except (InvalidId, TypeError):
        return None

    if user_document is None:
        return None

    return User(user_document)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        entered_username = request.form.get("username", "").strip()
        username_normalized = entered_username.lower()
        password = request.form.get("password", "")

        # Validate required fields
        if not entered_username or not password:
            return render_template(
                "login.html",
                error="Please enter your username and password.",
                username=entered_username
            ), 400

        # Validate maximum character lengths
        errors = length_errors({
            "username": entered_username,
            "password": password
        })

        if errors:
            return render_template(
                "login.html",
                error=errors[0],
                username=entered_username
            ), 400

        # Find user in MongoDB
        user_document = db.users.find_one({
            "username_normalized": username_normalized
        })

        # Verify credentials
        if user_document is None or not check_password_hash(
            user_document["password"], password
        ):
            return render_template(
                "login.html",
                error="Invalid username or password.",
                username=entered_username
            ), 401

        # Convert MongoDB document into Flask-Login user
        user = User(user_document)

        # Log in the user
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)