import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone
import certifi

load_dotenv()
db = MongoClient(os.getenv("MONGO_URI") ,tlsCAFile = certifi.where()) # where to find trusted certificate to verify Atlas connection

games = [
    {
        "title": "Hades",
        "image_url": "images/hades.jpg",
        "genre": "Roguelike",
        "platform": "PC",
        "year": 2020,
        "description": "Battle through the Underworld as Zagreus, the son of Hades, in an action-packed roguelike featuring Greek mythology, powerful upgrades, and evolving character relationships."
    },
    {
        "title": "Stardew Valley",
        "image_url": "images/stardew.jpeg",
        "genre": "Simulation",
        "platform": "PC",
        "year": 2016,
        "description": "Restore an old farm, grow crops, raise animals, explore mines, and build friendships with villagers in a relaxing farming and life simulation game."
    },
    {
        "title": "Minecraft",
        "image_url": "images/Minecraft.jpg",
        "genre": "Sandbox",
        "platform": "PC",
        "year": 2011,
        "description": "Explore procedurally generated worlds, gather resources, craft tools, and build almost anything imaginable while surviving dangerous creatures."
    },
    {
        "title": "Terraria",
        "image_url": "images/Terraria.jpg",
        "genre": "Sandbox",
        "platform": "PC",
        "year": 2011,
        "description": "Dig, build, explore, and fight bosses in a procedurally generated 2D world filled with weapons, treasures, and secrets."
    },
    {
        "title": "Hollow Knight",
        "image_url": "images/Hollow Knight.jpg",
        "genre": "Metroidvania",
        "platform": "PC",
        "year": 2017,
        "description": "Explore the mysterious underground kingdom of Hallownest, battle challenging enemies, unlock new abilities, and uncover the story of a fallen civilization."
    },
    {
        "title": "Celeste",
        "image_url": "images/Celeste.png",
        "genre": "Platformer",
        "platform": "PC",
        "year": 2018,
        "description": "Help Madeline climb Celeste Mountain through challenging platforming levels while experiencing a story about perseverance and personal struggles."
    },
    {
        "title": "Portal 2",
        "image_url": "images/Portal 2.jpg",
        "genre": "Puzzle",
        "platform": "PC",
        "year": 2011,
        "description": "Solve physics-based puzzles using a portal gun that connects two locations, while navigating the abandoned Aperture Science facility."
    },
    {
        "title": "The Witcher 3: Wild Hunt",
        "image_url": "images/Witcher_3_cover_art.jpg",
        "genre": "RPG",
        "platform": "PC",
        "year": 2015,
        "description": "Play as Geralt of Rivia, a monster hunter searching for his adopted daughter in a vast fantasy world filled with quests and difficult moral choices."
    },
    {
        "title": "Elden Ring",
        "image_url": "images/eldenring.jpg",
        "genre": "Action RPG",
        "platform": "PC",
        "year": 2022,
        "description": "Explore the Lands Between, discover hidden dungeons, defeat powerful bosses, and develop a unique combat build in an expansive dark fantasy world."
    },
    {
        "title": "Red Dead Redemption 2",
        "image_url": "images/Red Dead Redemption II.jpg",
        "genre": "Action Adventure",
        "platform": "PC",
        "year": 2018,
        "description": "Follow outlaw Arthur Morgan and the Van der Linde gang as they struggle to survive during the decline of the American Wild West."
    },
    {
        "title": "Cyberpunk 2077",
        "image_url": "images/cyberpunk.jpg",
        "genre": "Action RPG",
        "platform": "PC",
        "year": 2020,
        "description": "Become V, a mercenary navigating the futuristic Night City, where cybernetic enhancements, corporate power, and personal choices shape the story."
    },
    {
        "title": "Slay the Spire",
        "image_url": "images/Slay The Spire.jpg",
        "genre": "Deckbuilding",
        "platform": "PC",
        "year": 2019,
        "description": "Construct a powerful deck of cards, collect mysterious relics, and battle increasingly difficult enemies while climbing a dangerous tower."
    },
    {
        "title": "Subnautica",
        "image_url": "images/subnautica.jpg",
        "genre": "Survival",
        "platform": "PC",
        "year": 2018,
        "description": "Survive on an alien ocean planet by exploring underwater environments, building habitats, crafting equipment, and uncovering the planet's mysteries."
    },
    {
        "title": "Factorio",
        "image_url": "images/factorio.jpeg",
        "genre": "Strategy",
        "platform": "PC",
        "year": 2020,
        "description": "Design automated factories, manage resources, develop technologies, and defend production lines against hostile creatures on an alien planet."
    },
    {
        "title": "Civilization VI",
        "image_url": "images/Civilization 6.jpg",
        "genre": "Turn-Based Strategy",
        "platform": "PC",
        "year": 2016,
        "description": "Lead a civilization from the ancient era to the modern age through scientific discovery, diplomacy, warfare, and cultural development."
    },
    {
        "title": "Among Us",
        "image_url": "images/Among Us.jpg",
        "genre": "Social Deduction",
        "platform": "PC",
        "year": 2018,
        "description": "Work with crewmates to complete tasks aboard a spaceship while identifying impostors secretly attempting to eliminate the crew."
    },
    {
        "title": "Cuphead",
        "image_url": "images/cuphead.jpg",
        "genre": "Run and Gun",
        "platform": "PC",
        "year": 2017,
        "description": "Battle imaginative bosses using precise shooting and dodging mechanics in a challenging action game inspired by 1930s cartoons."
    },
    {
        "title": "Outer Wilds",
        "image_url": "images/Outer Wilds.jpg",
        "genre": "Exploration",
        "platform": "PC",
        "year": 2019,
        "description": "Investigate a mysterious solar system trapped in a time loop, uncover ancient ruins, and solve interconnected mysteries through exploration."
    },
    {
        "title": "Dead Cells",
        "image_url": "images/deadcells.jpg",
        "genre": "Roguelike",
        "platform": "PC",
        "year": 2018,
        "description": "Fight through procedurally assembled levels, discover weapons and abilities, and defeat challenging enemies in a fast-paced action platformer."
    },
    {
        "title": "Balatro",
        "image_url": "images/Balatro.jpg",
        "genre": "Deckbuilding",
        "platform": "PC",
        "year": 2024,
        "description": "Create powerful poker hands and combine special Joker cards with unique modifiers to achieve increasingly high scores in a roguelike card game."
    }
]

