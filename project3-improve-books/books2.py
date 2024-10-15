from typing import Optional

from fastapi import FastAPI,Path,Query
from pydantic import BaseModel,Field
from book import Book


app = FastAPI()

class BookRequest(BaseModel):
    # book_id: Optional[int] = None
    book_id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=100)
    rating: int = Field(gt=0, lt=6) #rating from 1 to 5
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example":{
                "title": "A new book",
                "author": "Codding challenge",
                "description": "A new description of a book",
                "rating":5,
                "published_date": 2030
            }
        }
    }




# Initialize the BOOKS list
BOOKS = [
    Book(1, 'Computer Science', 'Lumala Brian', 'description one', 4, 2000),
    Book(2, 'Understand Python', 'Lumala Brian', 'description two', 2,2001),
    Book(3, 'Understand Ruby', 'Bravol Brian', 'description three', 5,2002),
    Book(4, 'Be fast with FastAPI', 'Brian Bravol', 'description four', 1,2003),
    Book(5, 'Master Endpoints', 'Joseph Brian', 'description five',5,2004),
    Book(6, 'Computer Science Pro', 'Derrick Brian', 'description six', 3,2005),
]

# Endpoint to retrieve all books
@app.get("/books")
async def read_all_books():
    return BOOKS


# getting a single book path parameter
@app.get("/books/{book_id}")
async  def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.book_id == book_id:
            return book

# get book by rating query parameter
@app.get("/books/")
async  def read_book_by_rating(book_rating: int = Query(gt=0,lt=6)):
    books_to_return =[]
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/")
async def read_book_by_published_date(published_date: int = Query(gt=1999,lt=2031)):
    books_to_return =[]
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return  books_to_return


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

# update the book
@app.put("/books/update-book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book.book_id:
            BOOKS[i] = book

# path parameter
@app.delete("/book/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book_id:
            BOOKS.pop()
            break