from utils.logger import logger


class BookRepository:

    def __init__(self, connection):
        self.connection = connection

    def add_book(self, book):

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                INSERT INTO books
                (
                    title,
                    author,
                    publisher,
                    category,
                    isbn,
                    total_quantity,
                    available_quantity,
                    shelf_no
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                book.title,
                book.author,
                book.publisher,
                book.category,
                book.isbn,
                book.total_quantity,
                book.available_quantity,
                book.shelf_no
            )

            cursor.execute(query, values)

            self.connection.commit()

            logger.info(
                f"Book Added | Title: {book.title} | "
                f"Author: {book.author} | ISBN: {book.isbn}"
            )

            return True

        except Exception as e:

            self.connection.rollback()

            logger.error(f"Error while adding book: {e}")

            return False

        finally:

            if cursor:
                cursor.close()

    def get_all_books(self):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                SELECT
                    book_id,
                    title,
                    author,
                    publisher,
                    category,
                    isbn,
                    total_quantity,
                    available_quantity,
                    shelf_no
                FROM books
            """

            cursor.execute(query)

            books = cursor.fetchall()

            return books

        except Exception as e:

            logger.error(
                f"Error while fetching books: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

    def search_books(self, title, author):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                SELECT
                    book_id,
                    title,
                    author,
                    category,
                    available_quantity
                FROM books
                WHERE title LIKE %s
                OR author LIKE %s
            """

            search_title = f"%{title}%"
            search_author = f"%{author}%"

            cursor.execute(
                query,
                (search_title, search_author)
            )

            books = cursor.fetchall()

            return books

        except Exception as e:

            logger.error(
                f"Error while searching book: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

    def get_book_by_id(self, book_id):
        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                SELECT book_id, title, author, publisher,
                    category, isbn, total_quantity,
                    available_quantity, shelf_no
                FROM books
                WHERE book_id = %s
            """

            cursor.execute(query, (book_id,))

            return cursor.fetchone()

        except Exception as e:
            logger.error(f"Error fetching book: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

    def update_book(self, book):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                UPDATE books
                SET
                    title = %s,
                    author = %s,
                    publisher = %s,
                    category = %s,
                    isbn = %s,
                    total_quantity = %s,
                    available_quantity = %s,
                    shelf_no = %s
                WHERE book_id = %s
            """

            values = (
                book.title,
                book.author,
                book.publisher,
                book.category,
                book.isbn,
                book.total_quantity,
                book.available_quantity,
                book.shelf_no,
                book.book_id
            )

            cursor.execute(query, values)

            self.connection.commit()

            return True

        except Exception as e:

            self.connection.rollback()

            logger.error(
                f"Error while updating book: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

    def delete_book(self, book_id):

        cursor = None

        try:

            cursor = self.connection.cursor()

            query = """
                DELETE FROM books
                WHERE book_id = %s
            """

            cursor.execute(
                query,
                (book_id,)
            )

            self.connection.commit()

            return True

        except Exception as e:

            self.connection.rollback()

            logger.error(
                f"Error while deleting book: {e}"
            )

            return False

        finally:

            if cursor:
                cursor.close()
