from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# Define custom state schema for the financial educator
class FinancialEducatorState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    remaining_steps: int  # Required by create_react_agent
    user_level: str  # beginner, intermediate, advanced
    topics_covered: List[str]  # Track what topics have been discussed
    learning_progress: int  # Score from 0-100
    session_context: str  # Current focus area or context
    questions_asked: int  # Count of questions asked by student