from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatOllama(model="llama3")

#pydantic schema for structured output
class UserStory(BaseModel):

    title: str = Field(description="Story title")
    priority: str = Field(description="Priority level")

#parser for structured output
parser = JsonOutputParser(
    pydantic_object=UserStory #defining the class here
)

#prompt
prompt = ChatPromptTemplate.from_template(
    """
    Generate agile user story.
    {format_instructions}
    Topic: {topic}
    """
)

chain = (
    prompt.partial(
        format_instructions=parser.get_format_instructions()
    )
    | llm
    | parser
)

#retry logic
def safe_generate(topic, retries=3):
    for attempt in range(retries):

        try:
            result = chain.invoke({
                "topic": topic
            })
            return result

        except Exception as e:

            print(f"Retry {attempt+1}")

            print(e)

    return "Generation Failed"


result = safe_generate("Login System")
print(result)