for game in games:
    existing_game = db.games.find_one({"title": game["title"]})
    if existing_game is None:
        db.games.insert_one(game)
        print(f"Inserted {game['title']}")
    elif not existing_game.get("image_url"):
        db.games.update_one(
            {"_id": existing_game["_id"]},
            {"$set": {"image_url": game["image_url"]}},
        )
        print(f"Added image path for {game['title']}")

def day(d):
    # Helps to quickly return a UTC datetime for Oct <d>, 2026 at noon
    return datetime(2026, 10, d, 12, 0, tzinfo=timezone.utc)

# Game title, reviewer, rating, text, likes, dislikes, created_at, updated_at
sample_reviews = [
    ("Hades", "Cassivellaunus", 9, "Did you guys hear battle cries?.", 4, 0, day(8), day(8)),
    ("Hades", "Aristophanes", 6, "Noting a lack of ancient globule humans.", 2, 1, day(10), day(10)),
    ("Stardew Valley", "Napoleon", 10, "Finally, a farm fully under my own grasp.", 7, 0, day(9), day(9)),
    ("Stardew Valley", "Hannibal", 7, "Fun, but the first few days are slow.", 1, 1, day(11), day(12)),
    ("Minecraft", "Augustus", 1, "Best game I've ever played.", 3, 0, day(13), day(13))
]

inserted = 0
for title, reviewer, rating, text, likes, dislikes, created_at, updated_at in sample_reviews:
    game = db.games.find_one({"title": title})
    if game is None:
        print(f"Skipping review for '{title}': game not found")
        continue

    # Skip if this exact sample review is already in the database
    if db.reviews.find_one({"game_id": game["_id"], "reviewer": reviewer, "text": text}):
        continue

    db.reviews.insert_one({
        "game_id": game["_id"],
        "reviewer": reviewer,
        "rating": rating,
        "text": text,
        "likes": likes,
        "dislikes": dislikes,
        "created_at": created_at,
        "updated_at": updated_at,
    })
    inserted += 1

print(f"Inserted {inserted} new reviews")

# Recompute stored averages for every game that has reviews, since inserting directly skips update_average_rating() in app.py
for game_id in db.reviews.distinct("game_id"):
    ratings = [r["rating"] for r in db.reviews.find({"game_id": game_id}, {"rating": 1})]
    average = round(sum(ratings) / len(ratings), 1)
    db.games.update_one({"_id": game_id}, {"$set": {"average_rating": average}})