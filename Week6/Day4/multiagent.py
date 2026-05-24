from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3")

# Planner
def planner(topic):
    plan = llm.invoke(f"Break this into steps: {topic}").content
    return plan

# Researcher
def researcher(topic):
    return llm.invoke(f"Give detailed research on: {topic}").content

# Summarizer
def summarizer(data):
    return llm.invoke(f"Summarize:\n{data}").content

# Validator
def validator(summary):
    return llm.invoke(f"Check if this is correct:\n{summary}").content

# Pipeline
def multi_agent_system(topic):
    print("Planning...")
    plan = planner(topic)

    print("Researching...")
    data = researcher(topic)

    print("Summarizing...")
    summary = summarizer(data)

    print("Validating...")
    validation = validator(summary)

    return {
        "plan": plan,
        "summary": summary,
        "validation": validation
    }

output = multi_agent_system("Future of AI")
print(output)
