from strands import Agent
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    api_key="YOUR_API_KEY",
    model_id="gpt-4o-mini"
)

agent = Agent(model=model)
agent("Hello, how are you?")
