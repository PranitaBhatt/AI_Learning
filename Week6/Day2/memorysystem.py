from langchain_ollama import ChatOllama
import os

from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
    ConversationTokenBufferMemory,
    ConversationEntityMemory
)

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3"),
    custom_get_token_ids=lambda text: list(range(len(text.split()))),
)

#Buffer memory


buffer_memory = ConversationBufferMemory()

buffer_memory.save_context(
    {"input": "Hi"},
    {"output": "Hello"}
)

buffer_memory.save_context(
    {"input": "My name is Alex"},
    {"output": "Nice to meet you"}
)

print(buffer_memory.load_memory_variables({}))

#window menory

window_memory = ConversationBufferWindowMemory(k=1)

window_memory.save_context(
    {"input": "Hello"},
    {"output": "Hi"}
)

window_memory.save_context(
    {"input": "I love AI"},
    {"output": "Great"}
)

print(window_memory.load_memory_variables({}))

#summary memory

summary_memory = ConversationSummaryMemory(
    llm=llm
)

summary_memory.save_context(
    {"input": "I am learning AI"},
    {"output": "Nice"}
)

summary_memory.save_context(
    {"input": "I use Python"},
    {"output": "Excellent"}
)

print(summary_memory.load_memory_variables({}))

#token memory
token_memory = ConversationTokenBufferMemory(
    llm=llm,
    max_token_limit=50
)

token_memory.save_context(
    {"input": "Tell me about AI"},
    {"output": "AI is intelligence shown by machines"}
)

print(token_memory.load_memory_variables({}))

#entity memory

entity_memory = ConversationEntityMemory(
    llm=llm
)

entity_memory.save_context(
    {"input": "I work at OpenAI"},
    {"output": "That is amazing"}
)

print(entity_memory.load_memory_variables({"input": "I work at OpenAI"}))

