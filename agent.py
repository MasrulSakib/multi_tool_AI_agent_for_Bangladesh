import os

from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

from tools import ALL_TOOLS

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError("Please set GROQ_API_KEY in your .env file.")

llm = ChatGroq(model=MODEL_NAME, api_key=GROQ_API_KEY, temperature=0)

SYSTEM_PROMPT = """
You are a helpful assistant for questions about Bangladesh.

Routing rules:
1. If the question asks for specific data, counts, or statistics about
   universities, colleges, madrasahs, or government institutions, use
   institutions_db_tool.
2. If the question is about hospitals, clinics, or health facilities,
   use hospitals_db_tool.
3. If the question is about restaurants, cuisine, ratings, or
   locations, use restaurants_db_tool.
4. Otherwise (general knowledge - definitions, government policy,
   history, culture), use web_search_tool.

When using a DB tool, write a single valid SQLite SELECT query as the
tool input. Never show raw SQL or raw tool output as your final answer
- always explain the result in clear natural language.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_tool_calling_agent(llm=llm, tools=ALL_TOOLS, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=ALL_TOOLS, verbose=True)
