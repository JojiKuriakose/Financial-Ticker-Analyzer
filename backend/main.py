from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services.telemetry_service import configure_telemetry
from src.agents import manager as agents_manager
from src.routes.analyze import router as analyze_router
from src.config.settings import settings
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Configure telemetry first so modules can read tracer/logger at runtime
configure_telemetry()

# Create FastAPI app with the lifespan from the agent manager
app = FastAPI(lifespan=agents_manager.lifespan)


# Configure OpenTelemetry instrumentation for FastAPI
if settings.app_insights_connection_string:
    # Instrument FastAPI for automatic request tracing
    FastAPIInstrumentor.instrument_app(app)
    
    # Instrument requests library for external API calls
    RequestsInstrumentor().instrument()
    
    # Instrument logging for structured logs
    LoggingInstrumentor().instrument(set_logging_format=True)
    
    print("OpenTelemetry instrumentation configured for FastAPI, requests, and logging")
else:
    print("Application Insights connection string not found - instrumentation skipped")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(analyze_router)
