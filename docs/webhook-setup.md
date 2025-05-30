# Webhook Setup with LLM Integration

This document describes how to set up and use the GitHub webhook monitoring system with LLM-powered analysis.

## Features

- Real-time monitoring of GitHub events
- Intelligent event analysis using GPT-3.5
- Priority-based event categorization
- Actionable insights for each event

## LLM Analysis

The system uses OpenAI's GPT-3.5 to analyze each GitHub event and provides:
1. Event impact analysis
2. Suggested action items
3. Priority level (HIGH, MEDIUM, LOW)

## Webhook Configuration

1. Go to your GitHub repository settings
2. Navigate to "Webhooks" section
3. Add webhook with:
   - Payload URL: Your ngrok URL + `/webhook`
   - Content type: `application/json`
   - Events: Push, Pull Request, Merge

## Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENAI_API_KEY=your_key_here" > .env
```

## Running the Application

1. Start Flask server:
   ```bash
   python app.py
   ```

2. Start ngrok tunnel:
   ```bash
   ngrok http 5000
   ```

3. Configure GitHub webhook with the ngrok URL

## Event Analysis Example

When a push event occurs, the LLM will analyze:
- Code changes impact
- Potential risks
- Required review priority
- Suggested next steps 