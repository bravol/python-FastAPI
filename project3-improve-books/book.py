
from pydantic import BaseModel


class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: int
    published_date = int

    def __init__(self, book_id, title, author, description, rating, published_date ):
        self.book_id = book_id
        self.title = title
        self.description = description
        self. rating = rating
        self.author = author
        self.published_date = published_date

