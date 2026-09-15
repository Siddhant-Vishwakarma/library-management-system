class User:

    def __init__(self, user_id=None, full_name=None, email=None, phone=None,
                 department=None, password=None):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.department = department
        self.password = password
