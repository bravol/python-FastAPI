from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel,Field
from book import Book


app = FastAPI()

class BookRequest(BaseModel):
    book_id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=100)
    rating: int = Field(gt= -1, lt=6) #rating from 0 to 5



# Initialize the BOOKS list
BOOKS = [
    Book(1, 'Computer Science', 'Lumala Brian', 'description one', 4),
    Book(2, 'Understand Python', 'Lumala Brian', 'description two', 2),
    Book(3, 'Understand Ruby', 'Bravol Brian', 'description three', 5),
    Book(4, 'Be fast with FastAPI', 'Brian Bravol', 'description four', 1),
    Book(5, 'Master Endpoints', 'Joseph Brian', 'description five',5),
    Book(6, 'Computer Science Pro', 'Derrick Brian', 'description six', 3),
]

# Endpoint to retrieve all books
@app.get("/books")
async def read_all_books():
    return BOOKS

# Endpoint to create a new book
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(create_book_id(new_book))


def create_book_id(book:Book):
    if len(BOOKS) > 0:
        book.book_id = BOOKS[-1].book_id + 1
    else:
        book.book_id = 1
    return book