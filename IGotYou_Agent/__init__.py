from .agent import root_agent
from google.adk.runners import InMemoryRunner

# Create a runner instance that can be used by the backend
runner = InMemoryRunner(agent=root_agent)

__all__ = ["root_agent", "runner"]
