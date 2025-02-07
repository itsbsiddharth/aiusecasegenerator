# use_case_agent.py (updated)
from crewai import Agent, LLM
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

def create_use_case_agent():
    return Agent(
        role="Chief AI Solutions Architect",
        goal="Identify high-impact AI implementation opportunities Propose relevant use cases where the company can leverage GenAI, LLMs, and ML technologies to improve their processes, enhance customer satisfaction, and boost operational efficiency",
        backstory="""AI strategist with proven track record of delivering enterprise-grade 
        GenAI solutions across Fortune 500 companies.""",
        llm=llm,
        verbose=True,
        memory=True,
        allow_delegation=False,
        max_iter=5
    )