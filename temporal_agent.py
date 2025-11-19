"""Temporal workflow with AI agent orchestration."""
import logging
from datetime import timedelta
from temporalio import activity, workflow
from temporalio.common import RetryPolicy
from config import OLLAMA_HOST, OLLAMA_MODEL

logger = logging.getLogger(__name__)


@activity.defn
async def ai_agent_activity(task: str) -> str:
    """Use AI agent with native tool calling to handle the task."""
    # Import inside activity to avoid workflow sandbox restrictions
    from strands import Agent, tool as strands_tool
    from strands.models.ollama import OllamaModel
    from tools import get_time, get_weather, list_files, get_fact
    
    # Wrap tools for Strands
    @strands_tool
    def time_tool() -> str:
        """Get the current date and time."""
        return get_time()
    
    @strands_tool
    def weather_tool(city: str) -> str:
        """Get weather information for a city."""
        return get_weather(city)
    
    @strands_tool
    def files_tool() -> str:
        """List Python files in the current directory."""
        return list_files()
    
    @strands_tool
    def fact_tool(topic: str) -> str:
        """Get an interesting fact about a topic."""
        return get_fact(topic, OLLAMA_HOST, OLLAMA_MODEL)
    
    agent = Agent(
        model=OllamaModel(host=OLLAMA_HOST, model_id=OLLAMA_MODEL),
        tools=[time_tool, weather_tool, files_tool, fact_tool],
        system_prompt="Use available tools to provide accurate, helpful responses. Only use tools when necessary."
    )
    
    try:
        result = agent(task)
        return str(result.content if hasattr(result, 'content') else result)
    except Exception as e:
        logger.error(f"AI agent failed: {e}")
        raise


@workflow.defn
class TemporalAgentWorkflow:
    """
    Workflow that uses AI agent with native tool calling.
    Leverages Temporal for durability, observability, and retry semantics.
    """
    
    @workflow.run
    async def run(self, task: str, enable_partial_results: bool = True) -> str:
        """
        Execute task using AI agent with tools.
        
        Args:
            task: User's natural language request
            enable_partial_results: Return error message instead of raising exception
        
        Returns:
            Result from AI agent execution
        """
        workflow.logger.info(f"Processing task: {task}")
        
        try:
            result = await workflow.execute_activity(
                ai_agent_activity,
                task,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=RetryPolicy(
                    maximum_attempts=2,
                    initial_interval=timedelta(seconds=1)
                )
            )
            
            workflow.logger.info("Task completed successfully")
            return result
            
        except Exception as e:
            workflow.logger.error(f"Workflow failed: {e}")
            if enable_partial_results:
                return f"Task failed: {str(e)}"
            raise

