from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3")

# Tool 1
def multiply(a, b):
    return a * b

# Tool 2
def word_count(text):
    return len(text.split())

def tool_agent(query):
    if "multiply" in query:
        return multiply(5, 6)

    if "count words" in query:
        return word_count("This is a test sentence")

    return llm.invoke(query).content

print(tool_agent("multiply numbers"))
print(tool_agent("count words"))