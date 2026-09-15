from mysql.connector import pooling, Error
from utils.logger import logger
from config import DB_CONFIG

_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="library_pool",
            pool_size=5,
            **DB_CONFIG
        )
    return _pool


def get_connection():
    """
    Borrow a connection from the pool. Caller is responsible for
    closing it (which returns it to the pool) -- in the Flask app
    this happens automatically via the per-request teardown in app.py.
    """
    try:
        return _get_pool().get_connection()
    except Error as e:
        logger.error(f"Database Error: {e}")
        return None


def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
