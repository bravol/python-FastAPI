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

# path parameters dynamic
@app.get('/books/{book_title}')
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


# query parameters by category filter data based on the url provided.
@app.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return  books_to_return

# query parameters by author and category filter data based on the url provided.

@app.get('/book/{book_author}/')
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (book.get('author').casefold() == book_author.casefold() and
                book.get('category').casefold() == category.casefold()):
            books_to_return.append(book)
    return  books_to_return