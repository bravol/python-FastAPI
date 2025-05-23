from fastapi import FastAPI,Body

app = FastAPI()

# create a list of books

BOOKS = [
    {"title":"Title One", "author":"Author one", "category":"science"},
    {"title":"Title Two", "author":"Author Two", "category":"science"},
    {"title":"Title Three", "author":"Author Three", "category":"history"},
    {"title":"Title Four", "author":"Author Four", "category":"history"},
    {"title":"Title Five", "author":"Author Five", "category":"math"},
    {"title":"Title Six", "author":"Author Six", "category":"math"},

]

# GET REQUEST used to get data

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


@app.get("/books/by_author/")
async  def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return


# query parameters by author and category filter data based on the url provided.
@app.get('/book/{book_author}/')
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (book.get('author').casefold() == book_author.casefold() and
                book.get('category').casefold() == category.casefold()):
            books_to_return.append(book)
    return  books_to_return

# POST REQUEST used to create data
@app.post('/books/create_book')
async def create_book(new_book = Body()):
    BOOKS.append(new_book)


# PUT REQUEST used to update data
@app.put('/book/update_book')
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

# DELETE REQUEST METHOD used to delete data
@app.delete("/book/delete_book/{book_title}")
async  def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break



# # learning
# def user_dictionary(firstname, lastname, age):
#     created_user_dictionary={
#         "firstname": firstname,
#         "lastname": lastname,
#         'age': age
#     }
#     return created_user_dictionary
#
# solution = user_dictionary("lumala","brian",32)
# print(solution)

marks ={
    "Math":30,
    "English": 50
}

def calculate_homework(homework):
    sum_of_grades=0
    for work in homework.values():
        sum_of_grades += work
    final_grade = round(sum_of_grades / len(homework))
    print(final_grade)

calculate_homework(marks)
