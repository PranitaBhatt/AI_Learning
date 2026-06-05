import asyncio
import time

from langchain_ollama import ChatOllama


main_llm = ChatOllama(model="llama3")

fallback_llm = ChatOllama(model="mistral")


def log_event(event):

    print(f"\n[LOG]: {event}")

    print(f"[TIME]: {time.strftime('%H:%M:%S')}")

#retry logic
def retry_call(prompt, retries=3):

    for attempt in range(retries):

        try:

            return main_llm.invoke(prompt).content

        except Exception as e:

            print(f"Retry {attempt+1}")

            print(e)

    return "Failed"
#fallback logic

def fallback_call(prompt):

    try:

        return main_llm.invoke(prompt).content

    except Exception:

        print("Using Fallback Model")

        return fallback_llm.invoke(prompt).content
#timeout handling

async def timeout_demo():

    try:

        result = await asyncio.wait_for(
            main_llm.ainvoke("Explain AI"),
            timeout=10
        )

        print(result.content)

    except asyncio.TimeoutError:

        print("Timeout Occurred")
#rate limiting

def rate_limited_calls():

    prompts = [
        "What is AI?",
        "What is ML?",
        "What is DL?"
    ]

    for prompt in prompts:

        print(main_llm.invoke(prompt).content)

        time.sleep(2)
#execution
log_event("Starting System")

print(retry_call("Explain AI"))

print(fallback_call("Explain Machine Learning"))

rate_limited_calls()

asyncio.run(timeout_demo())
