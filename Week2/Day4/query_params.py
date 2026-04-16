from fastapi import FastAPI
app=FastAPI()
Books=[
    {"Title":"Title1","Author":"Author1","category":"science"},
    {"Title":"Title2","Author":"Author2","category":"science"},
    {"Title":"Title3","Author":"Author3","category":"history"},
    {"Title":"Title4","Author":"Author4","category":"english"},
    {"Title":"Title5","Author":"Author2","category":"history"},
]

#Query Parameters
@app.get("/api-endpoint")
async def read_category_by_query(category:str):
    books_to_return=[] #creating an empty list to store the books which are matching the category
    for book in Books:
        if book.get('category').casefold()==category.casefold():
            books_to_return.append(book)
    return books_to_return

#Ouery parameter with a path parameter
@app.get("/books/{book_author}")
async def read_category_with_querypath(book_author:str, category:str):
    book_return=[]
    for book in Books:
        if book.get('Author').casefold()==book_author.casefold() and \
        book.get('category').casefold()==category.casefold():     #usisng and fucntion we are filtering author and category both
            book_return.append(book)
    return book_return