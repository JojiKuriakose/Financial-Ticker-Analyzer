# Financial Ticker Analyser
## Problem Statement
**Challenge**: Investors and financial analysts struggle to make informed investment decisions due to:

   1. **Information Fragmentation** - Stock market data, news, and trends exist across multiple sources (market APIs, news feeds, research reports), requiring manual aggregation.
   2. **Analysis Paralysis** - Too much unstructured information to process manually; requires synthesizing multiple perspectives (technical analysis, sentiment, fundamentals) into actionable insights.
   3. **Time Constraints** - Manual analysis of each ticker is time-consuming, limiting the number of stocks investors can analyze before trading decisions.
   4. **Lack of Unified Intelligence** - No single tool combines:
       - **Real-time market data** (price trends, historical performance)
       - **Recent news & sentiment** (company announcements, industry events)
       - **Intelligent recommendations** (synthesized buy/hold/sell signals)
   5. **Scalability & Observability** - Need to track system performance, identify bottlenecks, and ensure reliable operation in production.

## Solution Overview
Financial Ticker Analyser is a **multi-agent AI system** that provides intelligent, end-to-end stock analysis through **orchestrated autonomous agents** powered by **Microsoft Foundry**.<br>
Key Solution Elements:
1. Three Specialized Agents (Microsoft Foundry Agent Service)
  - Trend Analysis Agent → Analyzes price patterns, historical data, technical indicators
  - News Research Agent → Summarizes recent news, company announcements, market sentiment
  - Decision Agent → Synthesizes findings from other agents into a final buy/hold/sell recommendation
2. Integrated Data Services
  - yFinance API - Real-time and historical stock data
  - DuckDuckGo API - Web search for news and company information
  - Data Processing - Pandas-based analysis and transformation
3. Dual Interface
  - REST API (/analyze/{ticker}) - Backend endpoint for programmatic access
  - Streamlit UI - Interactive chat interface for end users
4. Production-Ready Observability
  - OpenTelemetry Instrumentation - Auto-tracing of requests, external API calls, and logging
  - Azure Application Insights - Centralized monitoring, metrics, and diagnostics
  - Structured Logging - Trace each analysis step for debugging and optimization
5. Scalable Architecture
  - FastAPI + Uvicorn - High-performance async HTTP server
  - CORS Enabled - Frontend-backend communication
  - Thread Management - Proper cleanup and resource management during agent execution
    <br>
    <br>
This solution transforms financial analysis from a time-consuming manual process into an intelligent, automated, scalable service powered by **agentic AI**.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python, FastAPI, uvicorn
- **AI/ML**: Microsoft Foundry Agents, Azure Identity
- **External API**: yfinance, DuckDuckGo Search
- **Observability**: OpenTelemetry, Azure Monitor

## Key Features
✅ **Speed** - Complete analysis in seconds vs. hours of manual research<br>
✅ **Accuracy** - Multiple AI perspectives reduce bias, cross-validate findings<br>
✅ **Scalability** - Analyze unlimited tickers without adding resources<br>
✅ **Transparency** - Each step traced and logged for compliance & debugging<br>
✅ **Intelligence** - Agents collaborate autonomously with shared context<br>

## Application Architecture
<img width="1024" height="1536" alt="Ticker Architecture" src="https://github.com/user-attachments/assets/675bb4e4-2f21-4d1a-b125-26c438df493a" />








