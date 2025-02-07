# research_agent.py (updated)
from crewai import Agent, LLM
from tools.search_tool import SearchTool
# from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini LLM
llm = LLM(
    model="gemini/gemini-1.5-flash",  # Specify the provider and model
    temperature=0.3,
    api_key=os.getenv("GEMINI_API_KEY")
)

def create_research_agent():
    return Agent(
        role="Senior Industry Analyst",
        goal="Provide deep insights into market trends and company positioning but keep it very information dense and concise.",
        backstory="""A seasoned analyst with 15+ years experience in market intelligence and 
        competitive analysis across multiple industries.""",
        tools=[SearchTool()],
        llm=llm,
        verbose=True,
        memory=True,
        max_iter=3
    )