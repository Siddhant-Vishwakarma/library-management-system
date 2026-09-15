# Library Management System — Web (Flask)

A Flask conversion of your CLI library management system. Business logic,
database schema, and access rules all match the original — only the
interface changed from terminal prompts to a browser.

This has been tested end-to-end against a real MySQL/MariaDB instance:
login (admin + member), book CRUD, member management, and the issue/return
flow all work as expected.

## 1. Install dependencies

```bash
cd library_web
pip install -r requirements.txt
```

## 2. Set up the database

Load the corrected schema (fixes two bugs found in the original SQL file --
see "What was fixed" below):

```bash
mysql -u root -p < Library_Management_System_Schema.sql
```

This creates the `library_management` database with sample data:
- Admin login: **admin / admin123**
- Member login: **rahul@gmail.com / password123** (or ankit@gmail.com / password123)

## 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set `DB_PASSWORD` to your real MySQL root password, and
change `SECRET_KEY` to any long random string (used to sign session cookies).

## 4. Run it

```bash
flask --app app run
```

Visit **http://127.0.0.1:5000** and log in with the credentials above.

## Project structure

```
app.py                  Flask app factory, dashboard route
db_context.py           Per-request DB connection + repository wiring
config.py               Loads DB/secret settings from .env
database.py             MySQL connection pool
decorators.py           @login_required / @admin_required
blueprints/
    auth.py              /login, /logout
    books.py             /books/*  (admin only)
    users.py             /members/* (admin only)
    issue.py             /circulation/* (any logged-in user)
models/                 Unchanged from your CLI version
repositories/           Unchanged from your CLI version (2 small fixes, see below)
services/               Rewritten: same logic, now parameter-in/dict-out
                         instead of input()/print()
templates/              Jinja2 HTML
static/css/style.css    Styling
utils/logger.py         Recreated (was referenced but not in your upload)
utils/validation.py     Recreated for web form validation
```

## What was fixed along the way

These were bugs in the original code/schema, not stylistic changes:

1. **`users` table was missing a `password` column** in your SQL file, but
   `user_repository.py` inserts and reads one. Login as a member would have
   errored. Added the column.
2. **Seeded admin password was plaintext** (`'admin123'`), but
   `admin_repository.py` runs stored passwords through `bcrypt.checkpw()`,
   which requires an actual bcrypt hash. Replaced with a real hash.
3. **`Book.__init__`** required `book_id` as a positional argument with no
   default, but `add_book()` constructs a `Book` without passing one --
   this would have raised `TypeError` on every "Add Book". Gave it a
   default of `None`.
4. **`user_repository.view_users()` / `get_user_by_id()`** didn't select
   `user_id`, which the web UI needs for edit/delete links. Added it.
   `get_user_by_id` also used `SELECT *`, which would return the password
   hash to the app layer unnecessarily -- narrowed to explicit columns.
5. **`requirements.txt`** listed `mysql-connector-python==26.7.0`, which
   isn't a real published version. Corrected to `9.0.0`.

## Notes / things worth doing before real deployment

- The dev server (`flask run`) is fine locally but not for production --
  put Gunicorn + Nginx (or a host like Render/Railway) in front of it.
- `issue_service.issue_book()` currently lets any logged-in member issue a
  book to *any* user ID, not just their own -- this matches your original
  CLI's behavior exactly, but you may want to restrict members to their own
  `session['user_id']` for the web version.
- Logs write to `library_web/logs/library.log` (auto-created).
