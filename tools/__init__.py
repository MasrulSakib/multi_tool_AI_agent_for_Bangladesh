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
