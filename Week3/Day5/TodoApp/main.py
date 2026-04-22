from fastapi import FastAPI, Depends, HTTPException, status, Path
import models
from models import Todos
from database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db #yield is similar to that of return function which is used to return a value, here we referred it for code priority
    finally:
        db.close() #and after getting a response  this stmt is executed when we fetched info from db, return it to clien with yeild db and close the connection of db

db_depedency=Annotated[Session,Depends(get_db)] #assigning depedency to a variable for injection usability

#Adding a pydantic model for request body validation and response model
class TodoRequest(BaseModel):
    #id is not passed as it is auto incremented in db and which will be uniquely generated 
    title:str=Field(min_length=1) 
    description:str=Field(min_length=3)
    priority:int=Field(gt=0, lt=6)
    completed:bool
    

'''
An Optional similar method
#creating a first api endpoint
@app.get("/")
async def read_all(db: Annotated[Session,Depends(get_db)]): #Dependency Injection is when something your code needs is given to it instead of being created inside it. 
    return db.query(Todos).all() #this will return all the records in the todos table of our database, and it will be returned as a response to the client when they make a GET request to the root endpoint ("/").

You didn’t create the DB session yourself
FastAPI injected it for you
'''
#creating a first api endpoint
@app.get("/",status_code=status.HTTP_200_OK) 
async def read_all(db: db_depedency): #Dependency Injection is when something your code needs is given to it instead of being created inside it. 
    return db.query(Todos).all() #this will return all the records in the todos table of our database, and it will be returned as a response to the client when they make a GET request to the root endpoint ("/").

@app.get("/todo/{todos_id}",status_code=status.HTTP_200_OK) #adding a path and path parameter with a http method and status code
async def read_todo(db: db_depedency, todos_id: int=Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todos_id).first() #This line queries the database for a todo item with the specified ID. It uses the SQLAlchemy query interface to filter the Todos table based on the id column and retrieves the first matching record.
    if todo_model is not None: #This line checks if a matching todo item was found in the database. If the query returns a result, it means that a todo item with the specified ID exists.
        return todo_model 
    raise HTTPException(status_code=404, detail="Todo not found")  

#adding a post request method
@app.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_depedency,todo_request:TodoRequest):
    todo_model=Todos(**todo_request.dict()) 
    db.add(todo_model) 
    db.commit()

@app.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_depedency,todo_request:TodoRequest,todo_id:int):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is not None: 
        raise HTTPException(status_code=404, detail="Todo not found") 
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.completed=todo_request.completed 
    db.add(todo_model)
    db.commit()

