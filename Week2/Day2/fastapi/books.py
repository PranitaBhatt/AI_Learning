from fastapi import FastAPI
app=FastAPI()
Books=[
    {"Title":"Ttile1","Author":"Author1","category":"science"},
    {"Title":"Ttile2","Author":"Author2","category":"science"},
    {"Title":"Ttile3","Author":"Author3","category":"history"},
    {"Title":"Ttile4","Author":"Author4","category":"english"},
    {"Title":"Ttile5","Author":"Author5","category":"science"},
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

#Adding a function with dynamic parameter
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return{"dynamic_param":dynamic_param}