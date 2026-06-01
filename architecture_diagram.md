# Financial Ticker Analyser - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          END USER                                        │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                                  │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  • Interactive Chat UI                                           │   │
│  │  • Session State Management                                      │   │
│  │  • User Input Processing (Ticker Symbols)                        │   │
│  │  • Response Display (JSON/Charts)                                │   │
│  │  Stack: Streamlit 1.54.0, Plotly 6.5.2, Pandas 2.3.3           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────────────────┘
                         │
                         │ HTTP/REST
                         │ POST /analyze/{ticker}
                         │
┌────────────────────────▼──────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                                       │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  CORE API SERVER                                                   │   │
│  │  • Route Handler: /analyze/{ticker}                               │   │
│  │  • Request Routing & Orchestration                                │   │
│  │  • OpenTelemetry Instrumentation (Logging, Tracing, Metrics)    │   │
│  │  Stack: FastAPI 0.128.6, Uvicorn 0.40.0                         │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                         │                                                   │
│        ┌────────────────┼────────────────┬───────────────┐                 │
│        │                │                │               │                 │
│        ▼                ▼                ▼               ▼                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │  TOOLS       │ │   DATA       │ │    AI        │ │  TELEMETRY   │     │
│  │  LIBRARY     │ │  FETCHERS    │ │   AGENTS     │ │  EXPORTER    │     │
│  │              │ │              │ │              │ │              │     │
│  │ • Stock Data │ │ • yfinance   │ │ • Trend      │ │ • Azure      │     │
│  │   Analysis   │ │   (Market    │ │   Analysis   │ │   Monitor    │     │
│  │ • Web Search │ │   Data)      │ │   Agent      │ │   Exporter   │     │
│  │   (DuckDuck  │ │ • DuckDuck   │ │ • News       │ │ • Tracing    │     │
│  │   Go)        │ │   Search     │ │   Research   │ │ • Metrics    │     │
│  │ • Data       │ │   (Web Info) │ │   Agent      │ │ • Logging    │     │
│  │   Processing │ │              │ │ • Decision   │ │              │     │
│  │ • Pandas     │ │              │ │   Agent      │ │              │     │
│  │   Operations │ │              │ │              │ │              │     │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘     │
└────────────────────┬──────────────────────┬──────────────────────┬────────┘
                     │                      │                      │
          ┌──────────▼────────┐  ┌─────────▼─────────┐  ┌────────▼────────┐
          │                   │  │                   │  │                 │
          ▼                   ▼  ▼                   ▼  ▼                 │
┌──────────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐
│  │  MARKET DATA         │  │  WEB SEARCH          │  │  AZURE AI        │
│  │  ┌────────────────┐  │  │  ┌────────────────┐  │  │  ┌────────────┐  │
│  │  │ yFinance API   │  │  │  │ DuckDuckGo API │  │  │  │ Agents     │  │
│  │  │ (Real-time &   │  │  │  │ (News & Info)  │  │  │  │ Service    │  │
│  │  │  Historical)   │  │  │  │                │  │  │  │            │  │
│  │  └────────────────┘  │  │  └────────────────┘  │  │  │ Hosted on  │  │
│  │                      │  │                      │  │  │ Azure ML   │  │
│  └──────────────────────┘  └──────────────────────┘  │  │ Workspace  │  │
│                                                      │  └────────────┘  │
│                                                      └──────────────────┘
│  ┌──────────────────────┐
│  │  MONITORING          │
│  │  ┌────────────────┐  │
│  │  │ Application    │  │
│  │  │ Insights       │  │
│  │  │ (Traces,       │  │
│  │  │  Metrics,      │  │
│  │  │  Logs)         │  │
│  │  └────────────────┘  │
│  └──────────────────────┘
└──────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer
- **Technology**: Streamlit (Python web framework)
- **Purpose**: Provide interactive user interface for querying stock tickers
- **Key Features**:
  - Chat-based UI for user interaction
  - Session state management for conversation history
  - JSON response display and visualization
  - HTTP client for API communication

