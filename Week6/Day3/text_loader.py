from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

model=OllamaLLM(model="llama3")
prompt=ChatPromptTemplate.from_template(
    'Write a summary for following document: {document}'
)

parser=StrOutputParser()

#we need to create an object of textloader
file_path=Path(__file__).parent / "rag.txt"
loader=TextLoader(file_path,encoding="utf-8")  #encoding utf8 is used since it also acceots special characters

docs=loader.load()  #this will load the document and store it in docs variable

print(docs)  
print(type(docs))  #stores op as list
print(len(docs))  
print(type(docs[0]))  #stores op as document object
print(docs[0])

chain=prompt|model|parser
print(chain.invoke({'document':docs[0].page_content}))  #we need to pass the content
