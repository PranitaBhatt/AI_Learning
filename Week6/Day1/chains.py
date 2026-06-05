from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import os



llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
    temperature=0.7
)

#Output parser

parser = StrOutputParser()

#User Input

topic = "Machine Learning"

#prompt chain 1

technical_prompt = ChatPromptTemplate.from_template("""
Explain {topic} in technical but beginner-friendly language.
Include:
- Definition
- Working
- Examples
""")

technical_chain = technical_prompt | llm | parser

technical_result = technical_chain.invoke({
    "topic": topic
})
#prompt chain 2
architecture_prompt = ChatPromptTemplate.from_template("""
Provide architecture summary for {topic}.

Include:
- Main components
- Workflow
- Technologies used
""")

architecture_chain = architecture_prompt | llm | parser

architecture_result = architecture_chain.invoke({
    "topic": topic
})

#prompt chain 3

quiz_prompt = ChatPromptTemplate.from_template("""
Generate 5 quiz questions on {topic}.
""")

quiz_chain = quiz_prompt | llm | parser

quiz_result = quiz_chain.invoke({
    "topic": topic
})

#prompt chain 4

simple_prompt = ChatPromptTemplate.from_template("""
Explain {topic} like teaching a 10-year-old child.
""")

simple_chain = simple_prompt | llm | parser

simple_result = simple_chain.invoke({
    "topic": topic
})

#prompt chain 5

professional_prompt = ChatPromptTemplate.from_template("""
Explain {topic} like a university professor.
""")

professional_chain = professional_prompt | llm | parser

professional_result = professional_chain.invoke({
    "topic": topic
})



print("=" * 60)
print("TECHNICAL EXPLANATION")
print("=" * 60)
print(technical_result)

print("\n")

print("=" * 60)
print("ARCHITECTURE SUMMARY")
print("=" * 60)
print(architecture_result)

print("\n")

print("=" * 60)
print("QUIZ QUESTIONS")
print("=" * 60)
print(quiz_result)

print("\n")

print("=" * 60)
print("SIMPLE EXPLANATION")
print("=" * 60)
print(simple_result)

print("\n")

print("=" * 60)
print("PROFESSIONAL EXPLANATION")
print("=" * 60)
print(professional_result)



output_data = {
    "topic": topic,

    "technical_explanation": technical_result,

    "architecture_summary": architecture_result,

    "quiz_questions": quiz_result,

    "simple_explanation": simple_result,

    "professional_explanation": professional_result
}


with open("ai_documentation_output.json", "w") as file:
    json.dump(output_data, file, indent=4)

print("\n")
print("JSON file created successfully!")
print("Saved as: ai_documentation_output.json")
