"""Trend agent factory."""
from typing import Optional
from azure.ai.agents.models import Agent, ToolSet


def create_trend_agent(agent_client, model_deployment: str, tools_toolset: Optional[ToolSet] = None) -> Agent:
    """Create and return the TrendAgent."""
    return agent_client.create_agent(
        model=model_deployment,
        name="TrendAgent",
        instructions="You are a stock trend analyst. Use the 'fetch_stock_data' function to retrieve the last N daily closing prices. "
                        "Identify the short-term (last 30 days) price trend as UP, DOWN, or SIDEWAYS. "
                        'Return a concise JSON ONLY with the following keys: '
                        '{"as_of": "<date>", "trend": "up"|"down"|"sideways", "current_price": float, "recent_change_pct": float}.\n'
                        "recent_change_pct = (last_close/first_close - 1)*100 rounded to 2 decimals.",
        toolset=tools_toolset,
    )


__all__ = ["create_trend_agent"]
