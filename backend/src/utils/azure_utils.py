from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from src.config.settings import settings

agent_client=AgentsClient(
    endpoint=settings.project_endpoint, 
    credential=DefaultAzureCredential()
    )