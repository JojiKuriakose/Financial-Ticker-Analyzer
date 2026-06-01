"""API routes for analysis endpoints."""
from fastapi import APIRouter
from src.services.telemetry_service import get_tracer, get_logger
from src.agents import manager as agents_manager
from azure.ai.agents.models import MessageRole
import time

router = APIRouter()


@router.post("/analyze/{ticker}")
def execute_analysis(ticker: str):
    tracer = get_tracer()
    logger = get_logger()
    analysis_start = time.time()

    agent_client = agents_manager.agent_client
    trend_agent = agents_manager.trend_agent
    news_agent = agents_manager.news_agent
    decision_agent = agents_manager.decision_agent

    if tracer:
        with tracer.start_as_current_span("execute_analysis") as span:
            try:
                span.set_attribute("ticker", ticker)
                span.set_attribute("endpoint", "/analyze/{ticker}")
                if logger:
                    logger.info(f"Starting analysis for ticker: {ticker}")

                if not trend_agent or not news_agent or not decision_agent:
                    span.set_attribute("error", True)
                    span.set_attribute("error_type", "agents_not_initialized")
                    if logger:
                        logger.warning("Agents are not initialized")
                    return {"error": "Agents are not yet initialized."}, 503

                thread = agent_client.threads.create()
                thread_id = thread.id
                analysis_results = {}

                # Trend
                agent_client.messages.create(thread_id=thread_id, role="user", content=f"Analyze {ticker} price trend.")
                agent_client.runs.create_and_process(thread_id=thread_id, agent_id=trend_agent.id)
                trend_msg = agent_client.messages.get_last_message_text_by_role(thread_id=thread_id, role=MessageRole.AGENT)
                analysis_results["trend_analysis"] = trend_msg.text.value if trend_msg else 'No response'

                # News
                agent_client.messages.create(thread_id=thread_id, role="user", content=f"Summarize recent news for {ticker}.")
                agent_client.runs.create_and_process(thread_id=thread_id, agent_id=news_agent.id)
                news_msg = agent_client.messages.get_last_message_text_by_role(thread_id=thread_id, role=MessageRole.AGENT)
                analysis_results["news_summary"] = news_msg.text.value if news_msg else 'No response'

                # Decision
                agent_client.messages.create(thread_id=thread_id, role="user", content=f"Give a final recommendation for {ticker} based on the above analyses.")
                agent_client.runs.create_and_process(thread_id=thread_id, agent_id=decision_agent.id)
                decision_msg = agent_client.messages.get_last_message_text_by_role(thread_id=thread_id, role=MessageRole.AGENT)
                analysis_results["final_recommendation"] = decision_msg.text.value if decision_msg else 'No response'

                agent_client.threads.delete(thread_id)

                total_duration = time.time() - analysis_start
                span.set_attribute("total_duration_seconds", round(total_duration, 3))
                span.set_attribute("success", True)

                if logger:
                    logger.info(f"Complete analysis for {ticker} finished in {total_duration:.3f}s")

                return analysis_results
            except Exception as e:
                total_duration = time.time() - analysis_start
                span.set_attribute("error", True)
                span.set_attribute("error_message", str(e))
                span.set_attribute("total_duration_seconds", round(total_duration, 3))
                span.record_exception(e)
                if logger:
                    logger.error(f"Error during analysis for {ticker}: {e}")
                try:
                    if 'thread_id' in locals():
                        agent_client.threads.delete(thread_id)
                except:
                    pass
                return {"error": f"Analysis failed: {e}"}, 500
    else:
        if not trend_agent or not news_agent or not decision_agent:
            return {"error": "Agents are not yet initialized."}, 503

        thread = agent_client.threads.create()
        analysis_results = {}

        agent_client.messages.create(thread_id=thread.id, role="user", content=f"Analyze {ticker} price trend.")
        agent_client.runs.create_and_process(thread_id=thread.id, agent_id=trend_agent.id)
        trend_msg = agent_client.messages.get_last_message_text_by_role(thread_id=thread.id, role=MessageRole.AGENT)
        analysis_results["trend_analysis"] = trend_msg.text.value if trend_msg else 'No response'

        agent_client.messages.create(thread_id=thread.id, role="user", content=f"Summarize recent news for {ticker}.")
        agent_client.runs.create_and_process(thread_id=thread.id, agent_id=news_agent.id)
        news_msg = agent_client.messages.get_last_message_text_by_role(thread_id=thread.id, role=MessageRole.AGENT)
        analysis_results["news_summary"] = news_msg.text.value if news_msg else 'No response'

        agent_client.messages.create(thread_id=thread.id, role="user", content=f"Give a final recommendation for {ticker} based on the above analyses.")
        agent_client.runs.create_and_process(thread_id=thread.id, agent_id=decision_agent.id)
        decision_msg = agent_client.messages.get_last_message_text_by_role(thread_id=thread.id, role=MessageRole.AGENT)
        analysis_results["final_recommendation"] = decision_msg.text.value if decision_msg else 'No response'

        agent_client.threads.delete(thread.id)
        return analysis_results


__all__ = ["router"]
