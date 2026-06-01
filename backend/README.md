
# Backend — Financial Ticker Analyser

This folder contains the FastAPI backend and modular service code for the Financial Ticker Analyser project.

## Layout (important files)

- `main.py` — application bootstrap (includes FastAPI app wiring).
- `run.py` — tiny runner for development (uses `uvicorn`).
- `requirements.txt` — Python dependencies used for the backend.
- `src/` — application package
	- `src/config` — environment/config helpers
	- `src/telemetry.py` — OpenTelemetry + Azure Monitor helpers
	- `src/services` — data fetchers (`fetch_stock_data`, `fetch_latest_news`)
	- `src/agents` — agent factories and manager (Trend/News/Decision)
	- `src/routes` — FastAPI routers (e.g. `analyze`)

## Environment variables
Create a `.env` at the backend root or set environment variables in your environment. The app reads these via `python-dotenv`.

- `PROJECT_ENDPOINT` — Azure project/agent endpoint
- `MODEL_DEPLOYMENT_NAME` — model deployment name used by agents
- `APPLICATIONINSIGHTS_CONNECTION_STRING` — (optional) App Insights connection string for telemetry

If using `DefaultAzureCredential` (recommended for non-local flows) you may also need:
- `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET` — for service principal authentication

## Install dependencies

Using PowerShell:

```powershell
python -m pip install -r requirements.txt
```

If you use a virtual environment, activate it first.

## Run (development)

Start the server with the provided `run.py`:

```powershell
python run.py
```

Or run `uvicorn` directly:

```powershell
uvicorn main:app --reload --host localhost --port 8000
```

The primary API endpoint:

- `POST /analyze/{ticker}` — run a quick analysis for the given ticker (e.g. `HAL.NS`).

Example request (PowerShell/curl):

```powershell
curl -X POST http://localhost:8000/analyze/HAL.NS
```

## Notes

- Telemetry is enabled only when `APPLICATIONINSIGHTS_CONNECTION_STRING` is set; otherwise the app runs without instrumentation.
- The app uses `DefaultAzureCredential` to authenticate with Azure. For local testing you can run `az login` (Azure CLI) or supply client credentials in env variables.
- Agent creation is performed in the FastAPI lifespan; startup may take a few seconds while agents are created on your Azure project.

## Where to look next

- Implement additional routes in `src/routes`.
- Add unit tests (mock `agent_client`) and CI tasks.

