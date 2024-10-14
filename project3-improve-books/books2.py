from fastapi import  FastAPI, Body

from book import Book

app = FastAPI()

book1 = Book(1,'Computer Science','Lumala Brian', 'description one', 4)
book2 = Book(2,'Understand Python','Lumala Brian', 'description two', 2)
book3 = Book(3,'Understand Ruby','Bravol Brian', 'description three', 5)
book4 = Book(4,'Be fast with FastAPI','Brian Bravol', 'description four', 1)
book5 = Book(5,'Master Endpoints','Joseph Brian', 'description five', 5)
book6 = Book(6,'computer science Pro','Derrick Brian', 'description six', 3)


BOOKS = [book1, book2, book3, book4, book5, book6]




@app.get("/books")
async def read_all_books():
    return BOOKS