from utils.logger import logger
import bcrypt


class AdminRepository:

    def __init__(self, connection):
        self.connection = connection

    def authenticate(self, username, password):

        cursor = None

        try:
            cursor = self.connection.cursor()

            query = """
                SELECT admin_id,
                password
                FROM admins
                WHERE username = %s
            """

            cursor.execute(
                query,
                (username,)
            )

            admin = cursor.fetchone()

            if admin is None:
                return None

            admin_id, stored_hash = admin

            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")

            if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                return (admin_id,)

            return None

        except Exception as e:

            logger.error(
                f"Authentication error: {e}"
            )

            return None

        finally:

            if cursor:
                cursor.close()
