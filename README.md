# GitHub Events Monitor

This application monitors GitHub repository events (Push, Pull Request, and Merge) using webhooks and displays them in a clean UI with LLM-powered analysis.

## Features

- Real-time monitoring of GitHub events
- Intelligent event analysis using GPT-3.5
- Priority-based event categorization
- Actionable insights for each event
- Clean and modern UI with automatic updates

## Test Webhook

This is a test commit to verify webhook functionality with LLM integration.
Testing webhook with ngrok integration - [Timestamp: 2024-03-14]

## Setup Instructions

1. Clone this repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your OpenAI API key in `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Start ngrok tunnel:
   ```bash
   ngrok http 5000
   ```
3. Open the ngrok URL in your browser
4. Configure GitHub webhooks with the ngrok URL

## Event Analysis

The system uses OpenAI's GPT-3.5 to analyze each event and provides:
- Impact analysis
- Suggested action items
- Priority level (HIGH, MEDIUM, LOW)

For detailed setup instructions, see [Webhook Setup Guide](docs/webhook-setup.md)
