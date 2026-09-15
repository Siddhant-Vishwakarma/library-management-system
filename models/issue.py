class IssueBook:
    def __init__(self, issue_id=None, user_id=None, book_id=None,
                 issue_date=None, due_date=None, return_date=None):
        self.issue_id = issue_id
        self.user_id = user_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date
