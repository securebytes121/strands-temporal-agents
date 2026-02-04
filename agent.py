from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(
    model_id="gemma3:1b"
)

agent = Agent(model=model)
print(agent("Hello, how are you?"))
