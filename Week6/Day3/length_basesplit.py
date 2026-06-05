from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


loader=PyPDFLoader('test.pdf')
docs=loader.load()

splitter=CharacterTextSplitter(chunk_size=20,
                               chunk_overlap=0, #we use overlap as it keeps the context intact and helps in better understanding of the content keeping some common words in both the chunks. But here we are not using it as we want to see the effect of chunking clearly.
                               separator='')
result=splitter.split_documents(docs)
print(result[0].page_content)
