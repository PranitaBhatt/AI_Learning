from fastapi import FastAPI, Depends, HTTPException, status, Path
import models
from database import engine
from routers import auth,todos #this refers to the routers packages which we build for authorization point auth.py file



app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router) #this will help fecthing router from auth file
app.include_router(todos.router) #will fecth todos.py file
