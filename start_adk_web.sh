#!/bin/bash

# Start ADK Web Interface for IGotYou Agent
# This launches Google's ADK built-in web chat UI for your agent

echo "=================================================="
echo "🚀 Starting ADK Web Interface for IGotYou Agent"
echo "=================================================="
echo ""
echo "📍 Loading agent from: IGotYou/agent.py"
echo "🌐 Web interface will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the ADK web interface pointing to your agent
# The agent file should export 'root_agent' and 'runner'
adk web IGotYou/agent.py

echo ""
echo "👋 ADK Web Interface stopped"
