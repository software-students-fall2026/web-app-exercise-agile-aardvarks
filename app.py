import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, abort
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import certifi # For establishing trusted connection to AtlasDB
import re

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI") ,tlsCAFile = certifi.where()) # where to find trusted certificate to verify Atlas connection
db = client[os.getenv("MONGO_DBNAME")]

def get_game_or_404(game_id):
    try:
        game = db.games.find_one({"_id": ObjectId(game_id)})
    except InvalidId:
        game = None
    if game is None:
        abort(404)
    return game


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


@app.route("/")
def home():
    games = list(db.games.find().sort("title", 1))
    return render_template("home.html", games=games)


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


@app.route("/game/<game_id>")
def game_detail(game_id):
    game = get_game_or_404(game_id)
    reviews = list(db.reviews.find({"game_id": game["_id"]}).sort("created_at", -1))
    return render_template("game_detail.html", game=game, reviews=reviews)


@app.route("/add-game", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        game = {
            "title": request.form["title"].strip(),
            "genre": request.form["genre"].strip(),
            "platform": request.form["platform"].strip(),
            "year": int(request.form["year"]),
            "description": request.form["description"].strip(),
            "average_rating": None,
        }
        result = db.games.insert_one(game)
        return redirect(f"/game/{result.inserted_id}")
    return render_template("add_game.html")


@app.route("/game/<game_id>/review", methods=["GET", "POST"])
def write_review(game_id):
    # Look up the game, a bad or unknown id is a 404. Have to do this with new modules bc of ObjectId
    game = get_game_or_404(game_id)

    errors = []
    form = {"reviewer": "", "rating": "", "text": ""}

    if request.method == "POST":
        form["reviewer"] = request.form.get("reviewer", "").strip()
        form["rating"] = request.form.get("rating", "").strip()
        form["text"] = request.form.get("text", "").strip()

        rating = int(form["rating"])

        # Validation
        if not form["reviewer"]:
            errors.append("Please enter your name.")
        if not form["text"]:
            errors.append("Please write a review.")
        if not form["rating"]:
            errors.append("Please choose a rating.")

        if not errors:
            now = datetime.now(timezone.utc)
            db.reviews.insert_one({
                "game_id": game["_id"], # ObjectId, not the string from the URL
                "reviewer": form["reviewer"],
                "rating": rating,
                "text": form["text"],
                "likes": 0,
                "dislikes": 0,
                "created_at": now,
                "updated_at": now,
            })
            update_average_rating(game["_id"]) # Added by Angelina to save new average rating
            return redirect(f"/game/{game_id}") # Should work once Sara does details page

    return render_template("write_review.html", game=game, errors=errors, form=form)

@app.route("/review/<review_id>/edit", methods=["GET","POST"])
def edit_review(review_id):
    try:
        review = db.reviews.find_one({"_id":ObjectId(review_id)})
    except InvalidId:
        abort(404)

    if review is None:
        abort(404)

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        rating_val = request.form.get("rating", "")

        try:
            rating = int(rating_val)
        except ValueError:
            rating = 0

        if not text or rating < 1 or rating > 10:
            abort(400)

        db.reviews.update_one(
            {"id": review["_id"]},
            {"$set": {
                "text": text,
                "rating": rating,
                "updated_at": datetime.now(timezone.utc)
            }}
        )

        update_average_rating(review["game_id"])

        return redirect(f"/game/{review['game_id']}")

    return render_template("edit_review.html", review=review)




if __name__ == "__main__":
    app.run(debug=True)