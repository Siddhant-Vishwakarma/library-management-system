from flask import Blueprint, render_template, request, redirect, url_for, flash

from db_context import get_repos
from services.book_service import BookService
from decorators import admin_required

books_bp = Blueprint("books", __name__)


def _service():
    return BookService(get_repos()["book"])


@books_bp.route("/")
@admin_required
def list_books():
    result = _service().view_books()
    if not result["success"]:
        for e in result["errors"]:
            flash(e, "error")
    return render_template("books/list.html", books=result.get("books", []))


@books_bp.route("/search")
@admin_required
def search_books():
    title = request.args.get("title", "")
    author = request.args.get("author", "")
    books = []
    if title or author:
        result = _service().search_book(title, author)
        if not result["success"]:
            for e in result["errors"]:
                flash(e, "error")
        books = result.get("books", [])
    return render_template("books/search.html", books=books, query={"title": title, "author": author})


@books_bp.route("/add", methods=["GET", "POST"])
@admin_required
def add_book():
    if request.method == "POST":
        f = request.form
        result = _service().add_book(
            title=f.get("title", "").strip(),
            author=f.get("author", "").strip(),
            publisher=f.get("publisher", "").strip(),
            category=f.get("category", "").strip(),
            isbn=f.get("isbn", "").strip(),
            total_quantity=f.get("total_quantity", ""),
            shelf_no=f.get("shelf_no", "").strip(),
        )
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("books.list_books"))
        for e in result["errors"]:
            flash(e, "error")
        return render_template("books/form.html", book=None, form=f)

    return render_template("books/form.html", book=None, form={})


@books_bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_book(book_id):
    service = _service()

    if request.method == "POST":
        f = request.form
        result = service.update_book(
            book_id=book_id,
            title=f.get("title", "").strip(),
            author=f.get("author", "").strip(),
            publisher=f.get("publisher", "").strip(),
            category=f.get("category", "").strip(),
            isbn=f.get("isbn", "").strip(),
            total_quantity=f.get("total_quantity", ""),
            shelf_no=f.get("shelf_no", "").strip(),
        )
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("books.list_books"))
        for e in result["errors"]:
            flash(e, "error")
        return render_template("books/form.html", book={"book_id": book_id, **f.to_dict()}, form=f)

    result = service.get_book(book_id)
    if not result["success"]:
        for e in result["errors"]:
            flash(e, "error")
        return redirect(url_for("books.list_books"))

    return render_template("books/form.html", book=result["book"], form={})


@books_bp.route("/<int:book_id>/delete", methods=["POST"])
@admin_required
def delete_book(book_id):
    result = _service().delete_book(book_id)
    if result["success"]:
        flash(result["message"], "success")
    else:
        for e in result["errors"]:
            flash(e, "error")
    return redirect(url_for("books.list_books"))
