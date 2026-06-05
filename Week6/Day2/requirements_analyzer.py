import requests
import asyncio
from pydantic import BaseModel


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


class UserStory(BaseModel):
    title: str
    priority: str


class ConversationBufferMemory:
    def __init__(self):
        self.history = []

    def add(self, user, ai):
        self.history.append((user, ai))

    def get(self):
        return "\n".join([f"User: {u}\nAI: {a}" for u, a in self.history])


memory = ConversationBufferMemory()


async def async_retry(func, retries=3):
    for attempt in range(retries):
        try:
            return await func()
        except Exception:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(1)


async def call_llm(prompt: str):
    def sync_call():
        res = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False}
        )
        return res.json()["response"]

    return await asyncio.to_thread(sync_call)


async def sequential_chain(requirements: str):

    stories_prompt = f"""
Convert requirements into user stories.

Requirement:
{requirements}

Format:
Title: <user story>
Priority: <High/Medium/Low>
"""

    stories = await async_retry(lambda: call_llm(stories_prompt))

    task_prompt = f"""
Generate development tasks from the following user stories:

{stories}
"""

    tasks = await async_retry(lambda: call_llm(task_prompt))

    priority_prompt = f"""
Assign priority (High, Medium, Low) to each task:

{tasks}
"""

    prioritized_tasks = await async_retry(lambda: call_llm(priority_prompt))

    return stories, prioritized_tasks


async def chat(user_input: str):
    context = memory.get()

    prompt = f"""
You are a software assistant.

Conversation history:
{context}

User: {user_input}
AI:
"""

    response = await call_llm(prompt)
    memory.add(user_input, response)

    return response


async def main():
    while True:
        print("\n1. Analyze Requirements")
        print("2. Chat")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            req = input("Enter requirement:\n")
            stories, tasks = await sequential_chain(req)

            print("\nUser Stories:\n")
            print(stories)

            print("\nTasks with Priority:\n")
            print(tasks)

        elif choice == "2":
            msg = input("You: ")
            reply = await chat(msg)
            print("AI:", reply)

        elif choice == "3":
            break


if __name__ == "__main__":
    asyncio.run(main())