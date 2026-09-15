from utils.logger import logger
from utils.validation import require_non_empty, require_valid_email, require_valid_phone
from models.user import User


class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    @staticmethod
    def _row_to_dict(row):
        return {
            "user_id": row[0],
            "full_name": row[1],
            "email": row[2],
            "phone": row[3],
            "department": row[4],
        }

    def add_user(self, full_name, email, phone, department, password):
        errors = []
        errors.append(require_non_empty(full_name, "Full name"))
        errors.append(require_valid_email(email))
        errors.append(require_valid_phone(phone))
        errors.append(require_non_empty(department, "Department"))
        errors.append(require_non_empty(password, "Password"))
        errors = [e for e in errors if e]

        if errors:
            return {"success": False, "errors": errors}

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            department=department,
            password=password,
        )

        success = self.user_repository.add_user(user)

        if success:
            return {"success": True, "message": "User added successfully."}
        return {"success": False, "errors": ["Failed to add user. Email may already be in use."]}

    def view_users(self):
        users = self.user_repository.view_users()

        if users is None:
            return {"success": False, "errors": ["Failed to fetch users."], "users": []}

        return {"success": True, "users": [self._row_to_dict(u) for u in users]}

    def search_user(self, name, email):
        users = self.user_repository.search_users(name or "", email or "")

        if users is None:
            return {"success": False, "errors": ["Failed to search users."], "users": []}

        if not users:
            logger.warning(f"No user found | Name: {name} | Email: {email}")

        logger.info(f"User Search | Name: {name} | Email: {email}")
        return {"success": True, "users": [self._row_to_dict(u) for u in users]}

    def get_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            return {"success": False, "errors": ["User not found."]}
        return {"success": True, "user": self._row_to_dict(user)}

    def update_user(self, user_id, full_name, email, phone, department):
        existing = self.user_repository.get_user_by_id(user_id)
        if existing is None:
            logger.warning(f"Update failed. User ID {user_id} not found.")
            return {"success": False, "errors": ["User not found."]}

        errors = []
        errors.append(require_non_empty(full_name, "Full name"))
        errors.append(require_valid_email(email))
        errors.append(require_valid_phone(phone))
        errors.append(require_non_empty(department, "Department"))
        errors = [e for e in errors if e]

        if errors:
            return {"success": False, "errors": errors}

        user = User(
            user_id=user_id,
            full_name=full_name,
            email=email,
            phone=phone,
            department=department,
        )

        success = self.user_repository.update_user(user)

        if success:
            logger.info(f"User Updated | User ID: {user_id} | Name: {full_name}")
            return {"success": True, "message": "User updated successfully."}
        return {"success": False, "errors": ["Failed to update user."]}

    def delete_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            logger.warning(f"Delete failed. User ID {user_id} not found.")
            return {"success": False, "errors": ["User not found."]}

        success = self.user_repository.delete_user(user_id)

        if success:
            logger.info(f"User Deleted | User ID: {user_id} | Name: {user[1]}")
            return {"success": True, "message": "User deleted successfully."}
        return {"success": False, "errors": ["Failed to delete user."]}
