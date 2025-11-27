# Import the root_agent from the agent module
# Using relative import since this is in the same package
from .agent import root_agent

# Export root_agent for external use
__all__ = ["root_agent"]
