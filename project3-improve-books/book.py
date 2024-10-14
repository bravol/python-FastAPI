from fastapi import  FastAPI, Body

app = FastAPI()

class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, book_id, title, author, description, rating ):
        self.book_id = book_id
        self.title = title
        self.description = description
        self. rating = rating
        self.author = author