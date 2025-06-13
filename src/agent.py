# Import relevant functionality
from dotenv import load_dotenv
from src.state import FinancialEducatorState, initial_state
from tools import tools
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()  # Load environment variables from .env file
memory = MemorySaver()
model = ChatOpenAI(model_name="gpt-4-turbo-preview")

# Configuration for conversation history
CONVERSATION_WINDOW_SIZE = 10  # Number of messages to keep in history

# Initialize conversation with a system message
system_prompt = """
You are a patient and encouraging financial educator who teaches using the Socratic method. 
Your expertise lies in stock markets and personal finance.

Teaching Style:
- Use thoughtful questions to guide the student's understanding
- Break down complex financial concepts into digestible parts
- Encourage critical thinking about financial decisions
- When the student asks insightful questions or shows good understanding, offer moderate praise like "That's a thoughtful question" or "You're thinking in the right direction"
- If a student's understanding needs improvement, guide them gently with follow-up questions
- Always maintain a supportive and non-judgmental tone
- Use real-world examples when possible
- If you need to provide direct information, do so after asking relevant questions

State Awareness:
- Track the student's learning level and adjust your teaching accordingly
- Remember topics you've covered to build upon previous knowledge
- Monitor learning progress and provide encouragement
- Keep track of concepts explained to avoid repetition
- Use session context to maintain focus on current learning objectives

Remember to:
- Never echo back the student's questions
- Keep responses clear and concise
- Adapt your teaching pace to the student's level
- Encourage questions and curiosity
- Use the search tool to provide accurate, up-to-date information
"""

# Initialize the state with default values
initial_state = {
    "messages": [SystemMessage(content=system_prompt)],
    "remaining_steps": 3,  # Default number of steps for agent execution
    "user_level": "beginner",  # Default to beginner
    "topics_covered": [],
    "learning_progress": 0,
    "session_context": "introduction",
    "questions_asked": 0
}

# Create agent with custom state schema
agent_executor = create_react_agent(
    model, 
    tools, 
    checkpointer=memory,
    state_schema=FinancialEducatorState
)

# Use the agent in a continuous conversation
config = {"configurable": {"thread_id": "conversation_1"}}

print("Starting your financial education session. I'll guide you through learning about stocks and personal finance.")
print("Type 'bye' or 'exit' to end the session.")
print("=" * 50)

def get_recent_messages(messages_list, window_size):
    """Get the most recent messages within the window size, always including the system message."""
    if len(messages_list) <= window_size:
        return messages_list
    # Always keep the system message (first message) and the most recent messages
    return [messages_list[0]] + messages_list[-window_size+1:]

def update_learning_state(user_input, current_state):
    """Update learning state based on user input and interaction"""
    updated_state = current_state.copy()
    
    # Increment questions asked
    updated_state["questions_asked"] = current_state.get("questions_asked", 0) + 1
    
    # Simple heuristics to update learning progress and context
    if any(word in user_input.lower() for word in ["what", "how", "why", "explain"]):
        # User is asking questions - good engagement
        updated_state["learning_progress"] = min(100, current_state.get("learning_progress", 0) + 2)
    
    # Update session context based on keywords
    finance_keywords = {
        "stock": "stock_market",
        "investment": "investing",
        "portfolio": "portfolio_management", 
        "risk": "risk_management",
        "dividend": "dividend_investing",
        "budget": "budgeting",
        "savings": "savings_strategies"
    }
    
    for keyword, context in finance_keywords.items():
        if keyword in user_input.lower():
            updated_state["session_context"] = context
            if context not in current_state.get("topics_covered", []):
                updated_state["topics_covered"] = current_state.get("topics_covered", []) + [context]
            break
    
    return updated_state

# Start with initial state
current_state = initial_state

while True:
    # Get user input
    user_input = input("\nYou: ").strip()
    
    # Check for exit conditions
    if user_input.lower() in ["bye", "exit"]:
        print(f"\nGoodbye! Great session today. You asked {current_state.get('questions_asked', 0)} questions and covered {len(current_state.get('topics_covered', []))} topics.")
        print(f"Learning progress: {current_state.get('learning_progress', 0)}%")
        print(f"Topics covered: {', '.join(current_state.get('topics_covered', []))}")
        break
    
    # Update learning state based on user input
    current_state = update_learning_state(user_input, current_state)
    
    # Add user message to current state
    current_state["messages"] = current_state["messages"] + [HumanMessage(content=user_input)]
    
    # Get agent's response using current state
    recent_messages = get_recent_messages(current_state["messages"], CONVERSATION_WINDOW_SIZE)
    
    # Create state for agent with recent messages
    agent_state = current_state.copy()
    agent_state["messages"] = recent_messages
    
    final_response = None
    for step in agent_executor.stream(
        agent_state,
        config,
        stream_mode="values",
    ):
        final_response = step["messages"][-1]
        # Update current state with any state changes from the agent
        current_state.update({k: v for k, v in step.items() if k != "messages"})
    
    # Only print and store the final response
    if final_response:
        print("\nEducator:", final_response.content)
        current_state["messages"] = current_state["messages"] + [final_response]

print("=" * 50)
print("Session ended.")

# For models like Llama, Mistral, etc.
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])