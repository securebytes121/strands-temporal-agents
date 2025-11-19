from strands import Agent, tool
from strands.models.ollama import OllamaModel
from config import OLLAMA_HOST, OLLAMA_MODEL
from tools import get_time, get_weather, list_files, get_fact


@tool
def time_tool() -> str:
    return get_time()


@tool
def weather_tool(city: str) -> str:
    return get_weather(city)


@tool
def files_tool() -> str:
    return list_files()


@tool
def fact_tool(topic: str) -> str:
    return get_fact(topic, OLLAMA_HOST, OLLAMA_MODEL)


def create_agent() -> Agent:
    return Agent(
        model=OllamaModel(host=OLLAMA_HOST, model_id=OLLAMA_MODEL),
        tools=[time_tool, weather_tool, files_tool, fact_tool],
        system_prompt="Use available tools to provide accurate, helpful responses. Only use tools when necessary."
    )


def main():
    print("Simple Agent Demo")
    print("Type 'quit' to exit")
    print()
    
    agent = create_agent()
    
    while True:
        try:
            task = input("Enter task: ").strip()
            
            if task.lower() in ['quit', 'q', 'exit']:
                print("Goodbye!")
                break
            
            if not task:
                continue
            
            print("Processing...")
            result = agent(task)
            print(f"Result: {result}")
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()


if __name__ == "__main__":
    main()
