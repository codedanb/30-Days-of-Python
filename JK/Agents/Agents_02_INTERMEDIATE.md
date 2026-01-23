# Agents_02_INTERMEDIATE

## The Practitioner of Agents

*Target Audience*: Junior Developer / Daily User.  
*Philosophy*: Focus on "Getting things done". Standard patterns and libraries.

### Standard Library usage

In programming agents, libraries are pre-built tools that save time. Key libraries for agents include:  
- **LangChain**: A framework for building applications with large language models (LLMs). Use it to chain together prompts and tools for complex agent behaviors.  
- **OpenAI API**: Access powerful AI models like GPT to give your agents intelligence. Standard usage: Authenticate with API key, send prompts, receive responses.  
- **Hugging Face Transformers**: Library for using pre-trained AI models. Load models like BERT for natural language understanding in agents.  
- **Requests**: For agents that need to interact with web APIs or fetch data from the internet.

### Common Data Structures

Agents manage information efficiently:  
- **Lists**: Store sequences of tasks, perceptions, or actions (e.g., ["check weather", "send email", "update calendar"]).  
- **Dictionaries**: Key-value pairs for agent state (e.g., {"location": "home", "battery": 80, "tasks": ["clean", "cook"]}).  
- **Queues**: First-in-first-out structures for action planning (e.g., pending tasks in order).  
- **Stacks**: Last-in-first-out for backtracking in decision-making.

### Modular programming (Functions, basic OOP)

Build agents in reusable pieces:  
- **Functions**: Define reusable actions (e.g., `def greet_user(): return "Hello!"`).  
- **Classes**: Create agent blueprints (e.g., class SimpleAgent: with methods like perceive(), act()).  
- Basic inheritance: Extend base agent classes for specialized agents (e.g., ChatbotAgent inherits from BaseAgent).

### Error Handling (Try/Except)

Agents must handle failures gracefully:  
- **Try/Except Blocks**: Catch network errors (e.g., try: api_call() except ConnectionError: retry()).  
- Common exceptions: API rate limits, invalid inputs, timeouts.  
- Logging errors for debugging agent behavior.

### File I/O

Agents persist data:  
- **Reading Config Files**: Load agent settings from JSON/YAML (e.g., API keys, goals).  
- **Writing Logs**: Record actions and perceptions to text files for review.  
- **Saving State**: Serialize agent memory to files for resuming sessions.

### Getting Things Done: Building a Simple Agent

Using Python + LangChain:  
1. Install libraries: `pip install langchain openai`.  
2. Create a basic conversational agent that answers questions using OpenAI.  
3. Handle common errors like API failures.  
4. Modularize into functions for perception (user input), reasoning (LLM call), action (response output).

This level focuses on practical implementation for daily use, like automating email responses or simple chatbots.