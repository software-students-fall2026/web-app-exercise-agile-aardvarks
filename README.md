# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

We are building a game review database for gamers, so that they can find games worth playing and share their thoughts as well

## User stories

User stories are tracked as GitHub Issues: [View all user stories](https://github.com/software-students-fall2026/web-app-exercise-agile-aardvarks/issues)
Each story follows the format "As a [user type], I want [goal], so that [reason]."

## Steps necessary to run the software

### Prerequisites

- [Python 3](https://www.python.org/downloads/) (3.10 or newer)
- [Git](https://git-scm.com/downloads)
- The team's database credentials (shared in the team channel)

### Setup

1. Clone this repository and move into the folder:
    ```
    git clone https://github.com/software-students-fall2026/web-app-exercise-agile-aardvarks.git
    cd web-app-exercise-agile-aardvarks
    ```
2. Run the course setup script once (required for every clone):
    - Mac/Linux: `python3 .automations/setup.py`
    - Windows: `python .automations/setup.py`
3. Create and activate a virtual environment:
    - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
    - Windows: `python -m venv venv` then `source venv/Scripts/activate` (Git Bash) or `venv\Scripts\activate` (cmd/PowerShell)

    You should see `(venv)` at the start of your terminal prompt. Re-run the activate command each time you open a new terminal.
4. Install dependencies: `pip install -r requirements.txt`
5. Create your `.env` file from the example:
    - Mac/Linux/Git Bash: `cp env.example .env`
    - Windows (cmd): `copy env.example .env`

    Then open `.env` and fill in the values:
    - `MONGO_URI` and `MONGO_DBNAME`: get the real values from the team channel.
    - `SECRET_KEY`: used by Flask to keep users logged in. Generate one with `python3 -c "import secrets; print(secrets.token_hex(32))"` and paste the output in as the value.

    Never commit `.env`; it is already listed in `.gitignore`.
6. Add starting games and reviews: `python seed.py` (only needs to be done once per shared database)

### Running the app

1. Run `python app.py` (use `python3` on Mac if `python` is not found)
2. Open `http://127.0.0.1:5000` in your browser
3. Press `Ctrl + C` in the terminal to stop the server

### Using the app

- Anyone can browse games, search, sort, and read reviews without logging in.
- Create an account and log in to add games or write reviews.
- You can only edit or delete the games and reviews you created.

### Troubleshooting

- **`RuntimeError: SECRET_KEY must be set in the environment`**: your `.env` is missing `SECRET_KEY`. Add it as described in step 5 (make sure you edited `.env`, not `env.example`).
- **`TypeError: name must be an instance of str, not NoneType`**: the app can't find your `.env` file. Make sure it is named exactly `.env` and is in the main project folder next to `app.py`.
- **`ModuleNotFoundError`**: your virtual environment probably isn't active. Activate it (step 3) and run `pip install -r requirements.txt` again.
- **`ServerSelectionTimeoutError`**: check your internet connection, and ask a teammate to confirm your IP address is allowed under Network Access in MongoDB Atlas.


## Task boards

Each sprint has its own GitHub Project board:

- [Agile Aardvarks - Sprint 1](https://github.com/orgs/software-students-fall2026/projects/4/views/2/1)
- [Agile Aardvarks - Sprint 2](https://github.com/orgs/software-students-fall2026/projects/4/views/6)