# resource_agent.py (updated)
from crewai import Agent, LLM
from tools.search_tool import SearchTool
# from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini LLM
llm = LLM(
    model="gemini/gemini-1.5-flash",  # Specify the provider and model
    temperature=0.5,
    api_key=os.getenv("GEMINI_API_KEY")
)

def create_resource_agent():
    return Agent(
        role="Technical Resource Manager",
        goal="""Source and validate implementation resources including:
        1. Kaggle/HuggingFace datasets
        2. GitHub open-source models
        3. Research papers/case studies
        4. Framework documentation""",
        backstory="Expert ML engineer with 10+ years in technical resource curation",
        tools=[SearchTool()],
        max_iter=7,  # Increased from default 3
        max_rpm=15,  # Rate limiting for API calls
        llm=llm,
        verbose=True,
        memory=True,
        allow_delegation=False,
        step_callback=lambda x: print(f"Resource gathered: {x}")  # Add progress tracking
    )