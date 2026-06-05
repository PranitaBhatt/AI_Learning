import os
import urllib3

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("USER_AGENT", "AI_Learning_WebBaseLoader/1.0") #Sets a default USER_AGENT string if not already set.
#Helps websites identify your request (some sites block unknown agents).
for proxy_var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
    os.environ.pop(proxy_var, None)

from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

model = ChatOllama(model="llama3")

prompt = PromptTemplate(
    template='Answer the following question \n {question} from the following text - \n {text}',
    input_variables=['question','text'] #{question} → user question ,{text} → webpage content
)

parser = StrOutputParser()

url = 'https://www.flipkart.com/apple-macbook-air-m2-16-gb-256-gb-ssd-macos-sequoia-mc7x4hn-a/p/itmdc5308fa78421'
loader = WebBaseLoader(
    url,
    verify_ssl=False,  #verify_ssl=False: Skip SSL validation.
    requests_kwargs={"timeout": 20, "verify": False},
)

docs = loader.load()


chain = prompt | model | parser

print(chain.invoke({'question':'What is the product that we are talking about?', 'text':docs[0].page_content}))
