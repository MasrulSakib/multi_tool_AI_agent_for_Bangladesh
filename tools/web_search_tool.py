"""
web_search_tool.py

This tool is for questions that AREN'T in our three databases - things
like definitions, government policy, or general facts about Bangladesh.
It works by sending the question to the Tavily Search API and returning
the top results. This tool needs its own TAVILY_API_KEY (separate from
the key that configures the LLM itself).
"""

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
    # Step 1: read the Tavily API key from the .env file
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "TAVILY_API_KEY is not set. Add it to your .env file."

    # Step 2: ask Tavily to search the web and give us the top 5 results
    client = TavilyClient(api_key=api_key)
    response = client.search(query=query, max_results=5)
    results = response.get("results", [])

    if not results:
        return "No web results were found for that query."

    # Step 3: turn the results into simple, readable text lines
    lines = []
    for result in results:
        title = result.get("title", "Untitled")
        content = result.get("content", "").strip()
        url = result.get("url", "")
        lines.append(f"- {title}: {content} (source: {url})")

    return "\n".join(lines)
