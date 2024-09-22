from crewai import Agent, Task, Crew
from crewai_tools import BaseTool
import os
import requests
from langchain.llms import Ollama

# if you dont want to use CHATgpt, then uncomment the below line and use llm=ollama_openhermes for all agents.
#ollama_openhermes = Ollama(model="openhermes")  

class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Search for health articles based on blood test results."

    def _run(self, query: str) -> list:
        api_key = os.getenv("GOOGLE_API_KEY")
        search_engine_id = os.getenv("SEARCH_ENGINE_ID")
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}"
        
        response = requests.get(url)
        articles = response.json().get('items', [])
        return [(article['title'], article['link']) for article in articles]

# Create an instance of the tool
web_search_tool = WebSearchTool()

# Create agents
blood_test_analyst = Agent(
    role='Blood Test Analyst',
    goal='Analyze the blood test report and summarize the findings.',
    backstory='A medical expert specializing in blood test analysis.',
    verbose=True,
    allow_delegation=False,
    llm="gpt-4o", 
)

article_researcher = Agent(
    role='Article Researcher',
    goal='Search for health articles based on blood test results.',
    backstory='An expert researcher proficient in finding health-related articles.',
    tools=[web_search_tool],  
    verbose=True,
    allow_delegation=False,
    llm="gpt-4o", 
)

health_advisor = Agent(
    role='Health Advisor',
    goal='Provide health recommendations based on the articles found.',
    backstory='A health advisor with extensive knowledge in providing health advice.',
    verbose=True,
    allow_delegation=False,
    llm="gpt-4o", 
)

# Function to create tasks for agents
def create_tasks(raw_text):
    analyze_blood_test_task = Task(
        description=f'You have to analyze the blood test report from the following data: "{raw_text}"',
        expected_output='A summary of the blood test results.',
        agent=blood_test_analyst,
    )

    find_articles_task = Task(
        description='Search for health articles based on the blood test analysis.',
        expected_output='A list of relevant health articles with links.',
        agent=article_researcher,
        context=[analyze_blood_test_task]
    )

    provide_recommendations_task = Task(
        description='Provide health recommendations based on the articles found.',
        expected_output='Health recommendations with links to the articles.',
        agent=health_advisor,
        context=[find_articles_task]
    )

    crew = Crew(
        agents=[blood_test_analyst, article_researcher, health_advisor],
        tasks=[analyze_blood_test_task, find_articles_task, provide_recommendations_task],
        verbose=True
    )

    return crew
