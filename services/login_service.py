from utils.logger import logger


class LoginService:
    def __init__(self, admin_repository, user_repository):
        self.admin_repository = admin_repository
        self.user_repository = user_repository

    def login(self, username, password):
        """
        Tries admin login first (username-based),
        then falls back to user login (email-based).

        Returns a dict:
            {"success": True/False, "role": "admin"/"user"/None, "id": <id or None>}
        """
        admin = self.admin_repository.authenticate(username, password)

        if admin:
            logger.info(f"Admin Login Successful | username: {username}")
            return {"success": True, "role": "admin", "id": admin[0]}

        user = self.user_repository.authenticate_user(username, password)

        if user:
            logger.info(f"User Login Successful | email: {username}")
            return {"success": True, "role": "user", "id": user[0]}

        logger.warning(f"Login Failed | username/email: {username}")

        return {"success": False, "role": None, "id": None}
