from fastapi import FastAPI, Body
from book import Book


app = FastAPI()


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
async def create_book(book_request = Body()):
    BOOKS.append(book_request)
