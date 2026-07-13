from pydantic import BaseModel
from langchain_ollama import ChatOllama
import langchain
import langchain_core
import langchain_ollama

class Person(BaseModel):
    name: str
    age: int

print("langchain:", langchain.__version__)
print("langchain_core:", langchain_core.__version__)
print("langchain_ollama:", langchain_ollama.__version__)

llm = ChatOllama(
    model="qwen3:8b",
    base_url="http://host.docker.internal:11434"
)

structured_llm = llm.with_structured_output(Person)

result = structured_llm.invoke(
    "John is 25 years old."
)

print(result)