import os
from dotenv import load_dotenv
from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(debug=True)