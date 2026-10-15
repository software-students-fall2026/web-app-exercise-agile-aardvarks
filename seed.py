import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
db = MongoClient(os.getenv("MONGO_URI"))[os.getenv("MONGO_DBNAME")]


games = [
    {
        "title": "Hades",
        "genre": "Roguelike",
        "platform": "PC",
        "year": 2020,
        "description": "Battle through the Underworld as Zagreus, the son of Hades, in an action-packed roguelike featuring Greek mythology, powerful upgrades, and evolving character relationships."
    },
    {
        "title": "Stardew Valley",
        "genre": "Simulation",
        "platform": "PC",
        "year": 2016,
        "description": "Restore an old farm, grow crops, raise animals, explore mines, and build friendships with villagers in a relaxing farming and life simulation game."
    },
    {
        "title": "Minecraft",
        "genre": "Sandbox",
        "platform": "PC",
        "year": 2011,
        "description": "Explore procedurally generated worlds, gather resources, craft tools, and build almost anything imaginable while surviving dangerous creatures."
    },
    {
        "title": "Terraria",
        "genre": "Sandbox",
        "platform": "PC",
        "year": 2011,
        "description": "Dig, build, explore, and fight bosses in a procedurally generated 2D world filled with weapons, treasures, and secrets."
    },
    {
        "title": "Hollow Knight",
        "genre": "Metroidvania",
        "platform": "PC",
        "year": 2017,
        "description": "Explore the mysterious underground kingdom of Hallownest, battle challenging enemies, unlock new abilities, and uncover the story of a fallen civilization."
    },
    {
        "title": "Celeste",
        "genre": "Platformer",
        "platform": "PC",
        "year": 2018,
        "description": "Help Madeline climb Celeste Mountain through challenging platforming levels while experiencing a story about perseverance and personal struggles."
    },
    {
        "title": "Portal 2",
        "genre": "Puzzle",
        "platform": "PC",
        "year": 2011,
        "description": "Solve physics-based puzzles using a portal gun that connects two locations, while navigating the abandoned Aperture Science facility."
    },
    {
        "title": "The Witcher 3: Wild Hunt",
        "genre": "RPG",
        "platform": "PC",
        "year": 2015,
        "description": "Play as Geralt of Rivia, a monster hunter searching for his adopted daughter in a vast fantasy world filled with quests and difficult moral choices."
    },
    {
        "title": "Elden Ring",
        "genre": "Action RPG",
        "platform": "PC",
        "year": 2022,
        "description": "Explore the Lands Between, discover hidden dungeons, defeat powerful bosses, and develop a unique combat build in an expansive dark fantasy world."
    },
    {
        "title": "Red Dead Redemption 2",
        "genre": "Action Adventure",
        "platform": "PC",
        "year": 2018,
        "description": "Follow outlaw Arthur Morgan and the Van der Linde gang as they struggle to survive during the decline of the American Wild West."
    },
    {
        "title": "Cyberpunk 2077",
        "genre": "Action RPG",
        "platform": "PC",
        "year": 2020,
        "description": "Become V, a mercenary navigating the futuristic Night City, where cybernetic enhancements, corporate power, and personal choices shape the story."
    },
    {
        "title": "Slay the Spire",
        "genre": "Deckbuilding",
        "platform": "PC",
        "year": 2019,
        "description": "Construct a powerful deck of cards, collect mysterious relics, and battle increasingly difficult enemies while climbing a dangerous tower."
    },
    {
        "title": "Subnautica",
        "genre": "Survival",
        "platform": "PC",
        "year": 2018,
        "description": "Survive on an alien ocean planet by exploring underwater environments, building habitats, crafting equipment, and uncovering the planet's mysteries."
    },
    {
        "title": "Factorio",
        "genre": "Strategy",
        "platform": "PC",
        "year": 2020,
        "description": "Design automated factories, manage resources, develop technologies, and defend production lines against hostile creatures on an alien planet."
    },
    {
        "title": "Civilization VI",
        "genre": "Turn-Based Strategy",
        "platform": "PC",
        "year": 2016,
        "description": "Lead a civilization from the ancient era to the modern age through scientific discovery, diplomacy, warfare, and cultural development."
    },
    {
        "title": "Among Us",
        "genre": "Social Deduction",
        "platform": "PC",
        "year": 2018,
        "description": "Work with crewmates to complete tasks aboard a spaceship while identifying impostors secretly attempting to eliminate the crew."
    },
    {
        "title": "Cuphead",
        "genre": "Run and Gun",
        "platform": "PC",
        "year": 2017,
        "description": "Battle imaginative bosses using precise shooting and dodging mechanics in a challenging action game inspired by 1930s cartoons."
    },
    {
        "title": "Outer Wilds",
        "genre": "Exploration",
        "platform": "PC",
        "year": 2019,
        "description": "Investigate a mysterious solar system trapped in a time loop, uncover ancient ruins, and solve interconnected mysteries through exploration."
    },
    {
        "title": "Dead Cells",
        "genre": "Roguelike",
        "platform": "PC",
        "year": 2018,
        "description": "Fight through procedurally assembled levels, discover weapons and abilities, and defeat challenging enemies in a fast-paced action platformer."
    },
    {
        "title": "Balatro",
        "genre": "Deckbuilding",
        "platform": "PC",
        "year": 2024,
        "description": "Create powerful poker hands and combine special Joker cards with unique modifiers to achieve increasingly high scores in a roguelike card game."
    }
]

for game in games:
    if db.games.find_one({"title": game["title"]}) is None:
        db.games.insert_one(game)
        print(f"Inserted {game['title']}")