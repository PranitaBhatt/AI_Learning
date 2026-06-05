from langchain_text_splitters import RecursiveCharacterTextSplitter

text="""Retrieval-Augmented Generation, commonly referred to as RAG, is an architectural approach in artificial intelligence that enhances the capabilities of large language models by integrating external knowledge retrieval mechanisms into the text generation process. 
At its core, RAG addresses a fundamental limitation of traditional language models, which rely entirely on the information embedded in their training data. While these models can generate fluent and contextually coherent responses, they often struggle with accuracy, 
especially when dealing with up-to-date, domain-specific, or proprietary information. RAG overcomes this limitation by dynamically retrieving relevant information from an external data source and incorporating it into the model’s response generation.

To understand RAG, it is useful to first consider how standard language models operate. A typical large language model is trained on vast amounts of text data, learning statistical patterns and relationships between words. However, once training is complete, the model 
cannot access new information unless it is retrained. This makes it inherently static and prone to producing outdated or fabricated information, a phenomenon often described as hallucination. RAG introduces a dynamic layer that allows the model to query a separate 
knowledge base at inference time. This knowledge base can consist of documents, databases, or any structured or unstructured data relevant to the task.

The RAG process generally consists of three main stages: retrieval, augmentation, and generation. In the retrieval stage, the system receives a user query and searches for relevant pieces of information from a predefined corpus. This is typically achieved using vector
search techniques, where documents are converted into numerical embeddings that capture semantic meaning. These embeddings are stored in a vector database, and when a query is received, it is similarly converted into an embedding and compared against the stored vectors to identify the most relevant matches. This allows the system to go beyond simple keyword matching and retrieve information based on contextual similarity.

"""



splitter=RecursiveCharacterTextSplitter(chunk_size=100,
                               chunk_overlap=0, #we use overlap as it keeps the context intact and helps in better understanding of the content keeping some common words in both the chunks. But here we are not using it as we want to see the effect of chunking clearly.
)
chunks=splitter.split_text(text)
print(len(chunks))
print(chunks)
