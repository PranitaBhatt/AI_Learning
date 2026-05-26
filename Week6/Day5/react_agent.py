from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool


@tool
def echo(text: str) -> str:
    """Return the input text as the output."""
    return text

llm = ChatOllama(model="llama3.1:8b", temperature=0)

agent = create_agent(
    model=llm,
    tools=[echo],
    system_prompt=(
        "You are a thoughtful assistant with access to tools. "
        "When a tool returns the requested answer, reply with that answer directly."
    ),
)

def main() -> None:
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Echo Hello Geek using the echo tool."}]}
    )
    tool_messages = [
        message for message in response["messages"] if isinstance(message, ToolMessage)
    ]
    print(tool_messages[-1].content if tool_messages else response["messages"][-1].content)


if __name__ == "__main__":
    main()
