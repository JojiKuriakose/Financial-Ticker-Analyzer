"""News agent factory."""
from typing import Optional
from azure.ai.agents.models import Agent, ToolSet


def create_news_agent(agent_client, model_deployment: str, tools_toolset: Optional[ToolSet] = None) -> Agent:
    """Create and return the NewsAgent."""
    return agent_client.create_agent(
        model=model_deployment,
        name="NewsAgent",
        instructions="You are a market news analyst. Summarize the latest financial or company news that could impact the stock's movement. "
                        "Focus on events such as earnings, market sentiment, regulations, or sector-wide developments. "
                        'Return the summary in a short JSON ONLY with keys: '
                        '{"as_of": "<date>", "news_summary": "<short_summary>", "sentiment": "positive"|"negative"|"neutral"}',   
        toolset=tools_toolset,
    )


__all__ = ["create_news_agent"]
