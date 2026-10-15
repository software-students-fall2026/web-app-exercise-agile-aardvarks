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
- The team's `.env` values (shared in the team channel)

### Setup

1. Clone this repository and move into the folder:
```
    git clone https://github.com/software-students-fall2026/web-app-exercise-agile-aardvarks.git
    cd web-app-exercise-agile-aardvarks
```
2. Run the course setup script once (required for every clone):
    - Mac/Linux: `python3 .automations/setup.py`
    - Windows: `python .automations/setup.py`

    Fix any problems it reports.
3. Create and activate a virtual environment:
    - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
    - Windows (Command Prompt or PowerShell): `python -m venv venv` then `venv\Scripts\activate`
    - Windows (Git Bash): `python -m venv venv` then `source venv/Scripts/activate`

    You should see `(venv)` at the start of your terminal prompt. Re-run the activate command each time you open a new terminal.
4. Install dependencies: `pip install -r requirements.txt`
5. Create your `.env` file from the example:
    - Mac/Linux/Git Bash: `cp env.example .env`
    - Windows (Command Prompt): `copy env.example .env`

    Then open `.env` and replace the placeholder values with the real ones from the team channel. Never commit `.env`; it is already listed in `.gitignore`.
6. Add starting games: `python seed.py` (only needs to be done once per shared database)

### Running the app

1. Run `python app.py` (use `python3` on Mac if `python` is not found)
2. Open `http://127.0.0.1:5000` in your browser
3. Press `Ctrl + C` in the terminal to stop the server

The server reloads automatically when you save a file.

### Troubleshooting

- **`TypeError: name must be an instance of str, not NoneType`**: the app can't find your `.env` file. Make sure it is named exactly `.env` and is in the main project folder next to `app.py`.
- **`SSL: CERTIFICATE_VERIFY_FAILED` on Mac**: Python can't verify MongoDB's certificate. Run `open "/Applications/Python 3.12/Install Certificates.command"` (change `3.12` to your Python version), then restart the app.
- **`ServerSelectionTimeoutError` with no SSL message**: check your internet connection, and ask a teammate to confirm your IP address is allowed under Network Access in MongoDB Atlas.
- **`ModuleNotFoundError`**: your virtual environment probably isn't active. Activate it (step 3) and run `pip install -r requirements.txt` again.

## Task boards

Each sprint has its own GitHub Project board:

- [Agile Aardvarks - Sprint 1](https://github.com/orgs/software-students-fall2026/projects/4/views/1)
- [Agile Aardvarks - Sprint 2]()