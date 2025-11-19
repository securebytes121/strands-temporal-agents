import os
import logging
from datetime import datetime
import requests

logger = logging.getLogger(__name__)


def get_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def list_files() -> str:
    try:
        files = [f for f in os.listdir('.') if f.endswith('.py')]
        return f"Python files: {', '.join(files[:10])}"
    except Exception as e:
        return f"File listing error: {str(e)}"


def get_weather(city: str) -> str:
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            weather_data = response.text.strip()
            return f"{city}: {weather_data}"
        
        return f"Weather data unavailable for {city}"
        
    except Exception as e:
        logger.error(f"Weather service error for {city}: {e}")
        raise  # Let caller handle retry logic


def get_fact(topic: str, ollama_host: str, ollama_model: str) -> str:
    from strands import Agent
    from strands.models.ollama import OllamaModel
    
    agent = Agent(
        model=OllamaModel(host=ollama_host, model_id=ollama_model),
        system_prompt="Provide interesting, accurate facts about the requested topic. Be concise."
    )
    
    result = agent(f"Tell me an interesting fact about {topic}")
    return str(result.content if hasattr(result, 'content') else result)
