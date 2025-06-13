# Educator Bot

An interactive AI-powered educational assistant that teaches using the Socratic method, specializing in financial education and stock market concepts.

## Project Structure

```
educator-bot/
├── venv/                  # Virtual environment
├── requirements.txt       # Project dependencies
├── src/                   # Source code directory
│   ├── __init__.py
│   ├── tools.py          # Tools available for the agent to use
    └── agent.py          # Main implementation of the educator bot
└── README.md             # Project documentation
```

## Setup

1. Create and activate the virtual environment:
```bash
# Create virtual environment (already done)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
Create a `.env` file in the root directory and add your API keys:
```
OPENAI_API_KEY=your_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage

Run the educator bot:
```bash
python src/agent.py
```

The bot will start an interactive session where you can:
- Learn about financial concepts and stock markets
- Get guided through complex topics using the Socratic method
- Receive personalized feedback and encouragement
- Ask questions and get thoughtful responses

Type 'bye' or 'exit' to end the session.

## Features

- Socratic teaching method for effective learning
- Specialized in financial education and stock markets
- Interactive and engaging conversation style
- Real-time search capabilities for up-to-date information
- Personalized feedback and encouragement
- Clear and concise explanations of complex topics

## Requirements

- Python 3.8+
- OpenAI API key
- Tavily API key
- Dependencies listed in requirements.txt
