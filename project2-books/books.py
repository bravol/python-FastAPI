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

@app.get('/books/{dynamic_param}')
async def read_all_books(dynamic_param:str):
    return {'dynamic_param':dynamic_param}