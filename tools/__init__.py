"""
This file makes it easy to import all four tools at once, like this:

    from tools import ALL_TOOLS

instead of importing each tool file one by one. agent.py uses this
list directly to build the single Main Agent.
"""

from .institutions_tool import institutions_db_tool
from .hospitals_tool import hospitals_db_tool
from .restaurants_tool import restaurants_db_tool
from .web_search_tool import web_search_tool

ALL_TOOLS = [
    institutions_db_tool,
    hospitals_db_tool,
    restaurants_db_tool,
    web_search_tool,
]
