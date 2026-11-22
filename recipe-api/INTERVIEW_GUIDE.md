# Interview Guide: Recipe Management API

Simple English notes to explain this project with confidence.

---

## 1. Explain the project in 30 seconds
"I built a Recipe Management API using FastAPI and PostgreSQL. A client can
create, view, update, delete and search recipes. Each recipe has a list of
ingredients. I added validation, pagination, proper error codes and automated
tests. I also wrote documentation so anyone can run the project easily."

## 2. Explain your resume lines
**"REST API endpoints for managing recipes, built with FastAPI and PostgreSQL."**
> I made endpoints like POST /recipes and GET /recipes/{id}. They follow REST rules:
> URLs are nouns, HTTP methods show the action, and status codes show the result.

**"Practiced API testing, debugging, backend configuration and project documentation."**
> - *Testing:* I wrote pytest tests for success cases and error cases.
> - *Debugging:* I fixed problems like database connection errors and validation errors by reading logs and error messages.
> - *Configuration:* I kept the database URL in a `.env` file, not in the code.
> - *Documentation:* I wrote a README with setup steps and examples, and FastAPI gives automatic Swagger docs.

---

## 3. Key words in simple language
| Word | Easy meaning |
|------|--------------|
| API | A way for two programs to talk to each other |
| REST | A common style for designing APIs using URLs and HTTP methods |
| Endpoint | One URL that does one job, like `/recipes` |
| FastAPI | A Python tool to build APIs quickly |
| PostgreSQL | A database that stores data in tables |
| ORM (SQLAlchemy) | Lets me use Python classes instead of writing SQL |
| Model | A Python class that represents a database table |
| Schema (Pydantic) | A rule list for what data is allowed in a request or response |
| CRUD | Create, Read, Update, Delete |
| Session | One connection "conversation" with the database |
| Dependency Injection | FastAPI automatically gives a function what it needs (like a database session) |
| Migration | A tracked change to the database structure (Alembic does this) |
| Pagination | Returning data in small pages instead of all at once |

---

## 4. HTTP methods and status codes
| Action | Method | Success code |
|--------|--------|--------------|
| Create | POST | 201 Created |
| Read | GET | 200 OK |
| Update | PUT | 200 OK |
| Delete | DELETE | 204 No Content |

| Error | Meaning |
|-------|---------|
| 404 | The recipe does not exist |
| 422 | The data sent is invalid |
| 500 | A bug on the server |

---

## 5. What happens when a request comes in (step by step)
Example: `POST /recipes`
1. **Uvicorn** receives the HTTP request and gives it to FastAPI.
2. **FastAPI** finds the matching route in `routers/recipes.py`.
3. **Pydantic schema** (`RecipeCreate`) checks the data. Bad data gets a 422 error here.
4. **Dependency** `get_db` opens a database session.
5. The route calls **`crud.create_recipe`**.
6. **CRUD** builds the model objects and saves them with SQLAlchemy to PostgreSQL.
7. The saved recipe is converted using the **`RecipeOut` schema** into JSON.
8. The client receives the response with status 201.

---

## 6. What each file does
- **`main.py`**: Creates the FastAPI app, creates tables at startup, adds the routes.
- **`config.py`**: Reads the database URL from `.env`. This keeps secrets out of the code.
- **`database.py`**: Creates the engine (connection) and the session. `get_db` opens a session per request and always closes it.
- **`models.py`**: Defines the tables `recipes` and `ingredients` and their one-to-many relation.
- **`schemas.py`**: Defines the shape of input and output data, with rules (for example servings must be at least 1).
- **`crud.py`**: All database logic: create, get, list with filters, update, delete.
- **`routers/recipes.py`**: The endpoints. They are short because the real work is in `crud.py`.
- **`tests/`**: Automatic tests.

---

## 7. Design decisions (and why)
1. **Separate files for models, schemas, crud, routes.**
   Each file has one job. The code is easy to read, test and change.
2. **Separate models and schemas.**
   Models describe the database. Schemas describe the API. They can change independently, and I never leak internal details.
