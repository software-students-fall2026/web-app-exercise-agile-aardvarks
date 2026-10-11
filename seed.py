import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
db = MongoClient(os.getenv("MONGO_URI"))[os.getenv("MONGO_DBNAME")]

games = [
    {"title": "Hades", "genre": "Roguelike", "platform": "PC", "year": 2020,
     "description": "generic_description_1"},
    {"title": "Stardew Valley", "genre": "Simulation", "platform": "PC", "year": 2016,
     "description": "generic_description_2"},
    # add ~18 more for a solid starting library?
]

if db.games.count_documents({}) == 0:
    db.games.insert_many(games)
    print(f"Inserted {len(games)} games")
else:
    print("Games already exist, skipping")