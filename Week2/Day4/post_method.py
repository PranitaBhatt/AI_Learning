from fastapi import Body,FastAPI
app=FastAPI()
Books=[
    {"Title":"Title1","Author":"Author1","category":"science"},
    {"Title":"Title2","Author":"Author2","category":"science"},
    {"Title":"Title3","Author":"Author3","category":"history"},
    {"Title":"Title4","Author":"Author4","category":"english"},
    {"Title":"Title5","Author":"Author2","category":"history"},
]
@app.get("/books")
async def read_books():
    return Books

@app.post("/books/create_book")   #creating a post request to add a new book to the list of books
async def create_book(new_book=Body()):     #new book is the parameter which we are getting from the body of the request
    Books.append(new_book)      #Additonally we haven't passed a request body here