3. **Two tables (recipes and ingredients).**
   A recipe has many ingredients, so one table with a list would be bad design. This is a proper one-to-many relation with a foreign key.
4. **Cascade delete.**
   If a recipe is deleted, its ingredients are deleted too, so no orphan rows remain.
5. **PUT with optional fields.**
   The client sends only the fields it wants to change. I use `exclude_unset=True` to detect this.
6. **Reusable `get_recipe_or_404` dependency.**
   GET one, PUT and DELETE all need "find recipe or return 404". I wrote it once and reused it.
7. **Tests use SQLite in memory.**
   Tests are fast and do not damage real data. I override the `get_db` dependency to do this.
8. **Pagination with limit max 100.**
   Prevents someone from asking for a huge amount of data at once.

---

## 8. Testing: what I tested
- Health check works
- Create recipe returns 201 and the saved data
- Invalid data returns 422
- Get one recipe works, missing recipe returns 404
- List, search, category filter, pagination
- Partial update keeps other fields unchanged
- Update replaces ingredients
- Update or delete of a missing recipe returns 404
- Delete works, and the recipe is gone afterwards

Run with: `pytest -v`

---

## 9. Debugging stories you can tell (real situations this setup can cause)
1. **Connection refused:** The API could not connect to PostgreSQL because the container was not running. I checked with `docker ps`, started it with `docker compose up -d`.
2. **422 errors:** My JSON was missing a required field. I read the `detail` in the response; it shows exactly which field is wrong.
3. **Wrong database URL:** Password or database name did not match. I checked `.env` against `docker-compose.yml`.
4. **Import errors:** I ran commands from the wrong folder. Running from the project root fixed it.

Tip: say *how* you found the problem (read the error, checked logs, tested the endpoint in Swagger).

---

## 10. Likely interview questions and easy answers

**Q: Why FastAPI?**
It is fast, has automatic validation with Pydantic, and creates interactive docs at `/docs` without extra work.

**Q: Why PostgreSQL?**
Recipes and ingredients are structured data with relationships. A relational database fits this well, and PostgreSQL is reliable and popular.

**Q: What is the difference between a model and a schema?**
A model is a database table in Python. A schema checks the data coming in and going out of the API.

**Q: What is a foreign key?**
A column that links one table to another. `ingredients.recipe_id` points to `recipes.id`.

**Q: What is a session and why close it?**
A session is a database conversation. If it is not closed, connections stay open and the database can run out of connections. My `get_db` closes it in a `finally` block.

**Q: PUT vs PATCH?**
Strictly, PUT replaces the whole resource and PATCH changes part of it. My PUT accepts partial updates, which behaves like PATCH. I can say this honestly and add a PATCH route easily if needed.

**Q: How do you handle errors?**
Pydantic returns 422 for invalid input, and I raise `HTTPException` with 404 when a recipe is missing.

**Q: How do you keep secrets safe?**
The database URL is in `.env`, which is in `.gitignore`. Only `.env.example` is committed.

**Q: How would you handle database changes later?**
Use Alembic migrations. Right now tables are created at startup with `create_all`, which is fine for a small project but does not handle changes to existing tables.

**Q: How would you improve it?**
Add JWT login, Alembic migrations, a Dockerfile for the API, caching, and full-text search.

**Q: How would you scale it?**
Run several API instances behind a load balancer, add database indexes (I already index title and category), and add caching for frequent reads.

**Q: What is dependency injection in your project?**
`Depends(get_db)` gives each route a database session without the route creating it. It also makes testing easy because I can replace it with a test database.

---

## 11. Honest limitations (good to say in an interview)
- No user login yet.
- Tables are created with `create_all`, not migrations.
- Search is a simple title match (`ILIKE`).

Saying limitations with a plan to fix them shows maturity.

---

## 12. Quick demo plan (2 minutes)
1. Start PostgreSQL: `docker compose up -d`
2. Start the API: `uvicorn app.main:app --reload`
3. Open `/docs` in the browser.
4. Create a recipe with POST.
5. Fetch it with GET, search with `?search=`.
6. Update it with PUT and delete it with DELETE.
7. Show a 404 and a 422 error.
8. Run `pytest -v` and show the tests passing.
