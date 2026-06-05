from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool


@tool
def book_flight(origin: str, destination: str) -> str:
    """Simulate flight booking from origin to destination."""
    return f"Booked flight from {origin} to {destination}"


tools = [book_flight]

llm = ChatOllama(model="llama3.1:8b", temperature=0)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a travel assistant with access to tools. "
        "When a tool returns the requested answer, reply with that answer directly."
    ),
)

def main() -> None:
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Book a flight from NYC to LA using the book_flight tool.",
                }
            ]
        }
    )
    tool_messages = [
        message for message in response["messages"] if isinstance(message, ToolMessage)
    ]
    print("Final Output:", tool_messages[-1].content if tool_messages else response["messages"][-1].content)


if __name__ == "__main__":
    main()
