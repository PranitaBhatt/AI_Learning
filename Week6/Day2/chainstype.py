from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnableBranch
)

#main model
llm=ChatOllama(model="llama3")

#Fallback model: A model that is more likely to give a response when primary model fails
fallback_llm=ChatOllama(model="llama2")



#Adding first chain : SEQUENTIAL
title_prompt=ChatPromptTemplate.from_template("generate a title for {topic}")
outline_prompt=ChatPromptTemplate.from_template("generate an outline for this title: {title}")
article_prompt=ChatPromptTemplate.from_template("generate an article using this outline: {outline}")

#Chaining prompts with models
title_chain=title_prompt | llm
title = title_chain.invoke({
    "topic": "Artificial Intelligence"
}).content
print("Generated title:", title)

outline_chain=outline_prompt | llm
outline = outline_chain.invoke({
    "title": title
}).content
print("Generated outline:", outline)

article_chain=article_prompt | llm
article = article_chain.invoke({
    "outline": outline
}).content
print("Generated article:", article)

#Adding second chain : PARALLEL
review="""This article is genrated good but the content is poor"""
summary_prompt=ChatPromptTemplate.from_template("generate a summary for the article: {review}")
sentiment_prompt=ChatPromptTemplate.from_template("analyze the sentiment of the review: {review}")
keyword_prompt=ChatPromptTemplate.from_template("extract keywords from the review: {review}")

#Creating a paralle chain
parallel_chain=RunnableParallel(
    summary=summary_prompt | llm,
    sentiment=sentiment_prompt | llm,
    keywords=keyword_prompt | llm
)

p_result=parallel_chain.invoke({
    "review": review
})

print("Summary:", p_result["summary"].content)
print("Sentiment:", p_result["sentiment"].content)
print("Keywords:", p_result["keywords"].content)

#Adding third chain : Router
math_prompt=ChatPromptTemplate.from_template("solve the math problem: {input}")
coding_prompt=ChatPromptTemplate.from_template("write a code to solve the problem: {input}")

math_chain = math_prompt | llm
coding_chain = coding_prompt | llm

def route(info):
    question = info["input"].lower()

    if "code" in question or "python" in question:
        return coding_chain

    return math_chain
router_chain = RunnableLambda(route)
query={"input": "Write Python code for factorial"}

response = router_chain.invoke(query)
print("Response:", response.content)

#Adding fourth chain : Conditional Chain
positive_chain = RunnableLambda(
    lambda x: "Positive Review"
)

negative_chain = RunnableLambda(
    lambda x: "Escalate to Human"
)

conditional_chain = RunnableBranch(
    (
        lambda x: "bad" in x["review"].lower(),
        negative_chain
    ),
    positive_chain
)

response = conditional_chain.invoke({
    "review": "This product is bad"
})

print(response)

#Adding 5th chain : RunnableLambda
def uppercase(text):
    return text.upper()

lambda_chain = RunnableLambda(uppercase)

result = lambda_chain.invoke("hello world")

print(result)
