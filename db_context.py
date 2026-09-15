from flask import g
from database import get_connection

from repositories.admin_repository import AdminRepository
from repositories.user_repository import UserRepository
from repositories.book_repository import BookRepository
from repositories.issue_return_repository import IssueRepository


def get_db():
    """Lazily open one pooled connection per request, reused by all
    repositories touched during that request. Closed automatically
    in app.py's teardown_appcontext handler."""
    if "db" not in g:
        g.db = get_connection()
    return g.db


def get_repos():
    """Build fresh repository instances bound to this request's connection."""
    conn = get_db()
    return {
        "admin": AdminRepository(conn),
        "user": UserRepository(conn),
        "book": BookRepository(conn),
        "issue": IssueRepository(conn),
    }
