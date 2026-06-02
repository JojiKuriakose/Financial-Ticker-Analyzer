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
  - **Trend Analysis Agent** → Analyzes price patterns, historical data, technical indicators
  - **News Research Agent** → Summarizes recent news, company announcements, market sentiment
  - **Decision Agent** → Synthesizes findings from other agents into a final buy/hold/sell recommendation
2. Integrated Data Services
  - **yFinance API** - Real-time and historical stock data
  - **DuckDuckGo API** - Web search for news and company information
  - **Data Processing** - Pandas-based analysis and transformation
3. Dual Interface
  - **REST API (/analyze/{ticker})** - Backend endpoint for programmatic access
  - **Streamlit UI** - Interactive chat interface for end users
4. Production-Ready Observability
  - **OpenTelemetry Instrumentation** - Auto-tracing of requests, external API calls, and logging
  - **Azure Application Insights** - Centralized monitoring, metrics, and diagnostics
  - **Structured Logging** - Trace each analysis step for debugging and optimization
5. Scalable Architecture
  - **FastAPI + Uvicorn** - High-performance async HTTP server
  - **CORS Enabled** - Frontend-backend communication
  - **Thread Management** - Proper cleanup and resource management during agent execution
    <br>
    <br>
This solution transforms financial analysis from a time-consuming manual process into an intelligent, automated, scalable service powered by **agentic AI**.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python, FastAPI, uvicorn
- **AI/ML**: Microsoft Foundry Agents, Azure Identity, LLM
- **External API**: yfinance, DuckDuckGo Search
- **Observability**: OpenTelemetry, Azure Monitor

## Key Features
✅ **Speed** - Complete analysis in seconds vs. hours of manual research<br>
✅ **Accuracy** - Multiple AI perspectives reduce bias, cross-validate findings<br>
✅ **Scalability** - Analyze unlimited tickers without adding resources<br>
✅ **Transparency** - Each step traced and logged for compliance & debugging<br>
✅ **Intelligence** - Agents collaborate autonomously with shared context<br>

## Application Architecture
<img width="512" height="681" alt="Ticker Architecture" src="https://github.com/user-attachments/assets/675bb4e4-2f21-4d1a-b125-26c438df493a" />
<br>

## Application Demo
<br>
<img width="1902" height="966" alt="Screenshot 2026-06-01 182214" src="https://github.com/user-attachments/assets/244099da-1032-4ca5-a86b-8c41717a4c94" />
<br>

## Metrics
- **Server Reponse Time(latency-p95)**: 2.62 mins<br>
- **Prompt token count**: 670 avg per request(3.35K)[no. of requests=5]<br>
- **Completion token count**: 1045 avg per request(5.22K)[no. of requests=5]<br>










