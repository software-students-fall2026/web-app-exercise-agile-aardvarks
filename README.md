# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

We are building a game review database for gamers, so that they can find games worth playing and share their thoughts as well

## User stories

User stories are tracked as GitHub Issues: [View all user stories](https://github.com/software-students-fall2026/web-app-exercise-agile-aardvarks/issues)
Each story follows the format "As a [user type], I want [goal], so that [reason]."

## Steps necessary to run the software

1. Clone this repository: `git clone <repo-url>`, and `cd` into the folder
2. Create and activate a virtual environment:
    - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
    - Windows: `python -m venv venv` then `source venv/Scripts/activate`
3. Install dependencies:  `pip install -r requirements.txt`
4. Copy `env.example` to `.env` and fill in values (get real ones from team channel/doc)
5. Add starting games: `python seed.py` (only needs to be done once per shared database)
6. Run `python app.py`
7. Open `http://127.0.0.1:5000` in your browser

## Task boards

Each sprint has its own GitHub Project board:

- [Agile Aardvarks - Sprint 1](https://github.com/orgs/software-students-fall2026/projects/4/views/1)
- [Agile Aardvarks - Sprint 2]()