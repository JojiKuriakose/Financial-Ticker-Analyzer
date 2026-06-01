import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")
    app_insights_connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    
settings = Settings()