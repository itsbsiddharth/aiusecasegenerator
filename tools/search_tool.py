# search_tool.py (corrected)
from crewai.tools import BaseTool
from tavily import TavilyClient
from typing import Optional
import os

class SearchTool(BaseTool):
    name: str = "SearchTool"  # Proper type annotation
    description: str = "A tool to search the web for information about a company or industry."  # Proper type annotation

    def _run(self, query: str) -> str:
        try:
            # Get the Tavily API key from environment variables
            tavily_api_key = os.getenv("TAVILY_API_KEY")
            if not tavily_api_key:
                raise ValueError("Tavily API key not found in environment variables.")

            tavily = TavilyClient(api_key=tavily_api_key)
            response = tavily.search(query=query, max_results=5)
            
            # Format the results
            formatted_results = []
            for result in response.get('results', []):
                formatted_results.append(
                    f"""### {result.get("title", "No Title")}
                    **Source**: [{result.get("url", "Unknown source")}]({result.get("url", "Unknown source")})
                    **Content**: {result.get("content", "No content available")[:500]}...
                    """
                )

                
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Search error: {str(e)}"