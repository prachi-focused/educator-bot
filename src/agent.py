# Import relevant functionality
from dotenv import load_dotenv
from tools import tools

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

load_dotenv()  # Load environment variables from .env file
memory = MemorySaver()
model = ChatOpenAI(model_name="gpt-4-turbo-preview")

# Configuration for conversation history
CONVERSATION_WINDOW_SIZE = 10  # Number of messages to keep in history

agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent in a continuous conversation
config = {"configurable": {"thread_id": "conversation_1"}}
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

Remember to:
- Never echo back the student's questions
- Keep responses clear and concise
- Adapt your teaching pace to the student's level
- Encourage questions and curiosity
- Use the search tool to provide accurate, up-to-date information
"""

messages = [
    SystemMessage(content=system_prompt)
]

print("Starting your financial education session. I'll guide you through learning about stocks and personal finance.")
print("Type 'bye' or 'exit' to end the session.")
print("=" * 50)

def get_recent_messages(messages_list, window_size):
    """Get the most recent messages within the window size, always including the system message."""
    if len(messages_list) <= window_size:
        return messages_list
    # Always keep the system message (first message) and the most recent messages
    return [messages_list[0]] + messages_list[-window_size+1:]

while True:
    # Get user input
    user_input = input("\nYou: ").strip()
    
    # Check for exit conditions
    if user_input.lower() in ["bye", "exit"]:
        print("\nGoodbye. Feel free to return anytime you have more questions.")
        break
    
    # Add user message to history
    messages.append(HumanMessage(content=user_input))
    
    # Get agent's response using only recent messages
    recent_messages = get_recent_messages(messages, CONVERSATION_WINDOW_SIZE)
    final_response = None
    for step in agent_executor.stream(
        {"messages": recent_messages},
        config,
        stream_mode="values",
    ):
        final_response = step["messages"][-1]
    
    # Only print and store the final response
    if final_response:
        print("\nEducator:", final_response.content)
        messages.append(final_response)

print("=" * 50)
print("Session ended.")