# main.py (updated)
from crewai import Crew, Task,LLM
from agents.research_agent import create_research_agent
from agents.use_case_agent import create_use_case_agent
from agents.resource_agent import create_resource_agent
from dotenv import load_dotenv
import os
# from langchain_google_genai import ChatGoogleGenerativeAI
import litellm
os.environ['LITELLM_LOG'] = 'DEBUG' 
# Add to main.py before initializing LLM
litellm.drop_params = True
litellm.api_base = "https://generativelanguage.googleapis.com/v1beta/models/"



load_dotenv()
litellm.set_verbose = True  # Enable verbose logging
# Initialize the Gemini LLM
llm = LLM(
    model="gemini/gemini-1.5-flash",  # Specify the provider and model
    temperature=0.3,
    api_key=os.getenv("GEMINI_API_KEY")
)

def crew(company_name: str, industry: str):
    

    # Create agents
    research_agent = create_research_agent()
    use_case_agent = create_use_case_agent()
    resource_agent = create_resource_agent()

    # Define tasks with improved prompts
    research_task = Task(
        description=f"""Conduct comprehensive analysis of:
        1. {industry} industry trends, challenges, and opportunities
        2. {company_name}'s market position and competitors
        3. Current technology adoption in the sector
        4. Customer demographics and pain points""",
        expected_output="Structured report with industry overview, SWOT analysis, and technology landscape.",
        agent=research_agent,
        output_file="industry_analysis.md"
    )

    use_case_task = Task(
        description=f"""Generate 7-10 practical AI/GenAI use cases for {company_name} considering:
        1. Operational efficiency improvements
        2. Customer experience enhancement
        3. Revenue growth opportunities
        4. Risk reduction strategies
        Prioritize use cases with high impact and feasibility.""",
        expected_output="Prioritized list of use cases with implementation roadmap and success metrics.",
        agent=use_case_agent,
        context=[research_task],
        output_file="use_cases.md"
    )

    resource_task = Task(
        description=f"""For each approved use case,Iteratively gather resources for each use case with clickable links. collect:
        1. Relevant datasets from Kaggle/HuggingFace
        2. Open-source models from GitHub
        3. Research papers and case studies
        4. Tools and frameworks required
        Include links and brief descriptions.""",
        expected_output="Curated resource list with technical specifications and implementation guides.",
        agent=resource_agent,
        context=[use_case_task],
        output_file="resources.md"
    )

    # Create and run crew
    ai_crew = Crew(
        agents=[research_agent, use_case_agent, resource_agent],
        tasks=[research_task, use_case_task, resource_task],
        llm=llm,
        verbose=True,
        process="sequential"
    )

    result = ai_crew.kickoff()
    
    # Format output for Streamlit
    return {
        "tasks_output": [
            research_task.output.raw,
            use_case_task.output.raw,
            resource_task.output.raw
        ]
    }

