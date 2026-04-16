# Zen Log

A personal wellness tracking web app built with Flask and PostgreSQL. Track your daily mood, sleep, exercise, meditation, habits, and journal entries — then explore your patterns through an insights dashboard.

## Features

- **Daily Tracker** — Log mood (0–100 slider), sleep times, exercise minutes, meditation minutes, and a journal entry for each day
- **Habit Tracking** — Create habits, track daily completions, view current streaks and longest streaks, pause and resume habits with full period history
- **Journal** — Write and search through personal journal entries
- **Calendar** — Visual month view of tracked days colour-coded by mood
- **Insights** — Mood trend over time, average mood by day of week, habit completion rates, best/worst week averages, and correlation analysis (mood vs sleep, exercise, meditation, productivity)
- **Meditations** — Browse and play guided meditation audio
- **Home Dashboard** — Greeting, 7-day mood dots, habit streaks, and all-time stats switchable between last week, month, year, and all time

## Tech Stack

- **Backend** — Python, Flask 3.1.3
- **Database** — PostgreSQL (psycopg2)
- **Frontend** — Jinja2 templates, vanilla JS, Chart.js
- **Auth** — Flask sessions, bcrypt password hashing, email verification via SendGrid
- **Security** — Flask-WTF CSRF protection, Flask-Limiter rate limiting
- **Deployment** — Railway, served with Gunicorn

## Local Setup

**Prerequisites:** Python 3.10+, PostgreSQL

1. Clone the repo and create a virtual environment:
   ```bash
   git clone <repo-url>
   cd Startup
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/zenlog
   SECRET_KEY=your-secret-key
   SENDGRID_API_KEY=your-sendgrid-key
   BASE_URL=http://localhost:5000
   ```

4. Initialise the database:
   ```bash
   python -c "from Backend.database.creating_tables import create_tables; create_tables()"
   ```

5. Run the app:
   ```bash
   flask run
   ```

## Deployment

The app is deployed on [Railway](https://railway.app). Pushes to `main` deploy automatically. The `Procfile` runs Gunicorn with 4 workers:

```
web: gunicorn -w 4 --timeout 60 main:app
```

Set the same environment variables from the local setup in the Railway project settings.
