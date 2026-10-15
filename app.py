import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DBNAME")]


@app.route("/")
def home():
    games = list(db.games.find().sort("title", 1))
    return render_template("home.html", games=games)

# TODO (assign via Issues at some point): game details, review details, write review, edit review, delete review, search, add game, decide on others

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

import re

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()
    games = []

    if query:
        pattern = re.escape(query)

        games = list(db.games.find({
            "$or": [
                {"title": {"$regex": pattern, "$options": "i"}},
                {"genre": {"$regex": pattern, "$options": "i"}}
            ]
        }).sort("title", 1))

    return render_template("search.html", games=games, query=query)

@app.route("/games/<game_id>")
def game_details(game_id):
    if not ObjectId.is_valid(game_id):
        abort(404)

    game = db.games.find_one({"_id": ObjectId(game_id)})

    if game is None:
        abort(404)

    return render_template("game_details.html", game=game)

if __name__ == "__main__":
    app.run(debug=True)

