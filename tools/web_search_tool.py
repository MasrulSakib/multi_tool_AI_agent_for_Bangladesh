import os

from langchain_core.tools import tool
from tavily import TavilyClient


@tool
def web_search_tool(query: str) -> str:
    """Use this tool for general knowledge questions about Bangladesh
    that are NOT about specific institutions, hospitals, or restaurants
    records - for example definitions, government policy, history, or
    cultural context (e.g. "What is the role of DGHS in Bangladesh?").

    Input is a plain-text search query. Returns a few short web results
    as plain text.
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "TAVILY_API_KEY is not set. Add it to your .env file."

    client = TavilyClient(api_key=api_key)
    response = client.search(query=query, max_results=5)
    results = response.get("results", [])

    if not results:
        return "No web results were found for that query."

    lines = []
    for result in results:
        title = result.get("title", "Untitled")
        content = result.get("content", "").strip()
        url = result.get("url", "")
        lines.append(f"- {title}: {content} (source: {url})")

    return "\n".join(lines)
