import asyncio

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3")
#ainvoke
async def async_invoke():
    response = await llm.ainvoke(
        "Explain Artificial Intelligence"
    )

    print(response.content)

#batch processing

def batch_processing():

    prompt = ChatPromptTemplate.from_template(
        "Explain topic: {topic}"
    )

    chain = prompt | llm

    results = chain.batch([
        {"topic": "AI"},
        {"topic": "ML"},
        {"topic": "DL"},
    ])

    for result in results:

        print("\n")
        print(result.content)

#concurrency

async def concurrency_demo():

    tasks = [

        llm.ainvoke("Explain AI"),

        llm.ainvoke("Explain ML"),

        llm.ainvoke("Explain Deep Learning"),
    ]

    results = await asyncio.gather(*tasks)

    for result in results:

        print("\n")
        print(result.content)

#streaming response

def streaming_demo():
    for chunk in llm.stream(
        "Explain Generative AI"
    ):

        print(chunk.content, end="", flush=True)

#main

async def main():

    await async_invoke()
    batch_processing()
    await concurrency_demo()
    streaming_demo()

asyncio.run(main())
