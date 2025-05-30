from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import json

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=os.getenv('OPENAI_API_KEY')
)

# Define output schemas for LLM
response_schemas = [
    ResponseSchema(
        name="analysis",
        description="Analysis of the GitHub event and its potential impact"
    ),
    ResponseSchema(
        name="action_items",
        description="Suggested action items based on the event"
    ),
    ResponseSchema(
        name="priority",
        description="Priority level of the event (HIGH, MEDIUM, LOW)"
    )
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Store events in memory
events = []

def generate_fallback_analysis(event_data):
    """Generate a basic analysis when LLM is unavailable"""
    event_type = event_data.get('type', 'unknown')
    
    analysis = {
        "analysis": f"Received a {event_type} event. LLM analysis unavailable due to API limits.",
        "action_items": ["Review event details manually", "Check back later for AI analysis"],
        "priority": "MEDIUM"
    }
    return analysis

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.json
    
    # Prepare event data for LLM analysis
    event_type = event.get('type', 'unknown')
    event_data = {
        'type': event_type,
        'timestamp': datetime.now().isoformat(),
        'data': event
    }
    
    try:
        # Generate LLM analysis
        prompt = ChatPromptTemplate.from_template("""
        Analyze this GitHub event and provide insights:
        {event}
        
        {format_instructions}
        """)
        
        format_instructions = output_parser.get_format_instructions()
        
        # Get LLM response
        response = llm.invoke(
            prompt.format_messages(
                event=str(event_data),
                format_instructions=format_instructions
            )
        )
        
        analysis = output_parser.parse(response.content)
        event_data['analysis'] = analysis
        
    except Exception as e:
        print(f"Error in LLM analysis: {str(e)}")
        # Use fallback analysis when LLM fails
        event_data['analysis'] = generate_fallback_analysis(event_data)
    
    events.append(event_data)
    return jsonify({'status': 'success', 'event': event_data})

@app.route('/events')
def get_events():
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True) 