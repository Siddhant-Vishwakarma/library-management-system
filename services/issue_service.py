from datetime import date, timedelta
from utils.logger import logger
from utils.validation import require_non_empty
from models.issue import IssueBook


class IssueService:

    def __init__(self, issue_repository):
        self.issue_repository = issue_repository

    def issue_book(self, user_id, book_id):
        errors = []
        errors.append(require_non_empty(user_id, "User ID"))
        errors.append(require_non_empty(book_id, "Book ID"))
        errors = [e for e in errors if e]
        if errors:
            return {"success": False, "errors": errors}

        user = self.issue_repository.get_user(user_id)
        if user is None:
            logger.warning(f"Issue failed. User ID {user_id} not found.")
            return {"success": False, "errors": ["User not found."]}

        book = self.issue_repository.get_book(book_id)
        if book is None:
            logger.warning(f"Issue failed. Book ID {book_id} not found.")
            return {"success": False, "errors": ["Book not found."]}

        title, available = book[0], book[1]

        if available <= 0:
            logger.warning(f"Book unavailable. Book ID: {book_id}")
            return {"success": False, "errors": ["Book is not available."]}

        issue_date = date.today()
        due_date = issue_date + timedelta(days=15)

        issued_book = IssueBook(
            user_id=user_id,
            book_id=book_id,
            issue_date=issue_date,
            due_date=due_date,
        )

        success = self.issue_repository.issue_book(issued_book)

        if not success:
            return {"success": False, "errors": ["Failed to issue book."]}

        logger.info(f"Book Issued | User ID: {user_id} | Book ID: {book_id}")

        return {
            "success": True,
            "message": "Book issued successfully.",
            "issue": {
                "user": user[0],
                "book": title,
                "issue_date": issue_date,
                "due_date": due_date,
            },
        }

    def view_issued_books(self):
        records = self.issue_repository.get_all_issued_books()

        if records is None:
            return {"success": False, "errors": ["Failed to fetch issued books."], "records": []}

        results = [
            {
                "issue_id": r[0],
                "user": r[1],
                "book": r[2],
                "issue_date": r[3],
                "due_date": r[4],
                "return_date": r[5],
                "status": r[6],
            }
            for r in records
        ]
        return {"success": True, "records": results}

    def return_book(self, issue_id, book_id, return_date, fine):
        errors = []
        errors.append(require_non_empty(issue_id, "Issue ID"))
        errors.append(require_non_empty(book_id, "Book ID"))
        errors.append(require_non_empty(return_date, "Return date"))
        errors = [e for e in errors if e]

        try:
            fine_value = float(fine) if fine not in (None, "") else 0.0
        except ValueError:
            errors.append("Fine must be a number.")
            fine_value = 0.0

        if errors:
            return {"success": False, "errors": errors}

        result = self.issue_repository.return_book(
            issue_id, book_id, return_date, fine_value
        )

        if result:
            return {"success": True, "message": "Book returned successfully."}
        return {"success": False, "errors": ["Failed to return book."]}
