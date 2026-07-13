from urllib import response

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from tavily import TavilyClient
from langchain_tavily import TavilySearch
from LearnPydantic import AgentResponse, Source
from langchain.agents.structured_output import ToolStrategy

from pprint import pprint

load_dotenv()

#@tool
def search1(query: str) -> str:
    """
    Tool that search over the internet for a given query and returns the result.
    Args:
        query (str): The query to search for.
    Returns:
        str: The search result.
    """
    print("Searching for {query}...")
    return "Yamunanagar weather is very very cold and its around negative 30 degrees Celsius."



tavily_client = TavilyClient()

@tool
def search(query: str) -> str:
    """
    Tool that search over the internet for a given query and returns the result.
    Args:
        query (str): The query to search for.
    Returns:
        str: The search result.
    """
    print("Searching with tavily client for {query}")

    return tavily_client.search(query=query)

llm = ChatOllama(model="qwen3:8b", base_url="http://host.docker.internal:11434")


def call_ollama_test():
    desc_template= """
            Hi tell me something about {topic} in 2 sentences."""
    topic="LangChain"
    prompt_template= PromptTemplate(input_variables=["topic"], template = desc_template)

    chain = prompt_template | llm
    response = chain.invoke({"topic": topic})
    print(response.content)

def call_ollama_test_with_tool1():
    tools= [search]
    agent = create_agent(model=llm, tools=tools)
    response= agent.invoke({"messages":HumanMessage(content="What is the weather in Yamunanagar today?")})
    print(response)


def call_ollama_test_with_tool2():
    # we are here using in house tool of tavily, no need to create the search method as did in the previous function
    tools=[TavilySearch()]
    agent = create_agent(model=llm, tools=tools)
    response= agent.invoke({"messages":HumanMessage(content="What is the weather in Yamunanagar today?")})
    print(response)


def call_ollama_test_with_tool3():
    # we are here using in house tool of tavily, no need to create the search method as did in the previous function, 
    # with response format defined in LearnPydantic.py
    tools=[TavilySearch()]
    agent = create_agent(
    model=llm,
    tools=[TavilySearch()],
    response_format=ToolStrategy(AgentResponse),)
    response= agent.invoke({"messages":HumanMessage(content="What is the weather in Yamunanagar today?")}, 
                           response_format=ToolStrategy(AgentResponse))
    #print(response["structured_response"])
    pprint(response)
    print(type(response))

    if isinstance(response, dict):
        print(response.keys())


def main():
    print("Hello from langchain-me!")

    #print("call_ollama_test_with_tool1 with tavily client search method")
    #call_ollama_test_with_tool1()

    #print("call_ollama_test_with_tool2 with tavily search tool")
    #call_ollama_test_with_tool2()
  
    print("call_ollama_test_with_tool3 with tavily search tool")
    call_ollama_test_with_tool3()

if __name__ == "__main__":
    main()
