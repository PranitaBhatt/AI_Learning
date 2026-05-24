from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings

# Initialize embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Create semantic chunker
text_splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=0.8 # lower = more chunks
)

sample = """
Farmers were working hard in the fields, preparing the soil and planting seeds for the next season. The sun was bright, and the air smelled of earth and fresh grass.
The Indian Premier League (IPL) is the biggest cricket league in the world. People all over the world watch matches and cheer for teams.

Terrorism is a serious threat to global security. It creates fear and harms innocent people. Governments must work together to prevent such acts.
"""

docs = text_splitter.create_documents([sample])

print("Total chunks:", len(docs))

print("First chunk:", docs[0].page_content)
