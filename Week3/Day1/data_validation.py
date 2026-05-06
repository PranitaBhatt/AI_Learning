#Dat Validation using path parameters
from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field
 
app=FastAPI()
 
 
class Books:
    id: int
    title: str
    author: str
    description: str
    rating: int
 
 
    #Constructor is called
    def __init__(self, id, title, author, description, rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
 
 
class BookRequest(BaseModel): #Pydantic model
    #id: Optional[int] = None #we added id as optional so the type can be int or None. Also it will be generated automatically even if we didn't send it in the request body.
    id: Optional[int] = Field(description='id is not needed in request body',default=None)  #This will provide a description
    title: str = Field(min_length=3)  # Field Validation--minimum three characters
    author: str = Field(min_length=1)#minimum one character
    description: str = Field(min_length=3, max_length=100)#minimum three characters and maximum 100 characters
    rating: int = Field(ft=0, lt=6)#range lies from 0 to 5

    model_config={
        "json_schema_extra": {
            "example": {
                "title": "Space",
                "author": "Thomas",
                "description": "Very nice book",
                "rating": 5
            }
        }
    }
 
BOOKS=[
    Books(1, "Space", "Thomas", "Very nice book", 5),
    Books(2, "Space1", "Thomas", "Very classic book", 4),
    Books(3, "Space2", "Thomas", "Average book", 3),
    Books(4, "Hp1", "Thomas", "Good Book", 3),
    Books(5, "Hp2", "Thomas","Can improve", 3)
]
 
 
@app.get("/books")
async def read_all_books():
    return BOOKS

#Creating a new book endpoint
@app.get("/books/{book_id}") #additional path parameter
async def read_book(book_id: int=Path(gt=0)): #validation for path parameter--greater than 0    
    for book in BOOKS:
        if book.id==book_id:
            return book
    return {"error": "Book not found"}      
 
#Fetching book by rating
@app.get("/books/")#no path parameter is used, only query parameter is used
async def read_book_by_rating(book_rating: int):
    books_to_return=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_to_return.append(book)
    return books_to_return

@app.post("/create_book")
async def create_book(book_request: BookRequest): 
    print(type(book_request)) #BookRequest
    new_book = Books(**book_request.dict()) 
    print(type(new_book)) #Books
    BOOKS.append(find_book_id(new_book)) #add new book to list
   
# User sends data
# FastAPI receives it
# Convert to dictionary
# Create Book object
# Add to list
 
def find_book_id(book:Books):
  book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
  return book
'''  if len(BOOKS)>0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1'''

#Adding a PUT request method to update
@app.put("/books/update_book")
async def update_book(book: BookRequest): #here BookRequest is a pydantic model object
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id: #if id matches then update the book
            BOOKS[i]=book
            return BOOKS[i] #return the updated book
        
#Deleting book by id
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i) #remove the book from list
            break