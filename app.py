import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, abort
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DBNAME")]


@app.route("/")
def home():
    games = list(db.games.find().sort("title", 1))
    return render_template("home.html", games=games)

@app.route("/game/<game_id>")
def game_detail(game_id):
    try:
        game = db.games.find_one({"_id": ObjectId(game_id)})
    except InvalidId:
        game = None
    if game is None:
        abort(404)
    return render_template("game_detail.html", game=game)

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

if __name__ == "__main__":
    app.run(debug=True)

