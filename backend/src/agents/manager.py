"""Agent manager: create/delete agents and provide FastAPI lifespan context."""
from contextlib import asynccontextmanager
import time
from azure.ai.agents.models import FunctionTool, ToolSet, Agent
from fastapi import FastAPI
from src.config.settings import settings
from src.services.fetch_data import user_functions
from .trend import create_trend_agent
from .news import create_news_agent
from .decision import create_decision_agent
from src.services.telemetry_service import get_tracer, get_logger
from src.utils.azure_utils import agent_client


trend_agent: Agent = None
news_agent: Agent = None
decision_agent: Agent = None
tools_toolset: ToolSet = None


@asynccontextmanager
async def lifespan(app:FastAPI):
    """FastAPI lifespan that creates agents on startup and deletes them on shutdown."""
    global trend_agent, news_agent, decision_agent, tools_toolset
    tracer = get_tracer()
    logger = get_logger()
    startup_start = time.time()

    if tracer:
        with tracer.start_as_current_span("application_startup") as span:
            try:
                if logger:
                    logger.info("Starting up and creating agents...")
                print("Starting up and creating agents...")

                # 1. Register tools and enable auto-function calls
                span.add_event("Registering tools")
                functions = FunctionTool(user_functions)
                tools_toolset = ToolSet()
                tools_toolset.add(functions)
                agent_client.enable_auto_function_calls(tools_toolset)

                # 2. Create agents and assign them to the global variables
                span.add_event("Creating TrendAgent")
                trend_agent = create_trend_agent(agent_client, settings.model_deployment, tools_toolset)
                
                span.add_event("Creating NewsAgent")
                news_agent = create_news_agent(agent_client, settings.model_deployment, tools_toolset)

                span.add_event("Creating DecisionAgent")
                decision_agent = create_decision_agent(agent_client, settings.model_deployment, tools_toolset)

                startup_duration = time.time() - startup_start
                span.set_attribute("startup_duration_seconds", round(startup_duration, 3))
                span.set_attribute("agents_created", 3)
                span.set_attribute("success", True)

                if logger:
                    logger.info(f"Agents ready: {trend_agent.name}, {news_agent.name}, {decision_agent.name} (Duration: {startup_duration:.3f}s)")
                    print(f"Agents ready: {trend_agent.name}, {news_agent.name}, {decision_agent.name}")

            except Exception as e:
                startup_duration = time.time() - startup_start
                span.set_attribute("error", True)
                span.set_attribute("error_message", str(e))
                span.set_attribute("startup_duration_seconds", round(startup_duration, 3))
                span.record_exception(e)
                if logger:
                    logger.error(f"Error during agent startup: {e}")
                raise
    else:
        # Fallback without telemetry
        print("Starting up and creating agents without telemetry...")
        functions = FunctionTool(user_functions)
        tools_toolset = ToolSet()
        tools_toolset.add(functions)
        agent_client.enable_auto_function_calls(tools_toolset)

        trend_agent = create_trend_agent(agent_client, settings.model_deployment, tools_toolset)
        news_agent = create_news_agent(agent_client, settings.model_deployment, tools_toolset)
        decision_agent = create_decision_agent(agent_client, settings.model_deployment, tools_toolset)

    yield # This separates startup and shutdown

    # Shutdown with telemetry
    shutdown_start = time.time()
    tracer = get_tracer()
    logger = get_logger()
    if tracer:
        with tracer.start_as_current_span("application_shutdown") as span:
            try:
                if logger:
                    logger.info("Shutting down and deleting agents...")
                print("\nShutting down and deleting agents...")

                agents_deleted = 0
                if trend_agent and getattr(trend_agent, "id", None):
                    agent_client.delete_agent(trend_agent.id)
                    agents_deleted += 1
                    span.add_event("TrendAgent deleted")

                if news_agent and getattr(news_agent, "id", None):
                    agent_client.delete_agent(news_agent.id)
                    agents_deleted += 1
                    span.add_event("NewsAgent deleted")

                if decision_agent and getattr(decision_agent, "id", None):
                    agent_client.delete_agent(decision_agent.id)
                    agents_deleted += 1
                    span.add_event("DecisionAgent deleted")

                shutdown_duration = time.time() - shutdown_start
                span.set_attribute("shutdown_duration_seconds", round(shutdown_duration, 3))
                span.set_attribute("agents_deleted", agents_deleted)
                span.set_attribute("success", True)

                if logger:
                    logger.info(f"Agents deleted successfully (Duration: {shutdown_duration:.3f}s)")
                print("Agents deleted.")

            except Exception as e:
                shutdown_duration = time.time() - shutdown_start
                span.set_attribute("error", True)
                span.set_attribute("error_message", str(e))
                span.set_attribute("shutdown_duration_seconds", round(shutdown_duration, 3))
                span.record_exception(e)

                if logger:
                    logger.error(f"Error during agent shutdown: {e}")
                print(f"Error during shutdown: {str(e)}")
                
    else:
        # Fallback without telemetry
        print("\nShutting down and deleting agents without telemetry...")
        if trend_agent and getattr(trend_agent, "id", None):
            agent_client.delete_agent(trend_agent.id)
        if news_agent and getattr(news_agent, "id", None):
            agent_client.delete_agent(news_agent.id)
        if decision_agent and getattr(decision_agent, "id", None):
            agent_client.delete_agent(decision_agent.id)
        print("Agents deleted.")


__all__ = [
    "agent_client",
    "trend_agent",
    "news_agent",
    "decision_agent",
    "tools_toolset",
    "lifespan",
]
