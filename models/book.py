class Book:
    def __init__(self, book_id=None, title=None, author=None, publisher=None,
                 category=None, isbn=None, total_quantity=None,
                 available_quantity=None, shelf_no=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.category = category
        self.isbn = isbn
        self.total_quantity = total_quantity
        self.available_quantity = available_quantity
        self.shelf_no = shelf_no
