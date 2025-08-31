# DELETE

from bookshelf.models import Book
book = Book.objects.get(id=1)
book.delete() # Expected: (1, {'bookshelf.Book': 1})
