from typing import Optional

from fastapi import FastAPI
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
 
@app.post("/create_book")
async def create_book(book_request: BookRequest): #book_request is parameter of type BookRequest which is a Pydantic model. 
    # ** takes key-value from book request to book constructor
    # Accept any number of named arguments (key-value pairs)
    print(type(book_request)) #BookRequest
    new_book = Books(**book_request.dict()) #Unpack dictionary into arguments and convert it to a Book object
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