from fastapi import FastAPI
app=FastAPI()
Books=[
    {"Title":"Title1","Author":"Author1","category":"science"},
    {"Title":"Title2","Author":"Author2","category":"science"},
    {"Title":"Title3","Author":"Author3","category":"history"},
    {"Title":"Title4","Author":"Author4","category":"english"},
    {"Title":"Title5","Author":"Author5","category":"science"},
]
'''
Simply making a  get request
@app.get("/api-endpoint")
async def first_api():
    return{"message":"Hey This is my FirstAPI Program"}'''
 
#Implementing for the books
@app.get("/mybook")      #Requesting
async def read_all_books():
    return {"book_title":"My Book"}

''' ---Added to know the concept of chronological order of the API endpoints
@app.get("/books/mybook")
async def read_all_books():
    return {'book_title':"My Book"}'''
 
'''#Adding a function with dynamic parameter
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param: str):
    return{"dynamic_param":dynamic_param}'''

#Adding path parameters to get the title of the book
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in Books:
        if book.get('title').casefold() == book_title.casefold():
            return book