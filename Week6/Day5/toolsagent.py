from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

llm = ChatOllama(model="llama3.1:8b", temperature=0)

agent = create_agent(
    model=llm,
    tools=[add],
    system_prompt=(
        "You are an assistant that answers using tools. "
        "When a tool returns the requested answer, reply with that answer directly."
    ),
)

def main() -> None:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What is 5 plus 7? Use the add tool."}]}
    )
    tool_messages = [
        message for message in result["messages"] if isinstance(message, ToolMessage)
    ]
    print(tool_messages[-1].content if tool_messages else result["messages"][-1].content)


if __name__ == "__main__":
    main()
