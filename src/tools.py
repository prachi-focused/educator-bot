
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()  # Load environment variables from .env file

# Create the agent
search = TavilySearch(max_results=2)
tools = [search]
