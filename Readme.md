# Project Overview
This project implements a Health Analysis API using Crew AI agents, integrated with Flask for the backend. The API allows users to upload a PDF containing a blood test report, which is analyzed by various agents to provide insights and health recommendations. The system sends these insights along with relevant health articles to the user's email.

# Features:
User Authentication: Authenticate users with JWT tokens.
PDF Blood Test Analysis: Extracts data from uploaded PDF files and uses AI to analyze the report.
Health Article Search: Agents search the web for relevant health articles based on the analysis.
Email Notifications: Sends the analysis, health recommendations, and article links to the user via email. 

# Approach and Methodology
Crew AI Framework: This API uses Crew AI agents, each specialized in a task:

Blood Test Analyst Agent: Analyzes the blood test data.

Article Researcher Agent: Searches the web for health articles based on the results.

Health Advisor Agent: Provides health recommendations based on the research.

Tasks Delegation: The tasks are handled by different agents using a Task-Oriented methodology, with each agent focusing on a specific responsibility. Tasks are defined in the agents folder for better code modularity.

Integration with Flask: Flask acts as the backend web framework to expose API endpoints that allow users to authenticate, upload PDFs, and receive email notifications.

NLP Tools: The project uses NLP-based models (e.g., Ollama model) to enhance understanding and processing of health-related data from PDFs.

External Tools:

Web Search Tool: An agent-based tool to fetch relevant health articles using Google Custom Search API.
Email Utility: Sends the results to users via email.
Project Structure
bash
Copy code
├── agents/                 # Folder containing agent setup for various tasks
│   ├── __init__.py
│   ├── agents.py           # Define agents and tasks
├── utils/
│   ├── email_utils.py      # Function to send emails
│   ├── pdf_utils.py        # Function to extract text from PDFs
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── requirements.txt        # Python package dependencies
└── README.md               # This documentation

# Setup Instructions
1. Clone the Repository

git clone https://github.com/yourusername/crewai_health_analysis.git
cd crewai_health_analysis

2. Set Up a Virtual Environment (optional but recommended)

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

3. Install Dependencies
Install the required packages using pip:
pip install -r requirements.txt

5. Configure Environment Variables
Create a .env file in the root directory to store your API keys, email credentials, and other sensitive data:


- GOOGLE_API_KEY=your_google_api_key
- SEARCH_ENGINE_ID=your_custom_search_engine_id
- EMAIL_FROM=email_host
- GOOGLE_API_KEY
- MJ_APIKEY_PRIVATE = Mailjet secret key
- MJ_APIKEY_PUBLIC = Mailjet public key
- OPEN_API_KEY

5. Run the Application
Ensure you are in the project root directory, then run:

python app.py
This will start the Flask server on http://localhost:5000.

# How to Use the API (Postman Guide)
1. Login and Authentication (/login)
Request:
URL: http://localhost:5000/login
Method: POST
Body (raw JSON):
json
Copy code
{
  "username": "user",
  "password": "pass"
}
Response:
Returns a JWT access token for authentication.


3. Analyze Blood Test Report (/analyze)
Request:
URL: http://localhost:5000/analyze
Method: POST
Authorization: Bearer Token (JWT Token from /login)
Body (form-data):
pdf: Upload the PDF file of the blood test report.
email: Provide the email where results should be sent.
Response:
A JSON response containing:
analysis: Summary of blood test findings.
recommendations: Health recommendations.
articles: Links to relevant health articles.

5. Default Route (/)
Request:
URL: http://localhost:5000/
Method: GET
Response: Displays a welcome message with Postman usage instructions.


# Methodology Behind the Agents
Agent 1: Blood Test Analyst:

This agent uses the extracted text from the PDF to analyze the blood test data and provide a concise summary.
Agent 2: Article Researcher:

This agent performs web searches based on the analysis and finds relevant articles on health topics related to the report.
Agent 3: Health Advisor:

This agent reviews the found articles and suggests health tips or recommendations based on the blood test and article information.
Each agent performs its task using AI models and NLP tools to interpret the data and provide meaningful results to the user.

Troubleshooting
Server Not Starting: Ensure all dependencies are installed correctly (pip install -r requirements.txt).

Module Import Errors: Double-check the Python environment, especially if using a virtual environment, and ensure you have activated it.

PDF File Not Uploading: Make sure to send the request as form-data in Postman with pdf as a key.

API Keys Not Working: Verify that the Google API key and custom search engine ID are correct and set in the .env file.

Mail Not recieved: Check Spam folder
