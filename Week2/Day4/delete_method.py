from fastapi import Body,FastAPI
app=FastAPI()
Books=[
    {"Title":"Title1","Author":"Author1","category":"science"},
    {"Title":"Title2","Author":"Author2","category":"science"},
    {"Title":"Title3","Author":"Author3","category":"history"},
    {"Title":"Title4","Author":"Author4","category":"english"},
    {"Title":"Title5","Author":"Author2","category":"history"},
]
#GET
@app.get("/books")
async def read_books():
    return Books
#POST
@app.post("/books/create_book")   #creating a post request to add a new book to the list of books
async def create_book(new_book=Body()):     #new book is the parameter which we are getting from the body of the request
    Books.append(new_book) 
#PUT
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(Books)):
        if Books[i].get('Title').casefold()==updated_book.get('Title').casefold():  #via indexing it updates the value of the book
            Books[i]=updated_book
            
#DELETE
@app.delete("/books/delete_book/{book_title}") #here we have .deleted method with respect to our API endpoint and we are passing the book title as a path parameter
async def delete_book(book_title:str):
    for i in range(len(Books)):
        if Books[i].get("Title").casefold()==book_title.casefold():
            Books.pop(i)  #pop method is used to remove the book from the list of books via indexing
            break