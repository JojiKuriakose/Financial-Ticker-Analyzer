"""Data fetching services: stock history and news."""
from typing import Dict, Any, Optional
import time
import datetime
import yfinance as yf
from duckduckgo_search import DDGS
import pandas as pd
from src.services.telemetry_service import get_tracer, get_logger



def fetch_stock_data(ticker: str = "HAL.NS", period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    """Fetch historical stock data using yfinance."""
    tracer = get_tracer()
    logger = get_logger()
    start_time = time.time()

    if tracer:
        with tracer.start_as_current_span("fetch_stock_data") as span:
            try:
                span.set_attribute("ticker", ticker)
                span.set_attribute("period", period)
                span.set_attribute("interval", interval)

                if logger:
                    logger.info(f"Fetching stock data for ticker: {ticker}, period: {period}, interval: {interval}")

                stock = yf.Ticker(ticker)
                df = stock.history(period=period, interval=interval)
                df.reset_index(inplace=True)
                df["Date"] = pd.to_datetime(df["Date"]).dt.date.astype(str)

                duration = time.time() - start_time
                row_count = len(df)

                span.set_attribute("rows_returned", row_count)
                span.set_attribute("duration_seconds", round(duration, 3))
                span.set_attribute("success", True)

                if logger:
                    logger.info(f"Stock data fetched successfully - Ticker: {ticker}, Rows: {row_count}, Duration: {duration:.3f}s")

                return df
            except Exception as e:
                duration = time.time() - start_time
                span.set_attribute("error", True)
                span.set_attribute("error_message", str(e))
                span.set_attribute("duration_seconds", round(duration, 3))
                span.record_exception(e)
                if logger:
                    logger.error(f"Error fetching stock data for {ticker}: {e}")
                raise
    else:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        df.reset_index(inplace=True)
        df["Date"] = pd.to_datetime(df["Date"]).dt.date.astype(str)
        return df


def fetch_latest_news(query: str = "Hindustan Aeronautics Limited HAL stock India", max_results: int = 5) -> Dict[str, Any]:
    """Fetch recent headlines using DuckDuckGo News."""
    tracer = get_tracer()
    logger = get_logger()
    start_time = time.time()

    if tracer:
        with tracer.start_as_current_span("fetch_latest_news") as span:
            try:
                span.set_attribute("query", query)
                span.set_attribute("max_results", max_results)
                if logger:
                    logger.info(f"Fetching news with query: {query}, max_results: {max_results}")

                items = []
                with DDGS() as ddgs:
                    for r in ddgs.news(query, max_results=max_results):
                        items.append({
                            "title": r.get("title"),
                            "source": r.get("source"),
                            "date": r.get("date"),
                            "url": r.get("url"),
                            "snippet": r.get("body") or r.get("excerpt") or r.get("snippet"),
                        })

                duration = time.time() - start_time
                news_count = len(items)
                span.set_attribute("news_items_returned", news_count)
                span.set_attribute("duration_seconds", round(duration, 3))
                span.set_attribute("success", True)

                if logger:
                    logger.info(f"News fetched successfully - Query: {query}, Items: {news_count}, Duration: {duration:.3f}s")

                return {"query": query, "fetched_at": datetime.datetime.utcnow().isoformat() + "Z", "items": items}
            except Exception as e:
                duration = time.time() - start_time
                span.set_attribute("error", True)
                span.set_attribute("error_message", str(e))
                span.set_attribute("duration_seconds", round(duration, 3))
                span.record_exception(e)
                if logger:
                    logger.error(f"Error fetching news for query '{query}': {e}")
                raise
    else:
        items = []
        with DDGS() as ddgs:
            for r in ddgs.news(query, max_results=max_results):
                items.append({
                    "title": r.get("title"),
                    "source": r.get("source"),
                    "date": r.get("date"),
                    "url": r.get("url"),
                    "snippet": r.get("body") or r.get("excerpt") or r.get("snippet"),
                })
        return {"query": query, "fetched_at": datetime.datetime.utcnow().isoformat() + "Z", "items": items}


user_functions = {fetch_stock_data, fetch_latest_news}

__all__ = ["fetch_stock_data", "fetch_latest_news", "user_functions"]
