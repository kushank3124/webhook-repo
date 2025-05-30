# GitHub Events Monitor

This application monitors GitHub repository events (Push, Pull Request, and Merge) using webhooks and displays them in a clean UI.

## Test Webhook

This is a test commit to verify webhook functionality.

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
4. Create a `.env` file with your MongoDB connection string:
   ```
   MONGODB_URI=mongodb://localhost:27017/
   ```

## Configuring GitHub Webhooks

1. Go to your GitHub repository settings
2. Navigate to "Webhooks" section
3. Click "Add webhook"
4. Set the Payload URL to your server's endpoint: `http://your-server/webhook`
5. Set Content type to `application/json`
6. Select events:
   - Push
   - Pull requests
7. Click "Add webhook"

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open `http://localhost:5000` in your browser
3. The UI will automatically update every 15 seconds with new events

## Features

- Real-time monitoring of GitHub events
- Clean and minimal UI
- Automatic polling every 15 seconds
- Supports Push, Pull Request, and Merge events
- MongoDB storage for event persistence

## Event Formats

- Push: "{author} pushed to {to_branch} on {timestamp}"
- Pull Request: "{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
- Merge: "{author} merged branch {from_branch} to {to_branch} on {timestamp}" 