from utils.logger import logger
from utils.validation import require_non_empty, require_positive_integer
from models.book import Book


class BookService:

    def __init__(self, book_repository):
        self.book_repository = book_repository

    @staticmethod
    def _row_to_dict(row):
        return {
            "book_id": row[0],
            "title": row[1],
            "author": row[2],
            "publisher": row[3],
            "category": row[4],
            "isbn": row[5],
            "total_quantity": row[6],
            "available_quantity": row[7],
            "shelf_no": row[8],
        }

    def add_book(self, title, author, publisher, category, isbn,
                 total_quantity, shelf_no):

        errors = []
        errors.append(require_non_empty(title, "Title"))
        errors.append(require_non_empty(author, "Author"))
        errors.append(require_non_empty(publisher, "Publisher"))
        errors.append(require_non_empty(category, "Category"))
        errors.append(require_non_empty(isbn, "ISBN"))
        errors.append(require_positive_integer(total_quantity, "Total quantity"))
        errors.append(require_non_empty(shelf_no, "Shelf number"))
        errors = [e for e in errors if e]

        if errors:
            return {"success": False, "errors": errors}

        total_quantity = int(total_quantity)

        book = Book(
            title=title,
            author=author,
            publisher=publisher,
            category=category,
            isbn=isbn,
            total_quantity=total_quantity,
            available_quantity=total_quantity,
            shelf_no=shelf_no,
        )

        success = self.book_repository.add_book(book)

        if success:
            return {"success": True, "message": "Book added successfully."}
        return {"success": False, "errors": ["Failed to add book."]}

    def view_books(self):
        books = self.book_repository.get_all_books()

        if books is None:
            return {"success": False, "errors": ["Failed to fetch books."], "books": []}

        logger.info(f"Viewed all books. Total books: {len(books)}")
        return {"success": True, "books": [self._row_to_dict(b) for b in books]}

    def search_book(self, title, author):
        books = self.book_repository.search_books(title or "", author or "")

        if books is None:
            return {"success": False, "errors": ["Failed to search books."], "books": []}

        logger.info(f"Book Search | Title: {title} | Author: {author}")

        results = [
            {
                "book_id": b[0],
                "title": b[1],
                "author": b[2],
                "category": b[3],
                "available_quantity": b[4],
            }
            for b in books
        ]
        return {"success": True, "books": results}

    def get_book(self, book_id):
        book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            return {"success": False, "errors": ["Book not found."]}
        return {"success": True, "book": self._row_to_dict(book)}

    def update_book(self, book_id, title, author, publisher, category, isbn,
                     total_quantity, shelf_no):

        existing = self.book_repository.get_book_by_id(book_id)
        if existing is None:
            logger.warning(f"Update failed. Book ID {book_id} not found.")
            return {"success": False, "errors": ["Book not found."]}

        errors = []
        errors.append(require_non_empty(title, "Title"))
        errors.append(require_non_empty(author, "Author"))
        errors.append(require_non_empty(publisher, "Publisher"))
        errors.append(require_non_empty(category, "Category"))
        errors.append(require_non_empty(isbn, "ISBN"))
        errors.append(require_positive_integer(total_quantity, "Total quantity"))
        errors.append(require_non_empty(shelf_no, "Shelf number"))
        errors = [e for e in errors if e]

        if errors:
            return {"success": False, "errors": errors}

        total_quantity = int(total_quantity)

        # NOTE: matches the original CLI behavior of resetting
        # available_quantity to the new total_quantity on every edit.
        book = Book(
            book_id=book_id,
            title=title,
            author=author,
            publisher=publisher,
            category=category,
            isbn=isbn,
            total_quantity=total_quantity,
            available_quantity=total_quantity,
            shelf_no=shelf_no,
        )

        success = self.book_repository.update_book(book)

        if success:
            logger.info(f"Book Updated | Book ID: {book_id} | Title: {title}")
            return {"success": True, "message": "Book updated successfully."}
        return {"success": False, "errors": ["Failed to update book."]}

    def delete_book(self, book_id):
        book = self.book_repository.get_book_by_id(book_id)

        if book is None:
            logger.warning(f"Delete failed. Book ID {book_id} not found.")
            return {"success": False, "errors": ["Book not found."]}

        success = self.book_repository.delete_book(book_id)

        if success:
            logger.info(f"Book Deleted | Book ID: {book_id} | Title: {book[1]}")
            return {"success": True, "message": "Book deleted successfully."}
        return {"success": False, "errors": ["Failed to delete book."]}
