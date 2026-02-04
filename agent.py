from strands import Agent
from strands.models.ollama import OllamaModel

ollama_model = OllamaModel(
    host="http://localhost:11434",  # Ollama server address
    model_id="gemma3:1b"               # Specify which model to use
)

agent = Agent(model=ollama_model) # create an instance of Agent
agent("Hello , how are you?")

