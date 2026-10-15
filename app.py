import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, abort
from datetime import datetime, timezone
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DBNAME")]


@app.route("/")
def home():
    games = list(db.games.find().sort("title", 1))
    return render_template("home.html", games=games)

# TODO (assign via Issues at some point): review details, edit review, delete review, search, decide on others

@app.route("/add-game", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        game = {
            "title": request.form["title"].strip(),
            "genre": request.form["genre"].strip(),
            "platform": request.form["platform"].strip(),
            "year": int(request.form["year"]),
            "description": request.form["description"].strip(),
        }
        db.games.insert_one(game)
        return redirect("/")      # switch to the new game's page once details exists
    return render_template("add_game.html")

@app.route("/game/<game_id>/review", methods=["GET", "POST"])
def write_review(game_id):
    # Look up the game, a bad or unknown id is a 404. Have to do this with new modules bc of ObjectId
    try:
        game = db.games.find_one({"_id": ObjectId(game_id)})
    except InvalidId:
        game = None
    if game is None:
        abort(404)

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
            return redirect(f"/game/{game_id}") # Should work once Sara does details page

    return render_template("write_review.html", game=game, errors=errors, form=form)

if __name__ == "__main__":
    app.run(debug=True)