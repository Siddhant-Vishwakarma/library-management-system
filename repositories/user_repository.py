import bcrypt
from utils.logger import logger


class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    def add_user(self, user):
        cursor = None

        try:
            cursor = self.connection.cursor()

            hashed_password = bcrypt.hashpw(
                user.password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            query = """
            INSERT INTO users(
            full_name,email,phone,department,password
            )
            VALUES(%s,%s,%s,%s,%s)
            """
            values = (
                user.full_name,
                user.email,
                user.phone,
                user.department,
                hashed_password
            )

            cursor.execute(query, values)

            self.connection.commit()

            logger.info(
                f"User Added | Name: {user.full_name} | "
                f"Department | Department Name: {user.department} | "
            )
            return True

        except Exception as e:

            self.connection.rollback()

            logger.error(f"Error while adding user: {e}")

            return False

        finally:
            if cursor:
                cursor.close()

    def view_users(self):
        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                    SELECT user_id,
                            full_name,
                            email,
                            phone,
                            department
                            FROM users
                    """

            cursor.execute(query)

            users = cursor.fetchall()

            logger.info(
                f"User Viewed Successfully | "
            )
            return users

        except Exception as e:

            logger.error(f"Error while viewing user: {e}")

            return None

        finally:
            if cursor:
                cursor.close()

    def search_users(self, name, email):
        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                SELECT 
                user_id,
                full_name,
                email,
                phone,
                department
                FROM users
                WHERE full_name LIKE %s
                    OR email LIKE %s
                """
            search_name = f"%{name}%"
            search_email = f"%{email}%"

            cursor.execute(query, (search_name, search_email))

            users = cursor.fetchall()

            return users

        except Exception as e:

            logger.error(f"Error while searching user: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

    def authenticate_user(self, email, password):
        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                SELECT user_id, password
                FROM users
                WHERE email = %s
            """
            cursor.execute(query, (email,))

            result = cursor.fetchone()

            if result is None:
                return None

            user_id, stored_hash = result

            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")

            if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                return (user_id,)

            return None

        except Exception as e:
            logger.error(f"Error while authenticating user: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

    def get_user_by_id(self, user_id):
        cursor = None

        try:
            cursor = self.connection.cursor()

            query = "SELECT user_id, full_name, email, phone, department FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))

            return cursor.fetchone()

        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

    def update_user(self, user):

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                UPDATE users
                SET 
                    full_name = %s,
                    email = %s,
                    phone = %s,
                    department = %s
                WHERE user_id = %s
            """
            values = (
                user.full_name,
                user.email,
                user.phone,
                user.department,
                user.user_id
            )
            cursor.execute(query, values)

            self.connection.commit()

            return True

        except Exception as e:

            self.connection.rollback()

            logger.error(
                f"Error while updating user: {e}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

    def delete_user(self, user_id):
        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                DELETE  FROM users
                WHERE user_id = %s 
            """
            cursor.execute(query, (user_id,))

            self.connection.commit()

            return True

        except Exception as e:

            self.connection.rollback()

            logger.error(
                f"Error while deleting user: {e}"
            )

            return False
        finally:
            if cursor:
                cursor.close()
