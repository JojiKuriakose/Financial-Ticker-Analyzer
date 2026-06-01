"""Telemetry helpers for Microsoft Foundry tracing and Azure Monitor."""
import logging

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.config.settings import settings


def configure_telemetry():
    """Configure OpenTelemetry with Azure Monitor"""
    if not settings.app_insights_connection_string:
        logging.warning("APPLICATIONINSIGHTS_CONNECTION_STRING not found - telemetry disabled")
        return None, None
    
    # Configure trace provider
    trace_provider = TracerProvider()
    trace.set_tracer_provider(trace_provider)
    
    # Add Azure Monitor trace exporter
    trace_exporter = AzureMonitorTraceExporter(connection_string=settings.app_insights_connection_string)
    span_processor = BatchSpanProcessor(trace_exporter)
    trace_provider.add_span_processor(span_processor)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Get tracer for custom spans
    tracer = trace.get_tracer(__name__)
    
    logging.info("OpenTelemetry telemetry configured successfully with Azure Monitor")
    return tracer, logger

tracer, logger = configure_telemetry()

def get_tracer():
    return tracer

def get_logger():
    return logger

__all__ = [
    "configure_telemetry",
    "get_tracer",
    "get_logger"
]