### Backend Layer
- **Technology**: FastAPI with Uvicorn ASGI server
- **Purpose**: Core API server and orchestration layer
- **Responsibilities**:
  - Accept ticker analysis requests
  - Coordinate data fetching and AI agent execution
  - Handle telemetry and observability

### Data Fetchers
- **yFinance**: Retrieves historical and real-time stock market data
- **DuckDuckGo Search**: Searches for financial news and information
- **Pandas**: Data manipulation and analysis

### AI Agents (Azure AI Agents)
- **Trend Agent**: Analyzes stock price trends and patterns
- **News Agent**: Researches latest financial news for the ticker
- **Decision Agent**: Synthesizes data into investment recommendations

### Observability Stack
- **OpenTelemetry**: Instrumentation framework
  - FastAPI instrumentation
  - HTTP request tracing
  - Logging integration
- **Azure Monitor**: Centralized monitoring and alerting
  - Application Insights integration
  - Trace exporting
  - Metrics collection
  - Log aggregation

## Data Flow

```
User Input (Ticker)
        │
        ▼
    Streamlit UI
        │
        ▼
    FastAPI /analyze/{ticker}
        │
        ├─► Trend Agent ─────► Fetch Stock Data (yFinance)
        │                      Analyze Trends & Patterns
        │
        ├─► News Agent ──────► Search Web (DuckDuckGo)
        │                      Fetch Financial News
        │
        └─► Decision Agent ───► Synthesize Analysis
                                Generate Recommendations
        │
        ▼
    JSON Response
        │
        ▼
    Display in Streamlit UI
```

## Technology Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | Streamlit | 1.54.0 |
| | Plotly | 6.5.2 |
| | Pandas | 2.3.3 |
| **Backend** | FastAPI | 0.128.6 |
| | Uvicorn | 0.40.0 |
| | Pandas | 3.0.0 |
| | NumPy | 2.4.2 |
| **AI/ML** | Azure AI Agents | 1.1.0 |
| | Azure Identity | 1.25.1 |
| **Data Sources** | yfinance | 1.1.0 |
| | DuckDuckGo Search | 8.1.1 |
| **Observability** | OpenTelemetry | 1.39.0 |
| | Azure Monitor | 1.0.0b48 |
| **Python** | 3.13+ |

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Azure Cloud Environment                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Azure ML Workspace / App Service                 │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Backend Service (FastAPI + Uvicorn)        │  │  │
│  │  │  • Port: 8000                                │  │  │
│  │  │  • Environment: managed                      │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Azure AI Agents Service                    │  │  │
│  │  │  • Hosted agent infrastructure              │  │  │
│  │  │  • Multiple specialized agents              │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Application Insights                       │  │  │
│  │  │  • Monitoring & Diagnostics                 │  │  │
│  │  │  • Trace storage & analysis                 │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Frontend Deployment (Optional)                   │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Streamlit App (Cloud Deployment)          │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Key Integration Points

1. **API Contract**: Frontend communicates with Backend via REST API
   - Endpoint: `POST http://localhost:8000/analyze/{ticker}`
   - Request: Ticker symbol
   - Response: JSON with trend analysis, news, and recommendations

2. **Azure AI Integration**: Backend uses Azure Agents SDK
   - Credentials: Default Azure credentials (DefaultAzureCredential)
   - Endpoint: Project endpoint from environment
   - Model: Configured via MODEL_DEPLOYMENT_NAME

3. **Observability Integration**: Distributed tracing across layers
   - Backend instruments FastAPI, requests, logging
   - Azure Monitor receives traces and metrics
   - Custom spans track key operations

4. **Configuration**: Environment variables
   - `PROJECT_ENDPOINT`: Azure AI Agents endpoint
   - `MODEL_DEPLOYMENT_NAME`: Azure model deployment
   - `APPLICATIONINSIGHTS_CONNECTION_STRING`: Monitoring connection
   - `.env` file in project root
