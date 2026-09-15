from utils.logger import logger


class IssueRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_user(self, user_id):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                SELECT full_name
                FROM users
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (user_id,)
            )

            return cursor.fetchone()

        except Exception as e:

            logger.error(
                f"Error while checking user: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

    def get_book(self, book_id):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                SELECT
                    title,
                    available_quantity
                FROM books
                WHERE book_id = %s
            """

            cursor.execute(
                query,
                (book_id,)
            )

            return cursor.fetchone()

        except Exception as e:

            logger.error(
                f"Error while checking book: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

    def issue_book(self, issued_book):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                INSERT INTO issued_books
                (
                    user_id,
                    book_id,
                    issue_date,
                    due_date
                )
                VALUES (%s, %s, %s, %s)
            """

            values = (
                issued_book.user_id,
                issued_book.book_id,
                issued_book.issue_date,
                issued_book.due_date
            )

            cursor.execute(query, values)

            update_query = """
                UPDATE books
                SET available_quantity =
                    available_quantity - 1
                WHERE book_id = %s
            """

            cursor.execute(
                update_query,
                (issued_book.book_id,)
            )

            self.connection.commit()

            return True

        except Exception as e:

            self.connection.rollback()

            logger.error(
                f"Error while issuing book: {e}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

    def get_all_issued_books(self):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                SELECT
                    ib.issue_id,
                    u.full_name,
                    b.title,
                    ib.issue_date,
                    ib.due_date,
                    ib.return_date,
                    ib.status
                FROM issued_books ib
                INNER JOIN users u
                    ON ib.user_id = u.user_id
                INNER JOIN books b
                    ON ib.book_id = b.book_id
                ORDER BY ib.issue_id
            """

            cursor.execute(query)

            return cursor.fetchall()

        except Exception as e:

            logger.error(
                f"Error while fetching issued books: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

    def get_issue_by_id(self, issue_id):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                SELECT
                    book_id,
                    due_date,
                    status
                FROM issued_books
                WHERE issue_id = %s
            """

            cursor.execute(
                query,
                (issue_id,)
            )

            return cursor.fetchone()

        except Exception as e:

            logger.error(
                f"Error while getting issue record: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

    def return_book(self, issue_id, book_id, return_date, fine):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                UPDATE issued_books
                SET
                    return_date = %s,
                    fine = %s,
                    status = 'Returned'
                WHERE issue_id = %s
            """

            cursor.execute(
                query,
                (
                    return_date,
                    fine,
                    issue_id
                )
            )

            update_book_query = """
                UPDATE books
                SET available_quantity =
                    available_quantity + 1
                WHERE book_id = %s
            """

            cursor.execute(
                update_book_query,
                (book_id,)
            )

            self.connection.commit()

            return True

        except Exception as e:

            self.connection.rollback()

            logger.error(
                f"Error while returning book: {e}"
            )

            return False

        finally:

            if cursor:
                cursor.close()
