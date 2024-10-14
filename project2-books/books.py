from fastapi import FastAPI

app = FastAPI()

# create a list of books

BOOKS = [
    {'title':'Title One', 'author':'Author one', 'category':'science'},
    {'title':'Title Two', 'author':'Author Two', 'category':'science'},
    {'title':'Title Three', 'author':'Author Three', 'category':'history'},
    {'title':'Title Four', 'author':'Author Four', 'category':'history'},
    {'title':'Title Five', 'author':'Author Five', 'category':'math'},
    {'title':'Title Six', 'author':'Author Six', 'category':'math'},

]

@app.get("/books")
async def read_all_books():
    return BOOKS



@app.get('/books/mybook')
async def read_all_books():
    return {'book_title':'my favorite book!'}

@app.get('/books/{book_title}')
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

