"""Decision agent factory."""
from typing import Optional
from azure.ai.agents.models import Agent, ToolSet


def create_decision_agent(agent_client, model_deployment: str, tools_toolset: Optional[ToolSet] = None) -> Agent:
    """Create and return the DecisionAgent."""
    return agent_client.create_agent(
        model=model_deployment,
        name="DecisionAgent",
        instructions=(
                        "You are a financial advisor. Based on the analysis provided by the TrendAgent and NewsAgent:\n\n"
                        "- Provide a final recommendation: **BUY**, **SELL**, or **HOLD**.\n"
                        "- If BUY: suggest an entry price, a stop-loss level, and a target selling price.\n"
                        "- If SELL: suggest a selling price, a stop-loss level, and a potential re-entry price if conditions improve.\n"
                        "- Include an estimated risk probability (Low/Medium/High) based on uncertainty in news and trend analysis.\n\n"
                        "⚡ Final Output Format (well-structured for readability):\n\n"
                        "📊 Recommendation: BUY / SELL / HOLD\n"
                        "💰 Entry Price: <value>\n"
                        "🎯 Target Price: <value>\n"
                        "🛑 Stop Loss: <value>\n"
                        "📈 Risk Probability: Low / Medium / High\n"
                        "📝 Reasoning: <short reasoning based on trends + news>"
                    )
    )


__all__ = ["create_decision_agent"]
