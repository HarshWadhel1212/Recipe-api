# Recipe Management API

A REST API to create, read, update, delete and search recipes.
Built with **FastAPI** (Python) and **PostgreSQL**.

## Features
- Full CRUD for recipes (Create, Read, Update, Delete)
- Each recipe has many ingredients
- Search by title and filter by category
- Pagination (`skip` and `limit`)
- Input validation with clear error messages
- Automatic interactive docs (Swagger UI)
- Automated tests with pytest

## Tech Stack
| Tool | Why we use it |
|------|---------------|
| FastAPI | Fast, modern Python web framework |
| PostgreSQL | Reliable relational database |
| SQLAlchemy | Lets us use Python classes instead of raw SQL |
| Pydantic | Validates request and response data |
| Uvicorn | Server that runs the FastAPI app |
| Pytest | Testing |
| Docker Compose | Starts PostgreSQL with one command |

## Project Structure
```
recipe-api/
├── app/
│   ├── main.py          # Starts the app, adds routes
│   ├── config.py        # Reads settings (database URL)
│   ├── database.py      # Database connection and sessions
│   ├── models.py        # Database tables (Recipe, Ingredient)
│   ├── schemas.py       # Data validation (request/response shapes)
│   ├── crud.py          # Database operations
│   └── routers/
│       └── recipes.py   # API endpoints
├── tests/
│   ├── conftest.py      # Test setup (temporary database)
│   └── test_recipes.py  # Test cases
├── docker-compose.yml   # PostgreSQL container
├── requirements.txt     # Python packages
└── .env.example         # Example settings
```

## How to Run

**1. Create a virtual environment and install packages**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Start PostgreSQL**
```bash
docker compose up -d
```
(No Docker? Install PostgreSQL yourself, create a database named `recipe_db`,
and put your connection string in `.env`.)

**3. Create the settings file**
```bash
cp .env.example .env
```

**4. Start the API**
```bash
uvicorn app.main:app --reload
```
Open **http://127.0.0.1:8000/docs** to try every endpoint in the browser.
The tables are created automatically on startup.

## API Endpoints
| Method | URL | What it does | Success code |
|--------|-----|--------------|--------------|
| GET | `/health` | Check the API is running | 200 |
| POST | `/recipes` | Create a recipe | 201 |
| GET | `/recipes` | List recipes (`search`, `category`, `skip`, `limit`) | 200 |
| GET | `/recipes/{id}` | Get one recipe | 200 |
| PUT | `/recipes/{id}` | Update a recipe (send only changed fields) | 200 |
| DELETE | `/recipes/{id}` | Delete a recipe | 204 |

Error codes: `404` recipe not found, `422` invalid input.

### Example: create a recipe
```bash
curl -X POST http://127.0.0.1:8000/recipes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pancakes",
    "instructions": "Mix everything. Fry on a pan.",
    "category": "Breakfast",
    "prep_time_minutes": 10,
    "cook_time_minutes": 15,
    "servings": 4,
    "ingredients": [
      {"name": "Flour", "quantity": "2 cups"},
      {"name": "Milk", "quantity": "1 cup"}
    ]
  }'
```

### Example: search and filter
```bash
curl "http://127.0.0.1:8000/recipes?search=pan&category=Breakfast&limit=5"
```

## Run the Tests
```bash
pytest -v
```
Tests use an in-memory SQLite database, so they are fast and do not touch your PostgreSQL data.

## Database Design
```
recipes (1) ────< (many) ingredients
```
- `recipes`: id, title, description, instructions, category, prep_time_minutes,
  cook_time_minutes, servings, created_at, updated_at
- `ingredients`: id, recipe_id (foreign key), name, quantity
- Deleting a recipe also deletes its ingredients (cascade).

## Common Problems and Fixes
| Problem | Fix |
|---------|-----|
| `connection refused` on port 5432 | PostgreSQL is not running. Run `docker compose up -d` |
| `password authentication failed` | Check `DATABASE_URL` in `.env` |
| `ModuleNotFoundError: app` | Run commands from the project root folder |
| `422 Unprocessable Entity` | Your JSON is invalid. Read the `detail` field in the response |
| Tables missing | Restart the server; tables are created on startup |

## Future Improvements
- Alembic for database migrations
- User login with JWT
- Image upload for recipes
- Docker image for the API itself
