# Book Management API

A FastAPI application for managing books, reviews, and recommendations with AI-powered summaries.

---

## Prerequisites

- Python >= 3.12
- PostgreSQL installed
- pip (comes with Python)
- `virtualenv` (optional)

---

## Quick Setup

# ----------------------------------------
# 1. Clone the repository
# ----------------------------------------
git clone https://github.com/ankitmahajan-07/books-management
cd books-management

# ----------------------------------------
# 2. Create virtual environment & activate
# ----------------------------------------
python -m venv .venv

# Activate:
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

# ----------------------------------------
# 3. Upgrade pip & install dependencies
# ----------------------------------------
pip install --upgrade pip
pip install -r requirements.txt

# ----------------------------------------
# 4. Copy .env.example to .env
# ----------------------------------------
# Windows:
copy .env.example .env
# Linux/macOS:
# cp .env.example .env

# ----------------------------------------
# 5. Create PostgreSQL database
# ----------------------------------------
# Open psql or pgAdmin and run:
# CREATE DATABASE books;

# ----------------------------------------
# 6. Run Alembic migrations
# ----------------------------------------
alembic upgrade head

# ----------------------------------------
# 7. Add Groq API key to .env
# ----------------------------------------
Generate Groq API Key - https://console.groq.com/keys
Sign in or create an account.
Click Create API Key and copy it.
# Open .env and set:
# GROQ_API_KEY=your_groq_api_key_here

# ----------------------------------------
# 8. Start the FastAPI server
# ----------------------------------------
uvicorn app.main:app --reload

# ----------------------------------------
# 9. Open documentation
# ----------------------------------------
# Swagger docs: http://127.0.0.1:8000/docs
